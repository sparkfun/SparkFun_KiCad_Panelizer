"""
    SparkFun's version of:

        Simon John (@sej7278)'s version of:

            kicad-panelizer
            A simple script to create a v-scored panel of a KiCad board.
            Original author: Willem Hillier (@willemcvu)

            https://github.com/willemcvu/kicad-panelizer
        https://github.com/sej7278/kicad-panelizer
"""

__panelizer_version__ = "2.0" # SFE's first version

import os
import sys
from argparse import ArgumentParser
import pcbnew
import logging
from datetime import datetime
import wx

class Panelizer():
    def __init__(self):
        pass

    productionDir = "Production"

    def args_parse(self, args):
        # set up command-line arguments parser
        parser = ArgumentParser(description="A script to panelize KiCad 7 files.")
        parser.add_argument(
            "-v", "--version", action="version", version="%(prog)s " + __panelizer_version__
        )
        parser.add_argument(
            "-p", "--path", help="Path to the *.kicad_pcb file to be panelized"
        )
        parser.add_argument("--numx", type=int, help="Number of boards in X direction")
        parser.add_argument("--numy", type=int, help="Number of boards in Y direction")
        parser.add_argument("--gapx", type=float, default="0.0", help="Gap between boards in X direction (mm), default 0.0")
        parser.add_argument("--gapy", type=float, default="0.0", help="Gap between boards in Y direction (mm), default 0.0")
        parser.add_argument(
            "--norightgap", action="store_true", help="Remove the right-most X gap and insert an extra v-score"
        )
        parser.add_argument("--panelx", type=float, help="Panel size in X direction (mm)")
        parser.add_argument("--panely", type=float, help="Panel size in Y direction (mm)")
        parser.add_argument(
            "--smaller", action="store_true", help="Default: the created panel will be smaller than panelx x panely"
        )
        parser.add_argument(
            "--larger", action="store_true", help="The created panel will be larger than panelx x panely"
        )
        parser.add_argument("--hrail", type=float, default="0.0", help="Horizontal edge rail width (mm)")
        parser.add_argument("--vrail", type=float, default="0.0", help="Vertical edge rail width (mm)")
        parser.add_argument("--hrailtext", help="Text to put on the horizontal edge rail")
        parser.add_argument("--vrailtext", help="Text to put on the vertical edge rail")
        parser.add_argument(
            "--htitle", action="store_true", help="Print title info on horizontal edge rail"
        )
        parser.add_argument(
            "--vtitle", action="store_true", help="Print title info on vertical edge rail"
        )
        parser.add_argument("--textsize", type=float, default="2.0", help="The rail text size (mm), default 2.0")
        parser.add_argument(
            "--vscorelayer", default="User.Comments", help="Layer to put v-score lines on"
        )
        parser.add_argument(
            "--vscoretextlayer", default="User.Comments", help="Layer to put v-score text on"
        )
        parser.add_argument(
            "--vscoretext", default="V-SCORE", help="Text used to indicate v-scores"
        )
        parser.add_argument(
            "--vscorewidth",
            type=float,
            default="0.5",
            help="The width of the v-score lines (mm), default 0.5",
        )
        parser.add_argument(
            "--vscoreextends",
            type=float,
            help="How far past the board to extend the v-score lines (mm), default -vscorewidth/2",
        )
        parser.add_argument(
            "--fiducialslr", action="store_true", help="Add panel fiducials left and right"
        )
        parser.add_argument(
            "--fiducialstb", action="store_true", help="Add panel fiducials top and bottom"
        )
        parser.add_argument(
            "--exposeedge", action="store_true", help="Expose PCB bottom edge - e.g. for M.2 cards"
        )
        parser.add_argument(
            "--verbose", action='store_true', help="Verbose logging")
        return parser.parse_args(args)

    def startPanelizer(self, args, board=None, ordering=None, logger=None):
        """The main method

        Args:
            args - the command line args [1:] - parsed with args_parse
            board - the KiCad BOARD when running in a plugin

        Returns:
            sysExit - the value for sys.exit (if called from __main__)
            report - a helpful text report
        """

        # v-scoring parameters
        V_SCORE_TEXT_SIZE = 2 # mm

        # Panel fiducial parameters
        FIDUCIAL_MASK = 3.0 # mm - Fiducial_1.5mm_Mask3mm
        FIDUCIAL_OFFSET = 2.5 # mm
        FIDUCIAL_FOOTPRINT = "Fiducial_1.5mm_Mask3mm"

        # Minimum spacer for exposed edge panels
        MINIMUM_SPACER = 6.35 # mm

        # 'Extra' ordering instructions
        # Any PCB_TEXT containing any of these keywords will be copied into the ordering instructions
        possibleExtras = ['clean', 'Clean', 'CLEAN']

        sysExit = -1 # -1 indicates sysExit has not (yet) been set. The code below will set this to 0, 1, 2.
        report = "\nSTART: " + datetime.now().isoformat() + "\n"

        if logger is None:
            logger = logging.getLogger()
            logger.setLevel([ logging.WARNING, logging.DEBUG ][args.verbose])

        logger.info('PANELIZER START: ' + datetime.now().isoformat())

        # Read the args
        sourceBoardFile = args.path
        NUM_X = args.numx
        NUM_Y = args.numy
        PANEL_X = args.panelx
        PANEL_Y = args.panely
        GAP_X = args.gapx
        GAP_Y = args.gapy
        REMOVE_RIGHT = args.norightgap
        HORIZONTAL_EDGE_RAIL_WIDTH = args.hrail
        VERTICAL_EDGE_RAIL_WIDTH = args.vrail
        HORIZONTAL_EDGE_RAIL_TEXT = args.hrailtext
        VERTICAL_EDGE_RAIL_TEXT = args.vrailtext
        RAIL_TEXT_SIZE = args.textsize
        V_SCORE_LAYER = args.vscorelayer
        V_SCORE_TEXT_LAYER = args.vscoretextlayer
        V_SCORE_TEXT = args.vscoretext
        V_SCORE_WIDTH = args.vscorewidth
        V_SCORE_LINE_LENGTH_BEYOND_BOARD = args.vscoreextends
        if V_SCORE_LINE_LENGTH_BEYOND_BOARD is None:
            V_SCORE_LINE_LENGTH_BEYOND_BOARD = V_SCORE_WIDTH / 2
        TITLE_X = args.htitle
        TITLE_Y = args.vtitle
        FIDUCIALS_LR = args.fiducialslr
        FIDUCIALS_TB = args.fiducialstb
        EXPOSED_EDGE = args.exposeedge

        # Check if this is running in a plugin
        if board is None:
            if sourceBoardFile is None:
                report += "No path to kicad_pcb file. Quitting.\n"
                sysExit = 2
                return sysExit, report
            else:
                # Check that input board is a *.kicad_pcb file
                sourceFileExtension = os.path.splitext(sourceBoardFile)[1]
                if not sourceFileExtension == ".kicad_pcb":
                    report += sourceBoardFile + " is not a *.kicad_pcb file. Quitting.\n"
                    sysExit = 2
                    return sysExit, report

                # Load source board from file
                board = pcbnew.LoadBoard(sourceBoardFile)
                # Output file name is format \Production\{inputFile}_panelized.kicad_pcb
                panelOutputPath = os.path.split(sourceBoardFile)[0] # Get the file path head
                panelOutputPath = os.path.join(panelOutputPath, self.productionDir) # Add the production dir
                if not os.path.exists(panelOutputPath):
                    os.mkdir(panelOutputPath)
                panelOutputFile = os.path.split(sourceBoardFile)[1] # Get the file path tail
                panelOutputFile = os.path.join(panelOutputPath, os.path.splitext(panelOutputFile)[0] + "_panelized.kicad_pcb")
        else: # Running in a plugin
            panelOutputPath = os.path.split(board.GetFileName())[0] # Get the file path head
            panelOutputPath = os.path.join(panelOutputPath, self.productionDir) # Add the production dir
            if not os.path.exists(panelOutputPath):
                os.mkdir(panelOutputPath)
            panelOutputFile = os.path.split(board.GetFileName())[1] # Get the file path tail
            panelOutputFile = os.path.join(panelOutputPath, os.path.splitext(panelOutputFile)[0] + "_panelized.kicad_pcb")

        if board is None:
            report += "Could not load board. Quitting.\n"
            sysExit = 2
            return sysExit, report    

        # Check if about to overwrite a panel
        if os.path.isfile(panelOutputFile):
            if wx.GetApp() is not None:
                resp = wx.MessageBox("You are about to overwrite a panel file.\nAre you sure?",
                            'Warning', wx.OK | wx.CANCEL | wx.ICON_WARNING)
                if resp != wx.OK:
                    report += "User does not want to overwrite the panel. Quitting.\n"
                    sysExit = 1
                    return sysExit, report

        # Check that rails are at least RAIL_TEXT_SIZE plus 1mm
        if (((HORIZONTAL_EDGE_RAIL_TEXT or TITLE_X) and (HORIZONTAL_EDGE_RAIL_WIDTH < (RAIL_TEXT_SIZE + 2))) or
            ((VERTICAL_EDGE_RAIL_TEXT or TITLE_Y) and (VERTICAL_EDGE_RAIL_WIDTH < (RAIL_TEXT_SIZE + 2)))):
            report += "Rails are not large enough for the selected text. Quitting.\n"
            sysExit = 2
            return sysExit, report

        # Only allow numbers or panels
        if (PANEL_X or PANEL_Y) and (NUM_X or NUM_Y):
            report += "Specify number of boards or size of panel, not both. Quitting.\n"
            sysExit = 2
            return sysExit, report

        # Expect panel size or number of boards
        if (not PANEL_X or not PANEL_Y) and (not NUM_X or not NUM_Y):
            report += "Specify number of boards or size of panel. Quitting.\n"
            sysExit = 2
            return sysExit, report

        # Check the fiducials
        if (FIDUCIALS_LR and (VERTICAL_EDGE_RAIL_WIDTH < (FIDUCIAL_MASK + 1))):
            report += "Cannot add L+R fiducials - edge rails not wide enough.\n"
            FIDUCIALS_LR = False
            sysExit = 1
        if (FIDUCIALS_TB and (HORIZONTAL_EDGE_RAIL_WIDTH < (FIDUCIAL_MASK + 1))):
            report += "Cannot add T+B fiducials - edge rails not wide enough.\n"
            FIDUCIALS_TB = False
            sysExit = 1

        # Check smaller / larger
        if args.smaller and args.larger:
            report += "Both smaller- and larger-than were selected. Defaulting to smaller-than.\n"
            sysExit = 1
        if args.smaller:
            SMALLER_THAN = True
        elif args.larger:
            SMALLER_THAN = False
        else: # Both - or neither
            SMALLER_THAN = True

        # Check gaps
        if (GAP_X != 0.0) and (GAP_Y != 0.0):
            report += "Specify X or Y gaps, not both. Quitting.\n"
            sysExit = 2
            return sysExit, report
        if (GAP_X != 0.0) and (HORIZONTAL_EDGE_RAIL_WIDTH == 0.0):
            report += "Can not have X gaps without horizontal rails. Quitting.\n"
            sysExit = 2
            return sysExit, report
        if (GAP_Y != 0.0) and (VERTICAL_EDGE_RAIL_WIDTH == 0.0):
            report += "Can not have Y gaps without vertical rails. Quitting.\n"
            sysExit = 2
            return sysExit, report

        # Check exposed edge
        if EXPOSED_EDGE:
            if GAP_X > 0.0 or GAP_Y > 0.0:
                report += "Can not have gaps on exposed edge panels. Quitting.\n"
                sysExit = 2
                return sysExit, report
            if HORIZONTAL_EDGE_RAIL_TEXT or HORIZONTAL_EDGE_RAIL_WIDTH > 0.0 or TITLE_X:
                report += "Can not have horizontal rails or text on exposed edge panels. Quitting.\n"
                sysExit = 2
                return sysExit, report
            if NUM_Y:
                if NUM_Y > 2:
                    report += "Can not have more than two rows on exposed edge panels. Quitting.\n"
                    sysExit = 2
                    return sysExit, report

        # All dimension parameters used by this script are mm unless otherwise noted
        # KiCad works in nm (integer)
        SCALE = 1000000 # Convert mm to nm

        # Set up layer table
        layertable = {}
        numlayers = pcbnew.PCB_LAYER_ID_COUNT
        for i in range(numlayers):
            layertable[board.GetLayerName(i)] = i

        # Get dimensions of board
        # Note: the bounding box width and height _include_ the Edge.Cuts line width.
        #       We will subtract it.
        boardWidth = board.GetBoardEdgesBoundingBox().GetWidth() # nm
        boardHeight = board.GetBoardEdgesBoundingBox().GetHeight() # nm
        boardCenter = board.GetBoardEdgesBoundingBox().GetCenter()

        boardLeftEdge = boardCenter.x - boardWidth / 2
        boardRightEdge = boardCenter.x + boardWidth / 2
        boardTopEdge = boardCenter.y - boardHeight / 2
        boardBottomEdge = boardCenter.y + boardHeight / 2

        cutWidth = 0
        drawings = board.GetDrawings()
        for drawing in drawings:
            if drawing.IsOnLayer(layertable["Edge.Cuts"]):
                if drawing.GetWidth() > cutWidth:
                    cutWidth = drawing.GetWidth()
        #report += "Subtracting Edge.Cuts line width of {}mm.\n".format(cutWidth / SCALE)
        boardWidth -= cutWidth
        boardHeight -= cutWidth

        # Print report
        report += (
            "\nBoard: "
            + str(panelOutputFile)
            #+ "\nGenerated with: ./panelizer.py "
            #+ str(args)
            + "\n"
        )
        report += "Board dimensions: "
        report += "{:.2f} x ".format(boardWidth / SCALE)
        report += "{:.2f} mm.\n".format(boardHeight / SCALE)

        boardWidth += GAP_X * SCALE # convert mm to nm
        boardWidth += V_SCORE_WIDTH * SCALE # Add v-score width
        boardHeight += GAP_Y * SCALE # convert mm to nm
        boardHeight += V_SCORE_WIDTH * SCALE # Add v-score width

        # How many whole boards can we fit on the panel?
        # For simplicity, don't include the edge rail widths in this calculation.
        # (Assume panelx and panely define the PnP working area)
        spacerHeight = 0
        if not EXPOSED_EDGE:
            if PANEL_X:
                NUM_X = int((PANEL_X * SCALE) / boardWidth)
                if not SMALLER_THAN:
                    while (NUM_X * boardWidth) < (PANEL_X * SCALE):
                        NUM_X += 1
            if PANEL_Y:
                NUM_Y = int((PANEL_Y * SCALE) / boardHeight)
                if not SMALLER_THAN:
                    while (NUM_Y * boardHeight) < (PANEL_Y * SCALE):
                        NUM_Y += 1
        else:
            # Exposed edge: calculate if the panel can accomodate one or two rows
            if PANEL_X:
                NUM_X = int((PANEL_X * SCALE) / boardWidth)
                if not SMALLER_THAN:
                    while (NUM_X * boardWidth) < (PANEL_X * SCALE):
                        NUM_X += 1
            if PANEL_Y:
                if not SMALLER_THAN:
                    NUM_Y = 2
                elif (PANEL_Y * SCALE) < boardHeight:
                    NUM_Y = 0
                elif (PANEL_Y * SCALE) > ((boardHeight * 2 ) + (MINIMUM_SPACER * SCALE)):
                    NUM_Y = 2
                else:
                    NUM_Y = 1

            if NUM_Y == 2:
                spacerHeight = int(MINIMUM_SPACER * SCALE) # If PANEL_Y is not defined, add the minimum spacer
                if PANEL_Y:
                    spacerHeight = int((PANEL_Y * SCALE) - (boardHeight * 2))
                    if spacerHeight < (MINIMUM_SPACER * SCALE):
                        if not SMALLER_THAN:
                            spacerHeight = MINIMUM_SPACER * SCALE
                        else:
                            NUM_Y = 0

        # Check we can actually panelize the board
        if NUM_X == 0 or NUM_Y == 0:
            report += "Panel size is too small for board. Quitting.\n"
            sysExit = 2
            return sysExit, report    

        if PANEL_X or PANEL_Y:
            report += "You can fit " + str(NUM_X) + " x " + str(NUM_Y) + " boards on the panel.\n"
        
        orderingInstructionsSeen = False
        sparkfunLogoSeen = False
        sparkxLogoSeen = False
        solderMask = None
        silkscreen = None
        numLayers = None
        controlledImpedance = None
        finish = None
        thickness = None
        material = None
        copperWeight = None
        orderingExtras = None

        # Array of tracks
        # Note: Duplicate uses the same net name for the duplicated track.
        #       This creates DRC unconnected net errors. (KiKit does this properly...)
        minTrackWidth = 999999999
        minViaDrill = 999999999
        tracks = board.GetTracks()
        newTracks = []
        for sourceTrack in tracks:  # iterate through each track to be copied
            width = sourceTrack.GetWidth()
            if width < minTrackWidth:
                minTrackWidth = width
            if isinstance(sourceTrack, pcbnew.PCB_VIA):
                drill = sourceTrack.GetDrill()
                if drill < minViaDrill:
                    minViaDrill = drill
            layer = sourceTrack.GetLayerName()
            if numLayers is None and ("In1.Cu" in layer or "In2.Cu" in layer):
                numLayers = "Layers: 4"
            if "In3.Cu" in layer or "In4.Cu" in layer:
                numLayers = "Layers: 6"
            for x in range(0, NUM_X):  # iterate through x direction
                for y in range(0, NUM_Y):  # iterate through y direction
                    if (x != 0) or (y != 0):  # do not duplicate source object to location
                        newTrack = sourceTrack.Duplicate()
                        xpos = int(x * boardWidth)
                        ypos = int(-y * boardHeight)
                        if EXPOSED_EDGE and (y == 1):
                            centre = pcbnew.VECTOR2I(boardCenter.x, boardCenter.y)
                            angle = pcbnew.EDA_ANGLE(1800, pcbnew.TENTHS_OF_A_DEGREE_T)
                            newTrack.Rotate(centre, angle)
                            ypos -= int(spacerHeight + V_SCORE_WIDTH * SCALE)
                        newTrack.Move(
                            pcbnew.VECTOR2I(xpos, ypos)
                        )  # move to correct location
                        newTracks.append(newTrack)  # add to temporary list of tracks

        for track in newTracks:
            board.Add(track)

        # Array of modules
        modules = board.GetFootprints()
        newModules = []
        prodIDs = []
        for sourceModule in modules:
            if "Ordering_Instructions" in sourceModule.GetFPIDAsString():
                orderingInstructionsSeen = True
            if "SparkFun_Logo" in sourceModule.GetFPIDAsString():
                sparkfunLogoSeen = True
            if "SparkX_Logo" in sourceModule.GetFPIDAsString():
                sparkxLogoSeen = True
            pos = sourceModule.GetPosition() # Check if footprint is outside the bounding box
            if pos.x >= boardLeftEdge and pos.x <= boardRightEdge and \
                pos.y >= boardTopEdge and pos.y <= boardBottomEdge:
                for x in range(0, NUM_X):  # iterate through x direction
                    for y in range(0, NUM_Y):  # iterate through y direction
                        if (x != 0) or (y != 0): # do not duplicate source object to location
                            newModule = pcbnew.FOOTPRINT(sourceModule)
                            ref = ""
                            if hasattr(newModule, "Reference"):
                                ref = newModule.Reference().GetText()
                            if EXPOSED_EDGE and (y == 1):
                                centre = pcbnew.VECTOR2I(boardCenter.x, boardCenter.y)
                                angle = pcbnew.EDA_ANGLE(1800, pcbnew.TENTHS_OF_A_DEGREE_T)
                                newModule.Rotate(centre, angle)
                            xpos = int(x * boardWidth + newModule.GetPosition().x)
                            ypos = int(-y * boardHeight + newModule.GetPosition().y)
                            if EXPOSED_EDGE and (y == 1):
                                ypos -= int(spacerHeight + V_SCORE_WIDTH * SCALE)
                            newModule.SetPosition(pcbnew.VECTOR2I(xpos,ypos))
                            newModules.append(newModule)
                            if hasattr(sourceModule, "HasProperty"):
                                if sourceModule.HasProperty("PROD_ID"):
                                    prodIDs.append([sourceModule.GetPropertyNative("PROD_ID"), ref])
                        else: # Add source object to prodIDs
                            if hasattr(sourceModule, "HasProperty"):
                                if sourceModule.HasProperty("PROD_ID"):
                                    ref = ""
                                    if hasattr(sourceModule, "Reference"):
                                        ref = sourceModule.Reference().GetText()
                                    prodIDs.append([sourceModule.GetPropertyNative("PROD_ID"), ref])
            else: # Move source modules which are outside the bounding box
                if pos.y > boardBottomEdge: # If the drawing is below the bottom edge, move it below the rail
                    sourceModule.Move(pcbnew.VECTOR2I(0, int(HORIZONTAL_EDGE_RAIL_WIDTH * SCALE)))
                elif pos.x > boardRightEdge: # If the drawing is to the right, move it beyond the panel
                    sourceModule.Move(pcbnew.VECTOR2I(int(((NUM_X - 1) * boardWidth) + (VERTICAL_EDGE_RAIL_WIDTH * SCALE)), 0))
                elif pos.y < boardTopEdge: # If the drawing is above the top edge, move it above the panel
                    sourceModule.Move(pcbnew.VECTOR2I(0, int((-(NUM_Y - 1) * boardHeight) - (HORIZONTAL_EDGE_RAIL_WIDTH * SCALE))))
                else: # elif pos.x < boardLeftEdge: # If the drawing is to the left, move it outside the rail
                    sourceModule.Move(pcbnew.VECTOR2I(int(-VERTICAL_EDGE_RAIL_WIDTH * SCALE), 0))

        for module in newModules:
            board.Add(module)

        if sparkfunLogoSeen:
            solderMask = "Solder Mask: Red"
            silkscreen = "Silkscreen: White"
        if sparkxLogoSeen:
            solderMask = "Solder Mask: Black"
            silkscreen = "Silkscreen: White"

        # Array of zones
        modules = board.GetFootprints()
        newZones = []
        for a in range(0, board.GetAreaCount()):
            for x in range(0, NUM_X):  # iterate through x direction
                for y in range(0, NUM_Y):  # iterate through y direction
                    if (x != 0) or (y != 0):  # do not duplicate source object to location
                        sourceZone = board.GetArea(a)
                        newZone = sourceZone.Duplicate()
                        newZone.SetNet(sourceZone.GetNet())
                        xpos = int(x * boardWidth)
                        ypos = int(-y * boardHeight)
                        if EXPOSED_EDGE and (y == 1):
                            centre = pcbnew.VECTOR2I(boardCenter.x, boardCenter.y)
                            angle = pcbnew.EDA_ANGLE(1800, pcbnew.TENTHS_OF_A_DEGREE_T)
                            newZone.Rotate(centre, angle)
                            ypos -= int(spacerHeight + V_SCORE_WIDTH * SCALE)
                        newZone.Move(
                            pcbnew.VECTOR2I(xpos, ypos)
                        )
                        newZones.append(newZone)

        for zone in newZones:
            board.Add(zone)

        # Array of drawing objects
        drawings = board.GetDrawings()
        newDrawings = []
        for sourceDrawing in drawings:
            if isinstance(sourceDrawing, pcbnew.PCB_TEXT):
                txt = sourceDrawing.GetShownText()
                if "mask" in txt or "Mask" in txt or "MASK" in txt:
                    solderMask = txt
                if "layers" in txt or "Layers" in txt or "LAYERS" in txt:
                    if numLayers is None: # Should we trust the instructions or the tracks?!
                        numLayers = txt
                if "impedance" in txt or "Impedance" in txt or "IMPEDANCE" in txt:
                    controlledImpedance = txt
                if "finish" in txt or "Finish" in txt or "FINISH" in txt:
                    finish = txt
                if "thickness" in txt or "Thickness" in txt or "THICKNESS" in txt:
                    thickness = txt
                if "material" in txt or "Material" in txt or "MATERIAL" in txt:
                    material = txt            
                if "weight" in txt or "Weight" in txt or "WEIGHT" in txt or "oz" in txt or "Oz" in txt or "OZ" in txt:
                    copperWeight = txt
                for extra in possibleExtras:
                    if extra in txt:
                        if orderingExtras is None:
                            orderingExtras = ""
                        orderingExtras += txt + "\n"
            pos = sourceDrawing.GetPosition() # Check if drawing is outside the bounding box
            if pos.x >= boardLeftEdge and pos.x <= boardRightEdge and \
                pos.y >= boardTopEdge and pos.y <= boardBottomEdge:
                for x in range(0, NUM_X):  # iterate through x direction
                    for y in range(0, NUM_Y):  # iterate through y direction
                        if (x != 0) or (y != 0):  # do not duplicate source object to location
                            newDrawing = sourceDrawing.Duplicate()
                            xpos = int(x * boardWidth)
                            ypos = int(-y * boardHeight)
                            if EXPOSED_EDGE and (y == 1):
                                centre = pcbnew.VECTOR2I(boardCenter.x, boardCenter.y)
                                angle = pcbnew.EDA_ANGLE(1800, pcbnew.TENTHS_OF_A_DEGREE_T)
                                newDrawing.Rotate(centre, angle)
                                ypos -= int(spacerHeight + V_SCORE_WIDTH * SCALE)
                            newDrawing.Move(
                                pcbnew.VECTOR2I(xpos, ypos)
                            )
                            newDrawings.append(newDrawing)
            else: # Move source drawings which are outside the bounding box
                #if txt is not None: # Copy all text outside the bounding box to the report
                #    report += txt + "\n"
                if pos.y > boardBottomEdge: # If the drawing is below the bottom edge, move it below the rail
                    sourceDrawing.Move(pcbnew.VECTOR2I(0, int(HORIZONTAL_EDGE_RAIL_WIDTH * SCALE)))
                elif pos.x > boardRightEdge: # If the drawing is to the right, move it beyond the panel
                    sourceDrawing.Move(pcbnew.VECTOR2I(int(((NUM_X - 1) * boardWidth) + (VERTICAL_EDGE_RAIL_WIDTH * SCALE)), 0))
                elif pos.y < boardTopEdge: # If the drawing is above the top edge, move it above the panel
                    sourceDrawing.Move(pcbnew.VECTOR2I(0, int((-(NUM_Y - 1) * boardHeight) - (HORIZONTAL_EDGE_RAIL_WIDTH * SCALE))))
                else: # elif pos.x < boardLeftEdge: # If the drawing is to the left, move it outside the rail
                    sourceDrawing.Move(pcbnew.VECTOR2I(int(-VERTICAL_EDGE_RAIL_WIDTH * SCALE), 0))

        for drawing in newDrawings:
            board.Add(drawing)

        # Get dimensions and center coordinate of entire array (without siderails to be added shortly)
        arrayWidth = board.GetBoardEdgesBoundingBox().GetWidth()
        arrayWidth -= cutWidth
        arrayHeight = board.GetBoardEdgesBoundingBox().GetHeight()
        arrayHeight -= cutWidth
        arrayCenter = board.GetBoardEdgesBoundingBox().GetCenter()

        spacerLeft = arrayCenter.x - arrayWidth / 2
        spacerRight = arrayCenter.x + arrayWidth / 2
        spacerTop = arrayCenter.y - spacerHeight / 2
        spacerBottom = arrayCenter.y + spacerHeight / 2

        # SFE: On SFE panels, we keep all the existing edge cuts and let JLCPCB figure out which are
        #      true edges and which are v-scores. Also, if the edges are not straight lines, it gets
        #      complicated quickly. (The original version of this panelizer only worked on rectangular
        #      boards.) (Use KiKit if you want to avoid the redundant edge cuts.)
        #
        # Erase all existing edgeCuts objects (individual board outlines)
        #drawings = board.GetDrawings()
        #for drawing in drawings:
        #    if drawing.IsOnLayer(layertable["Edge.Cuts"]):
        #        drawing.DeleteStructure()

        # Rail Edge.Cuts
        v_score_top_outer = int(
            arrayCenter.y
            - arrayHeight / 2
            - GAP_Y * SCALE
            - V_SCORE_WIDTH * SCALE
            - HORIZONTAL_EDGE_RAIL_WIDTH * SCALE
            )
        v_score_top_inner = int(v_score_top_outer + HORIZONTAL_EDGE_RAIL_WIDTH * SCALE)
        v_score_bottom_outer = int(
            arrayCenter.y
            + arrayHeight / 2
            + GAP_Y * SCALE
            + V_SCORE_WIDTH * SCALE
            + HORIZONTAL_EDGE_RAIL_WIDTH * SCALE
            )
        v_score_bottom_inner = int(v_score_bottom_outer - HORIZONTAL_EDGE_RAIL_WIDTH * SCALE)
        v_score_left_outer = int(
            arrayCenter.x
            - arrayWidth / 2
            - GAP_X * SCALE
            - V_SCORE_WIDTH * SCALE
            - VERTICAL_EDGE_RAIL_WIDTH * SCALE
            )
        v_score_left_inner = v_score_left_outer + VERTICAL_EDGE_RAIL_WIDTH * SCALE
        v_score_right_outer = int(
            arrayCenter.x
            + arrayWidth / 2
            + ((GAP_X * SCALE) if (not REMOVE_RIGHT) else 0.0)
            + V_SCORE_WIDTH * SCALE
            + VERTICAL_EDGE_RAIL_WIDTH * SCALE
            )
        v_score_right_inner = v_score_right_outer - VERTICAL_EDGE_RAIL_WIDTH * SCALE

        # Define rail edge cuts - if any
        edgeCuts = []
        if EXPOSED_EDGE and (NUM_Y == 2):
            # Add the spacer
            edgeCuts.append([spacerLeft, spacerTop,
                             spacerRight, spacerTop])
            edgeCuts.append([spacerRight, spacerTop,
                             spacerRight, spacerBottom])
            edgeCuts.append([spacerRight, spacerBottom,
                             spacerLeft, spacerBottom])
            edgeCuts.append([spacerLeft, spacerBottom,
                             spacerLeft, spacerTop])
        if HORIZONTAL_EDGE_RAIL_WIDTH > 0.0 and VERTICAL_EDGE_RAIL_WIDTH > 0.0:
            # Both vertical and horizontal edges, continuous border
            edgeCuts.append([v_score_left_outer, v_score_top_outer,
                             v_score_right_outer, v_score_top_outer])
            edgeCuts.append([v_score_right_outer, v_score_top_outer,
                             v_score_right_outer, v_score_bottom_outer])
            edgeCuts.append([v_score_right_outer, v_score_bottom_outer,
                             v_score_left_outer, v_score_bottom_outer])
            edgeCuts.append([v_score_left_outer, v_score_bottom_outer,
                             v_score_left_outer, v_score_top_outer])
            edgeCuts.append([v_score_left_inner, v_score_top_inner,
                             v_score_right_inner, v_score_top_inner])
            edgeCuts.append([v_score_right_inner, v_score_top_inner,
                             v_score_right_inner, v_score_bottom_inner])
            edgeCuts.append([v_score_right_inner, v_score_bottom_inner,
                             v_score_left_inner, v_score_bottom_inner])
            edgeCuts.append([v_score_left_inner, v_score_bottom_inner,
                             v_score_left_inner, v_score_top_inner])
            #report += "Adding both horizontal and vertical rails.\n"
        elif HORIZONTAL_EDGE_RAIL_WIDTH > 0.0:
            # Horizontal edges only
            v_score_left_inner += V_SCORE_WIDTH * SCALE
            v_score_right_inner -= V_SCORE_WIDTH * SCALE
            v_score_left_inner += GAP_X * SCALE
            v_score_right_inner -= (GAP_X * SCALE) if (not REMOVE_RIGHT) else 0.0
            edgeCuts.append([v_score_left_inner, v_score_top_outer,
                             v_score_right_inner, v_score_top_outer])
            edgeCuts.append([v_score_right_inner, v_score_top_outer,
                             v_score_right_inner, v_score_top_inner])
            edgeCuts.append([v_score_right_inner, v_score_top_inner,
                             v_score_left_inner, v_score_top_inner])
            edgeCuts.append([v_score_left_inner, v_score_top_inner,
                             v_score_left_inner, v_score_top_outer])
            edgeCuts.append([v_score_left_inner, v_score_bottom_inner,
                             v_score_right_inner, v_score_bottom_inner])
            edgeCuts.append([v_score_right_inner, v_score_bottom_inner,
                             v_score_right_inner, v_score_bottom_outer])
            edgeCuts.append([v_score_right_inner, v_score_bottom_outer,
                             v_score_left_inner, v_score_bottom_outer])
            edgeCuts.append([v_score_left_inner, v_score_bottom_outer,
                             v_score_left_inner, v_score_bottom_inner])
            #report += "Adding horizontal rails only.\n"
        elif VERTICAL_EDGE_RAIL_WIDTH > 0.0:
            # VERTICAL edges only
            v_score_top_inner += V_SCORE_WIDTH * SCALE
            v_score_bottom_inner -= V_SCORE_WIDTH * SCALE
            v_score_top_inner += GAP_Y * SCALE
            v_score_bottom_inner -= GAP_Y * SCALE
            edgeCuts.append([v_score_left_outer, v_score_top_inner,
                             v_score_left_inner, v_score_top_inner])
            edgeCuts.append([v_score_left_inner, v_score_top_inner,
                             v_score_left_inner, v_score_bottom_inner])
            edgeCuts.append([v_score_left_inner, v_score_bottom_inner,
                             v_score_left_outer, v_score_bottom_inner])
            edgeCuts.append([v_score_left_outer, v_score_bottom_inner,
                             v_score_left_outer, v_score_top_inner])
            edgeCuts.append([v_score_right_inner, v_score_top_inner,
                             v_score_right_outer, v_score_top_inner])
            edgeCuts.append([v_score_right_outer, v_score_top_inner,
                             v_score_right_outer, v_score_bottom_inner])
            edgeCuts.append([v_score_right_outer, v_score_bottom_inner,
                             v_score_right_inner, v_score_bottom_inner])
            edgeCuts.append([v_score_right_inner, v_score_bottom_inner,
                             v_score_right_inner, v_score_top_inner])
            #report += "Adding vertical rails only.\n"
        else:
            pass # report += "Adding no rails.\n"

        # Add rail cuts - if any
        for cut in edgeCuts:
            edge = pcbnew.PCB_SHAPE(board)
            board.Add(edge)
            edge.SetStart(pcbnew.VECTOR2I(int(cut[0]), int(cut[1])))
            edge.SetEnd(pcbnew.VECTOR2I(int(cut[2]), int(cut[3])))
            edge.SetLayer(layertable["Edge.Cuts"])

        # Re-calculate board dimensions with new edge cuts
        panelWidth = board.GetBoardEdgesBoundingBox().GetWidth()
        panelWidth -= cutWidth
        panelHeight = board.GetBoardEdgesBoundingBox().GetHeight()
        panelHeight -= cutWidth
        panelCenter = board.GetBoardEdgesBoundingBox().GetCenter()

        # Absolute edges of v-scoring
        vscore_top = (
            panelCenter.y
            - panelHeight / 2
            - V_SCORE_LINE_LENGTH_BEYOND_BOARD * SCALE
        )
        vscore_bottom = (
            panelCenter.y
            + panelHeight / 2
            + V_SCORE_LINE_LENGTH_BEYOND_BOARD * SCALE
        )
        vscore_right = (
            panelCenter.x
            + panelWidth / 2
            + V_SCORE_LINE_LENGTH_BEYOND_BOARD * SCALE
        )
        vscore_left = (
            panelCenter.x
            - panelWidth / 2
            - V_SCORE_LINE_LENGTH_BEYOND_BOARD * SCALE
        )

        # Vertical v-scores
        # Add v-scores only if vertical gaps (running top to bottom, defined in X)
        # are <= V_SCORE_WIDTH. Unless REMOVE_RIGHT is true.
        v_score_x = []
        
        if GAP_X <= V_SCORE_WIDTH:
            if VERTICAL_EDGE_RAIL_WIDTH > 0:
                RANGE_START = 0
                RANGE_END = NUM_X + 1
            else:
                RANGE_START = 1
                RANGE_END = NUM_X
            for x in range(RANGE_START, RANGE_END):
                v_score_x.append(
                    arrayCenter.x
                    - arrayWidth / 2
                    - GAP_X * SCALE / 2
                    - V_SCORE_WIDTH * SCALE / 2
                    + boardWidth * x
                )
        else:
            # Board has vertical gaps. Check REMOVE_RIGHT
            if REMOVE_RIGHT:
                v_score_x.append(
                    arrayCenter.x
                    + arrayWidth / 2
                    + V_SCORE_WIDTH * SCALE / 2
                )

        for x_loc in v_score_x:
            v_score_line = pcbnew.PCB_SHAPE(board)
            v_score_line.SetStart(pcbnew.VECTOR2I(int(x_loc), int(vscore_top)))
            v_score_line.SetEnd(pcbnew.VECTOR2I(int(x_loc), int(vscore_bottom)))
            v_score_line.SetLayer(layertable[V_SCORE_LAYER])
            v_score_line.SetWidth(int(V_SCORE_WIDTH * SCALE))
            board.Add(v_score_line)
            v_score_text = pcbnew.PCB_TEXT(board)
            v_score_text.SetText(V_SCORE_TEXT)
            v_score_text.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_LEFT)
            v_score_text.SetPosition(
                pcbnew.VECTOR2I(int(x_loc), int(vscore_top - V_SCORE_TEXT_SIZE * SCALE))
            )
            v_score_text.SetTextSize(
                pcbnew.VECTOR2I(SCALE * V_SCORE_TEXT_SIZE, SCALE * V_SCORE_TEXT_SIZE)
            )
            v_score_text.SetLayer(layertable[V_SCORE_TEXT_LAYER])
            v_score_text.SetTextAngle(pcbnew.EDA_ANGLE(900, pcbnew.TENTHS_OF_A_DEGREE_T))
            board.Add(v_score_text)

        # Horizontal v-scores
        # Add v-scores only if the horizontal gaps (running left to right, defined in Y)
        # are <= V_SCORE_WIDTH. Ignore for larger gaps.
        v_score_y = []

        if EXPOSED_EDGE and (NUM_Y == 2):
            v_score_y.append(
                spacerBottom
                + V_SCORE_WIDTH * SCALE / 2
            )
            v_score_y.append(
                spacerTop
                - V_SCORE_WIDTH * SCALE / 2
            )
        elif GAP_Y <= V_SCORE_WIDTH:
            if HORIZONTAL_EDGE_RAIL_WIDTH > 0:
                RANGE_START = 0
                RANGE_END = NUM_Y + 1
            else:
                RANGE_START = 1
                RANGE_END = NUM_Y
            for y in range(RANGE_START, RANGE_END):
                v_score_y.append(
                    arrayCenter.y
                    - arrayHeight / 2
                    - GAP_Y * SCALE / 2
                    - V_SCORE_WIDTH * SCALE / 2
                    + boardHeight * y
                )

        for y_loc in v_score_y:
            v_score_line = pcbnew.PCB_SHAPE(board)
            v_score_line.SetStart(pcbnew.VECTOR2I(int(vscore_left), int(y_loc)))
            v_score_line.SetEnd(pcbnew.VECTOR2I(int(vscore_right), int(y_loc)))
            v_score_line.SetLayer(layertable[V_SCORE_LAYER])
            v_score_line.SetWidth(int(V_SCORE_WIDTH * SCALE))
            board.Add(v_score_line)
            v_score_text = pcbnew.PCB_TEXT(board)
            v_score_text.SetText(V_SCORE_TEXT)
            v_score_text.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_RIGHT)
            v_score_text.SetPosition(
                pcbnew.VECTOR2I(int(vscore_left - V_SCORE_TEXT_SIZE * SCALE), int(y_loc))
            )
            v_score_text.SetTextSize(
                pcbnew.VECTOR2I(SCALE * V_SCORE_TEXT_SIZE, SCALE * V_SCORE_TEXT_SIZE)
            )
            v_score_text.SetLayer(layertable[V_SCORE_TEXT_LAYER])
            v_score_text.SetTextAngle(pcbnew.EDA_ANGLE(0, pcbnew.TENTHS_OF_A_DEGREE_T))
            board.Add(v_score_text)

        # Add route out text
        route_outs = []
        if GAP_X > 0.0:
            if VERTICAL_EDGE_RAIL_WIDTH > 0.0:
                RANGE_START = 0
                if not REMOVE_RIGHT:
                    RANGE_END = NUM_X + 1
                else:
                    RANGE_END = NUM_X
            else:
                RANGE_START = 1
                RANGE_END = NUM_X
            for x in range(RANGE_START, RANGE_END):
                route_outs.append([
                    int(
                        arrayCenter.x
                        - arrayWidth / 2
                        - GAP_X * SCALE / 2
                        - V_SCORE_WIDTH * SCALE / 2
                        + boardWidth * x
                    ),
                    int(arrayCenter.y),
                    900
                ])
        if GAP_Y > 0.0:
            if HORIZONTAL_EDGE_RAIL_WIDTH > 0.0:
                RANGE_START = 0
                RANGE_END = NUM_Y + 1
            else:
                RANGE_START = 1
                RANGE_END = NUM_Y
            for y in range(RANGE_START, RANGE_END):
                route_outs.append([
                    int(arrayCenter.x),
                    int(
                        arrayCenter.y
                        - arrayHeight / 2
                        - GAP_Y * SCALE / 2
                        - V_SCORE_WIDTH * SCALE / 2
                        + boardHeight * y
                    ),
                    0
                ])
        for pos in route_outs:
            route_text = pcbnew.PCB_TEXT(board)
            route_text.SetText("ROUTE OUT")
            route_text.SetTextSize(pcbnew.VECTOR2I(SCALE * V_SCORE_TEXT_SIZE, SCALE * V_SCORE_TEXT_SIZE))
            route_text.SetLayer(layertable[V_SCORE_TEXT_LAYER])
            route_text.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
            route_text.SetPosition(pcbnew.VECTOR2I(pos[0], pos[1]))
            route_text.SetTextAngle(pcbnew.EDA_ANGLE(pos[2], pcbnew.TENTHS_OF_A_DEGREE_T))
            board.Add(route_text)

        # Add Do Not Remove text on exposed edge panel
        if EXPOSED_EDGE and (NUM_Y == 2):
            route_text = pcbnew.PCB_TEXT(board)
            route_text.SetText("DO NOT REMOVE")
            route_text.SetTextSize(pcbnew.VECTOR2I(SCALE * V_SCORE_TEXT_SIZE, SCALE * V_SCORE_TEXT_SIZE))
            route_text.SetLayer(layertable[V_SCORE_TEXT_LAYER])
            route_text.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
            route_text.SetPosition(pcbnew.VECTOR2I(arrayCenter.x, arrayCenter.y))
            board.Add(route_text)

        # Add fiducials

        # Find the KiCad Fiducial footprints
        fiducialPath = os.getenv('KICAD7_FOOTPRINT_DIR') # This works when running the plugin inside KiCad
        if fiducialPath is not None:
            fiducialPath = os.path.join(fiducialPath,"Fiducial.pretty")
        else:
            fiducialPath = os.getenv('PYTHONHOME') # This works when running the panelizer manually in a KiCad Command Prompt
            if fiducialPath is not None:
                fiducialPath = os.path.join(fiducialPath,"..","share","kicad","footprints","Fiducial.pretty")

        if fiducialPath is None:
            report += "Could not find a path to Fiducial.pretty. Unable to add fiducials.\n"
            sysExit = 1
        else:
            fiducials = []
            if FIDUCIALS_LR:
                fiducials.append([
                    int(panelCenter.x - (panelWidth / 2 - VERTICAL_EDGE_RAIL_WIDTH / 2 * SCALE)),
                    int(panelCenter.y - (panelHeight / 2 - (SCALE * FIDUCIAL_OFFSET + SCALE * HORIZONTAL_EDGE_RAIL_WIDTH)))
                ])
                fiducials.append([
                    int(panelCenter.x - (panelWidth / 2 - VERTICAL_EDGE_RAIL_WIDTH / 2 * SCALE)),
                    int(panelCenter.y + (panelHeight / 2 - (SCALE * FIDUCIAL_OFFSET + SCALE * HORIZONTAL_EDGE_RAIL_WIDTH)))
                ])
                fiducials.append([
                    int(panelCenter.x + (panelWidth / 2 - VERTICAL_EDGE_RAIL_WIDTH / 2 * SCALE)),
                    int(panelCenter.y - (panelHeight / 2 - (SCALE * FIDUCIAL_OFFSET + SCALE * HORIZONTAL_EDGE_RAIL_WIDTH)))
                ])
            if FIDUCIALS_TB:
                fiducials.append([
                    int(panelCenter.x - (panelWidth / 2 - (SCALE * FIDUCIAL_OFFSET + SCALE * VERTICAL_EDGE_RAIL_WIDTH))),
                    int(panelCenter.y + (panelHeight / 2 - HORIZONTAL_EDGE_RAIL_WIDTH / 2 * SCALE))
                ])
                fiducials.append([
                    int(panelCenter.x + (panelWidth / 2 - (SCALE * FIDUCIAL_OFFSET + SCALE * VERTICAL_EDGE_RAIL_WIDTH))),
                    int(panelCenter.y - (panelHeight / 2 - HORIZONTAL_EDGE_RAIL_WIDTH / 2 * SCALE))
                ])
                fiducials.append([
                    int(panelCenter.x - (panelWidth / 2 - (SCALE * FIDUCIAL_OFFSET + SCALE * VERTICAL_EDGE_RAIL_WIDTH))),
                    int(panelCenter.y - (panelHeight / 2 - HORIZONTAL_EDGE_RAIL_WIDTH / 2 * SCALE))
                ])
            for pos in fiducials:
                # Front / Top
                fiducial = pcbnew.FootprintLoad(fiducialPath, FIDUCIAL_FOOTPRINT)
                fiducial.SetReference("") # Clear the reference silk
                fiducial.SetValue("")
                board.Add(fiducial)
                fiducial.SetPosition(pcbnew.VECTOR2I(pos[0], pos[1]))

                # Back / Bottom
                fiducial = pcbnew.FootprintLoad(fiducialPath, FIDUCIAL_FOOTPRINT)
                fiducial.SetReference("") # Clear the reference silk
                fiducial.SetValue("")
                board.Add(fiducial)
                fiducial.SetPosition(pcbnew.VECTOR2I(pos[0], pos[1]))
                fiducial.Flip(pcbnew.VECTOR2I(pos[0], pos[1]), False)

        # Add text to rail
        if HORIZONTAL_EDGE_RAIL_TEXT: # Add text to bottom rail
            hrail_text = pcbnew.PCB_TEXT(board)
            hrail_text.SetText(HORIZONTAL_EDGE_RAIL_TEXT)
            hrail_text.SetTextSize(pcbnew.VECTOR2I(int(SCALE * RAIL_TEXT_SIZE), int(SCALE * RAIL_TEXT_SIZE)))
            hrail_text.SetLayer(pcbnew.F_SilkS)
            hrail_text.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_LEFT)
            hrail_text.SetPosition(
                pcbnew.VECTOR2I(
                    int(panelCenter.x - (panelWidth / 2 - VERTICAL_EDGE_RAIL_WIDTH * SCALE - SCALE * FIDUCIAL_OFFSET * 2)),
                    int(panelCenter.y + (panelHeight / 2 - HORIZONTAL_EDGE_RAIL_WIDTH / 2 * SCALE))
                )
            )
            board.Add(hrail_text)

        if VERTICAL_EDGE_RAIL_TEXT: # Add text to left rail
            vrail_text = pcbnew.PCB_TEXT(board)
            vrail_text.SetText(VERTICAL_EDGE_RAIL_TEXT)
            vrail_text.SetTextSize(pcbnew.VECTOR2I(int(SCALE * RAIL_TEXT_SIZE), int(SCALE * RAIL_TEXT_SIZE)))
            vrail_text.SetLayer(pcbnew.F_SilkS)
            vrail_text.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_LEFT)
            vrail_text.SetPosition(
                pcbnew.VECTOR2I(
                    int(panelCenter.x - (panelWidth / 2 - VERTICAL_EDGE_RAIL_WIDTH / 2 * SCALE)),
                    int(panelCenter.y - (panelHeight / 2 - HORIZONTAL_EDGE_RAIL_WIDTH * SCALE - SCALE * FIDUCIAL_OFFSET * 2))
                )
            )
            vrail_text.SetTextAngle(pcbnew.EDA_ANGLE(-900, pcbnew.TENTHS_OF_A_DEGREE_T))  # rotate if on vrail
            board.Add(vrail_text)

        # Add title text to rail
        TITLE_TEXT = ""
        if board.GetTitleBlock().GetTitle():
            TITLE_TEXT += str(board.GetTitleBlock().GetTitle())

        if board.GetTitleBlock().GetRevision():
            TITLE_TEXT += " Rev. " + str(board.GetTitleBlock().GetRevision())

        if board.GetTitleBlock().GetDate():
            TITLE_TEXT += ", " + str(board.GetTitleBlock().GetDate())

        if board.GetTitleBlock().GetCompany():
            TITLE_TEXT += " (c) " + str(board.GetTitleBlock().GetCompany())

        if TITLE_TEXT == "":
            TITLE_TEXT = os.path.split(panelOutputFile)[1] # Default to the panel filename

        if TITLE_X: # Add text to top rail
            titleblock_text = pcbnew.PCB_TEXT(board)
            titleblock_text.SetText(TITLE_TEXT)
            titleblock_text.SetTextSize(pcbnew.VECTOR2I(int(SCALE * RAIL_TEXT_SIZE), int(SCALE * RAIL_TEXT_SIZE)))
            titleblock_text.SetLayer(pcbnew.F_SilkS)
            titleblock_text.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_LEFT)
            titleblock_text.SetPosition(
                pcbnew.VECTOR2I(
                    int(panelCenter.x - (panelWidth / 2 - VERTICAL_EDGE_RAIL_WIDTH * SCALE - SCALE * FIDUCIAL_OFFSET * 2)),
                    int(panelCenter.y - (panelHeight / 2 - HORIZONTAL_EDGE_RAIL_WIDTH / 2 * SCALE))
                )
            )
            board.Add(titleblock_text)

        if TITLE_Y: # Add text to right rail
            titleblock_text = pcbnew.PCB_TEXT(board)
            titleblock_text.SetText(TITLE_TEXT)
            titleblock_text.SetTextSize(pcbnew.VECTOR2I(int(SCALE * RAIL_TEXT_SIZE), int(SCALE * RAIL_TEXT_SIZE)))
            titleblock_text.SetLayer(pcbnew.F_SilkS)
            titleblock_text.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_LEFT)
            titleblock_text.SetPosition(
                pcbnew.VECTOR2I(
                    int(panelCenter.x + (panelWidth / 2 - VERTICAL_EDGE_RAIL_WIDTH / 2 * SCALE)),
                    int(panelCenter.y - (panelHeight / 2 - HORIZONTAL_EDGE_RAIL_WIDTH * SCALE - SCALE * FIDUCIAL_OFFSET * 2))
                )
            )
            titleblock_text.SetTextAngle(pcbnew.EDA_ANGLE(-900, pcbnew.TENTHS_OF_A_DEGREE_T))
            board.Add(titleblock_text)

        # Save output
        board.SetFileName(panelOutputFile)
        board.Save(panelOutputFile)

        # Warn if panel is under 70x70mm
        if panelWidth / SCALE < 70 or panelHeight / SCALE < 70:
            report += "Warning: panel is under 70x70mm. It may be too small to v-score.\n"
            sysExit = 1

        # Add ordering instructions:
        if not orderingInstructionsSeen:
            if wx.GetApp() is not None:
                resp = wx.MessageBox("Ordering Instructions not found!\nNo futher warnings will be given.",
                            'Warning', wx.OK | wx.ICON_WARNING)
            sysExit = 1

        if ordering is None:
            report += "\nOrdering Instructions:\n"
            report += (
                "Panel dimensions: "
                + "{:.2f} x ".format(panelWidth / SCALE)
                + "{:.2f} mm.\n".format(panelHeight / SCALE)
            )
            if controlledImpedance is not None:
                report += controlledImpedance + "\n"
            if material is not None:
                report += material + "\n"
            if solderMask is None:
                solderMask = "Solder Mask: Red"
            report += solderMask + "\n"
            if silkscreen is None:
                silkscreen = "Silkscreen: White"
            report += silkscreen + "\n"
            if numLayers is None:
                numLayers = "Layers: 2"
            report += numLayers + "\n"
            if finish is None:
                finish = "Finish: HASL Lead-free"
            report += finish + "\n"
            if thickness is None:
                thickness = "Thickness: 1.6mm"
            report += thickness + "\n"
            if copperWeight is None:
                copperWeight = "Copper weight: 1oz"
            report += copperWeight + "\n"
            report += "Minimum track width: {:.2f}mm ({:.2f}mil)\n".format(
                float(minTrackWidth) / SCALE, float(minTrackWidth) * 1000 / (SCALE * 25.4))
            report += "Minimum via drill: {:.2f}mm ({:.2f}mil)\n".format(
                float(minViaDrill) / SCALE, float(minViaDrill) * 1000 / (SCALE * 25.4))
            if orderingExtras is not None:
                report += orderingExtras
        else:
            try:
                with open(ordering, 'w') as oi:
                    oi.write("Ordering Instructions:\n")
                    oi.write(
                        "Panel dimensions: "
                        + "{:.2f} x ".format(panelWidth / SCALE)
                        + "{:.2f} mm.\n".format(panelHeight / SCALE)
                    )
                    if controlledImpedance is not None:
                        oi.write(controlledImpedance + "\n")
                    if material is not None:
                        oi.write(material + "\n")
                    if solderMask is None:
                        if wx.GetApp() is not None and orderingInstructionsSeen:
                            resp = wx.MessageBox("Solder mask color not found!",
                                        'Warning', wx.OK | wx.ICON_WARNING)
                        solderMask = "Solder Mask: Red"
                    oi.write(solderMask + "\n")
                    if silkscreen is None:
                        if wx.GetApp() is not None and orderingInstructionsSeen:
                            resp = wx.MessageBox("Silkscreen color not found!",
                                        'Warning', wx.OK | wx.ICON_WARNING)
                        silkscreen = "Silkscreen: White"
                    oi.write(silkscreen + "\n")
                    if numLayers is None:
                        if wx.GetApp() is not None and orderingInstructionsSeen:
                            resp = wx.MessageBox("Number of layers not found!",
                                        'Warning', wx.OK | wx.ICON_WARNING)
                        numLayers = "Layers: 2"
                    oi.write(numLayers + "\n")
                    if finish is None:
                        if wx.GetApp() is not None and orderingInstructionsSeen:
                            resp = wx.MessageBox("PCB finish not found!",
                                        'Warning', wx.OK | wx.ICON_WARNING)
                        finish = "Finish: HASL Lead-free"
                    oi.write(finish + "\n")
                    if thickness is None:
                        if wx.GetApp() is not None and orderingInstructionsSeen:
                            resp = wx.MessageBox("PCB thickness not found!",
                                        'Warning', wx.OK | wx.ICON_WARNING)
                        thickness = "Thickness: 1.6mm"
                    oi.write(thickness + "\n")
                    if copperWeight is None:
                        if wx.GetApp() is not None and orderingInstructionsSeen:
                            resp = wx.MessageBox("Copper weight not found!",
                                        'Warning', wx.OK | wx.ICON_WARNING)
                        copperWeight = "Copper weight: 1oz"
                    oi.write(copperWeight + "\n")
                    oi.write("Minimum track width: {:.2f}mm ({:.2f}mil)\n".format(
                        float(minTrackWidth) / SCALE, float(minTrackWidth) * 1000 / (SCALE * 25.4)))
                    oi.write("Minimum via drill: {:.2f}mm ({:.2f}mil)\n".format(
                        float(minViaDrill) / SCALE, float(minViaDrill) * 1000 / (SCALE * 25.4)))
                    if orderingExtras is not None:
                        oi.write(orderingExtras)
            except Exception as e:
                # Don't throw exception if we can't save ordering instructions
                pass

        if (prodIDs is not None):
            emptyProdIDs = {}
            for prodID in prodIDs:
                if (prodID[0] == '') or (prodID[0] == ' '):
                    if prodID[1] not in emptyProdIDs:
                        emptyProdIDs[prodID[1]] = 1
                    else:
                        emptyProdIDs[prodID[1]] = emptyProdIDs[prodID[1]] + 1
            if wx.GetApp() is not None and orderingInstructionsSeen and emptyProdIDs:
                refs = ""
                for keys, value in emptyProdIDs.items():
                    if refs == "":
                        refs += keys
                    else:
                        refs += "," + keys
                resp = wx.MessageBox("Empty (undefined) PROD_IDs found!\n" + refs,
                            'Warning', wx.OK | wx.ICON_WARNING)
                sysExit = 1

        if sysExit < 0:
            sysExit = 0

        return sysExit, report

    def startPanelizerCommand(self, command, board=None, ordering=None, logger=None):

        parser = self.args_parse(command)

        sysExit, report = self.startPanelizer(parser, board, ordering, logger)

        return sysExit, report

if __name__ == '__main__':

    panelizer = Panelizer()

    if len(sys.argv) < 2:
        parser = panelizer.args_parse(['-h']) # Test args: e.g. ['-p','<path to board>','--numx','3','--numy','3']
    else:
        parser = panelizer.args_parse(sys.argv[1:]) #Parse the args

    sysExit, report = panelizer.startPanelizer(parser)

    print(report)

    sys.exit(sysExit)
