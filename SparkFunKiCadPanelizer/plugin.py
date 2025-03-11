import os
import logging
import wx
import wx.aui

import pcbnew

from .dialog import Dialog

from .panelizer.panelizer import Panelizer

class PanelizerPlugin(pcbnew.ActionPlugin, object):

    def __init__(self):
        super(PanelizerPlugin, self).__init__()

        self.logger = None
        self.config_file = None

        self.name = "Panelize PCB"
        self.category = "Modify PCB"
        self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = True
        icon_dir = os.path.dirname(__file__)
        self.icon_file_name = os.path.join(icon_dir, 'icon.png')
        self.description = "Panelize PCB"
        
        self._pcbnew_frame = None

        self.supportedVersions = ['7.','8.','9.']

        self.kicad_build_version = pcbnew.GetBuildVersion()

    productionDir = "Production"

    def IsSupported(self):
        for v in self.supportedVersions:
            if self.kicad_build_version.startswith(v):
                return True
        return False
    
    def Run(self):
        if self._pcbnew_frame is None:
            try:
                self._pcbnew_frame = [x for x in wx.GetTopLevelWindows() if ('pcbnew' in x.GetTitle().lower() and not 'python' in x.GetTitle().lower()) or ('pcb editor' in x.GetTitle().lower())]
                if len(self._pcbnew_frame) == 1:
                    self._pcbnew_frame = self._pcbnew_frame[0]
                else:
                    self._pcbnew_frame = None
            except:
                pass

        # Construct the config_file path from the board name
        board = pcbnew.GetBoard()
        panelOutputPath = os.path.split(board.GetFileName())[0] # Get the file path head
        panelOutputPath = os.path.join(panelOutputPath, self.productionDir) # Add the production dir
        if not os.path.exists(panelOutputPath):
            os.mkdir(panelOutputPath)
        self.config_file = os.path.join(panelOutputPath, 'panel_config.json')
        self.ordering_instructions = os.path.join(panelOutputPath, 'ordering_instructions.txt')

        logFile = os.path.join(panelOutputPath, 'panelizer.log')
        try:
            os.remove(logFile)
        except FileNotFoundError:
            pass

        self.logger = logging.getLogger('panelizer_logger')
        f_handler = logging.FileHandler(logFile)
        f_handler.setLevel(logging.DEBUG) # Log everything
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)
        self.logger.addHandler(f_handler)

        # Build layer table
        layertable = {}
        numlayers = pcbnew.PCB_LAYER_ID_COUNT
        for i in range(numlayers):
            layertable[i] = {'standardName': board.GetStandardLayerName(i), 'actualName': board.GetLayerName(i)}

        # Check the number of copper layers. Delete unwanted layers from the table.
        wantedCopper = []
        wantedCopper.append("F.Cu")
        wantedCopper.append("B.Cu")
        if (board.GetCopperLayerCount() > 2):
            for i in range(1, board.GetCopperLayerCount() - 1):
                wantedCopper.append("In{}.Cu".format(i))
        deleteLayers = []
        for layer, names in layertable.items():
            if names['standardName'][-3:] == ".Cu":
                if names['standardName'] not in wantedCopper:
                    deleteLayers.append(layer)
        for layer in deleteLayers:
            layertable.pop(layer, None)

        def run_panelizer(dlg, p_panelizer):
            self.logger.log(logging.INFO, "Running Panelizer")

            if not self.IsSupported():
                # Log an error if this version of KiCad has not been tested
                self.logger.log(logging.ERROR, "Version check failed. \"{}\" may not be supported. Panelizing may fail".format(self.kicad_build_version))

            command = []

            convertDimensions = 1.0
            if dlg.CurrentSettings()["dimensionsInchesBtn"]:
                convertDimensions = 25.4
            
            panelx = float(dlg.CurrentSettings()["panelSizeXCtrl"]) * convertDimensions
            panely = float(dlg.CurrentSettings()["panelSizeYCtrl"]) * convertDimensions
            command.extend(['--panelx','{:.6f}'.format(panelx)])
            command.extend(['--panely','{:.6f}'.format(panely)])

            smallerThan = dlg.CurrentSettings()["panelSizeSmallerBtn"]
            if smallerThan:
                command.append('--smaller')
            else:
                command.append('--larger')

            vscorelayer = dlg.CurrentSettings()[dlg.vscore_layer]
            command.extend(['--vscorelayer', vscorelayer, '--vscoretextlayer', vscorelayer])

            gapx = float(dlg.CurrentSettings()["gapsVerticalCtrl"]) * convertDimensions
            gapy = float(dlg.CurrentSettings()["gapsHorizontalCtrl"]) * convertDimensions
            command.extend(['--gapx','{:.6f}'.format(gapx)])
            command.extend(['--gapy','{:.6f}'.format(gapy)])

            removeRight = dlg.CurrentSettings()["removeRightVerticalCheck"]
            if removeRight:
                command.append('--norightgap')

            exposeedge = dlg.CurrentSettings()["productionExposeCheck"]
            if exposeedge:
                command.append('--exposeedge')

            fiducials = dlg.CurrentSettings()["productionBordersCheck"]
            leftright = dlg.CurrentSettings()["productionFiducialsCheck"]
            if not exposeedge:
                if fiducials:
                    # Default the rail width to 1/4" and nudge by 1/4 of the rail width.
                    # This provides the clearance needed for clamping and AOI Inspection of the fiducials.
                    # This is nasty. The default should be in panelizer.py. But I can't think of a solution
                    # which is good for everyone - including anyone running the panelizer from the command line.
                    command.extend(['--hrail','6.35','--vrail','6.35'])
                    command.extend(['--fiducialpos','0.25'])
                    if leftright:
                        command.append('--fiducialslr')
                    else:
                        command.append('--fiducialstb')
            else:
                if fiducials:
                    # Same comment as above
                    command.extend(['--vrail','6.35'])
                    command.extend(['--fiducialpos','0.25'])
                    command.append('--fiducialslr')

            self.logger.log(logging.INFO, command)

            board = pcbnew.GetBoard()

            if board is not None:
                sysExit, report = p_panelizer.startPanelizerCommand(command, board, self.ordering_instructions, self.logger)
                logWarn = logging.INFO
                if sysExit >= 1:
                    logWarn = logging.WARN
                if sysExit >= 2:
                    logWarn = logging.ERROR
                self.logger.log(logWarn, report)
                if sysExit > 0:
                    wx.MessageBox("Panelizer " + ("warning" if (sysExit == 1) else "error") + ".\nPlease check panelizer.log for details.",
                        ("Warning" if (sysExit == 1) else "Error"), wx.OK | (wx.ICON_WARNING if (sysExit == 1) else wx.ICON_ERROR))
                else:
                    wx.MessageBox("Panelizer complete.\nPlease check panelizer.log for details.",
                        "Info", wx.OK | wx.ICON_INFORMATION)
            else:
                self.logger.log(logging.ERROR, "Could not get the board")

            dlg.GetParent().EndModal(wx.ID_OK)

        dlg = Dialog(self._pcbnew_frame, self.config_file, layertable, self.ordering_instructions, Panelizer(), run_panelizer)
    
        try:
            result = dlg.ShowModal()
            if result == wx.ID_OK:
                self.logger.log(logging.INFO, "Panelizer complete")
            elif result == wx.ID_CANCEL:
                self.logger.log(logging.INFO, "Panelizer cancelled")
            else:
                self.logger.log(logging.INFO, "Panelizer finished - " + str(result))

        finally:
            self.logger.removeHandler(f_handler)
            dlg.Destroy()
                        

    