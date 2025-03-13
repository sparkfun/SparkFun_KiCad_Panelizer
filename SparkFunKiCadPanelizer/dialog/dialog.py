"""Subclass of dialog_text_base, which is generated by wxFormBuilder."""
from logging import exception
import os
import wx
import json
import sys

from . import dialog_text_base

_APP_NAME = "SparkFun KiCad Panelizer"

# sub folder for our resource files
_RESOURCE_DIRECTORY = os.path.join("..", "resource")

#https://stackoverflow.com/a/50914550
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, _RESOURCE_DIRECTORY, relative_path)

def get_version(rel_path: str) -> str:
    try: 
        with open(resource_path(rel_path), encoding='utf-8') as fp:
            for line in fp.read().splitlines():
                if line.startswith("__version__"):
                    delim = '"' if '"' in line else "'"
                    return line.split(delim)[1]
            raise RuntimeError("Unable to find version string.")
    except:
        raise RuntimeError("Unable to find _version.py.")

_APP_VERSION = get_version("_version.py")

def get_btn_bitmap(bitmap):
    path = resource_path(bitmap)
    png = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
    return wx.BitmapBundle(png)

def ParseFloat(InputString, DefaultValue=0.0):
    value = DefaultValue
    if InputString != "":
        try:
            value = float(InputString)
        except ValueError:
            print("Value not valid")
    return value

class Dialog(dialog_text_base.DialogPanelBase):
    def __init__(self, parent, config, layertable, ordering, panelizer, func):

        dialog_text_base.DialogPanelBase.__init__(self, None)

        self.panel = DialogPanel(self, config, layertable, ordering, panelizer, func)

        best_size = self.panel.BestSize
        # hack for some gtk themes that incorrectly calculate best size
        best_size.IncBy(dx=0, dy=30)
        self.SetClientSize(best_size)

        self.SetTitle(_APP_NAME + " - " + _APP_VERSION)

    # hack for new wxFormBuilder generating code incompatible with old wxPython
    # noinspection PyMethodOverriding
    def SetSizeHints(self, sz1, sz2):
        try:
            # wxPython 4
            super(Dialog, self).SetSizeHints(sz1, sz2)
        except TypeError:
            # wxPython 3
            self.SetSizeHintsSz(sz1, sz2)

class DialogPanel(dialog_text_base.DialogPanel):
    # The names of the config items need to match the names in dialog_text_base minus the m_
    # - except for vScoreLayer
    vscore_layer = 'vScoreLayer'
    default_vscore_layer = 'User.Comments'
    config_defaults = {
        'dimensionsInchesBtn': 'true',
        'dimensionsMmBtn': 'false',
        'panelSizeSmallerBtn': 'true',
        'panelSizeLargerBtn': 'false',
        'panelSizeXCtrl': '5.5',
        'panelSizeYCtrl': '7.5',
        'gapsVerticalCtrl': '0.0',
        'gapsHorizontalCtrl': '0.0',
        'removeRightVerticalCheck': 'false',
        'productionBordersCheck': 'false',
        'productionFiducialsCheck': 'false',
        'productionExposeCheck': 'false',
        vscore_layer: default_vscore_layer
    }

    def __init__(self, parent, config, layertable, ordering, panelizer, func):

        dialog_text_base.DialogPanel.__init__(self, parent)
        
        self.config_file = config

        self.layertable = layertable

        self.ordering_instructions = ordering

        self.panelizer = panelizer

        self.func = func

        self.error = None

        self.general = GeneralPanel(self.notebook)
        self.vscore = VScorePanel(self.notebook)
        self.notebook.AddPage(self.general, "General")
        self.notebook.AddPage(self.vscore, "V-Score")

        # Delete any existing rows in LayersGrid
        if self.vscore.LayersGrid.NumberRows:
            self.vscore.LayersGrid.DeleteRows(0, self.vscore.LayersGrid.NumberRows)
        # Append empty rows based on layertable
        self.vscore.LayersGrid.AppendRows(len(self.layertable))
        # Initialize them
        row = 0
        for layer, names in self.layertable.items():
            self.vscore.LayersGrid.SetCellValue(row, 0, "0") # JSON style
            self.vscore.LayersGrid.SetCellRenderer(row, 0, wx.grid.GridCellBoolRenderer())
            layerName = names['standardName']
            if names['actualName'] != names['standardName']:
                layerName += " (" + names['actualName'] + ")"
            self.vscore.LayersGrid.SetCellValue(row, 1, layerName)
            self.vscore.LayersGrid.SetReadOnly(row, 1)
            row += 1

        self.loadConfig()

    def loadConfig(self):
        # Load up last sessions config
        params = self.config_defaults
        try:
            with open(self.config_file, 'r') as cf:
                json_params = json.load(cf)
            params.update(json_params)
        except Exception as e:
            # Don't throw exception if we can't load previous config
            pass

        self.LoadSettings(params)
        
    def saveConfig(self):
        try:
            with open(self.config_file, 'w') as cf:
                json.dump(self.CurrentSettings(), cf, indent=2)
        except Exception as e:
            # Don't throw exception if we can't save config
            pass
            
    def LoadSettings(self, params):
        for key,value in params.items():
            if key not in self.config_defaults.keys():
                continue
            if value is None:
                continue

            if self.vscore_layer in key:
                defaultLayerFound = False
                for row in range(self.vscore.LayersGrid.GetNumberRows()):
                    if value in self.vscore.LayersGrid.GetCellValue(row, 1):
                        b = "1"
                        defaultLayerFound = True
                    else:
                        b = "0"
                    self.vscore.LayersGrid.SetCellValue(row, 0, b)
                if not defaultLayerFound:
                    self.vscore.LayersGrid.SetCellValue(0, 0, "1") # Default to the first layer
            else:
                try:
                    obj = getattr(self.general, "m_{}".format(key))
                    if hasattr(obj, "SetValue"):
                        obj.SetValue(value)
                    elif hasattr(obj, "SetStringSelection"):
                        obj.SetStringSelection(value)
                    else:
                        raise Exception("Invalid item")  
                except Exception as e:
                    pass 

        return params

    def CurrentSettings(self):
        params = {}

        for item in self.config_defaults.keys():
            if self.vscore_layer in item:
                for row in range(self.vscore.LayersGrid.GetNumberRows()):
                    if self.vscore.LayersGrid.GetCellValue(row, 0) == "1":
                        layername = self.vscore.LayersGrid.GetCellValue(row, 1)
                        if " (" in layername:
                            layername = layername[:layername.find(" (")] # Trim the actual name - if present
                        params.update({self.vscore_layer: layername})
            else:
                obj = getattr(self.general, "m_{}".format(item))
                if hasattr(obj, "GetValue"):
                    params.update({item: obj.GetValue()})
                elif hasattr(obj, "GetStringSelection"):
                    params.update({item: obj.GetStringSelection()})
                else:
                    raise Exception("Invalid item")    
        
        return params

    def OnPanelizeClick(self, e):
        self.saveConfig()
        self.func(self, self.panelizer)

    def OnCancelClick(self, e):
        self.GetParent().EndModal(wx.ID_CANCEL)     

class GeneralPanel(dialog_text_base.GeneralPanelBase):

    def __init__(self, parent):
        dialog_text_base.GeneralPanelBase.__init__(self, parent)

        self.m_buttonGapsVerticalHelp.SetLabelText("")
        # Icon by Icons8 https://icons8.com : https://icons8.com/icon/63308/info
        self.m_buttonGapsVerticalHelp.SetBitmap(get_btn_bitmap("info-15.png"))

        self.m_buttonGapsHorizontalHelp.SetLabelText("")
        # Icon by Icons8 https://icons8.com : https://icons8.com/icon/63308/info
        self.m_buttonGapsHorizontalHelp.SetBitmap(get_btn_bitmap("info-15.png"))

        self.m_buttonFiducialsHelp.SetLabelText("")
        # Icon by Icons8 https://icons8.com : https://icons8.com/icon/63308/info
        self.m_buttonFiducialsHelp.SetBitmap(get_btn_bitmap("info-15.png"))

        self.m_buttonEdgeHelp.SetLabelText("")
        # Icon by Icons8 https://icons8.com : https://icons8.com/icon/63308/info
        self.m_buttonEdgeHelp.SetBitmap(get_btn_bitmap("info-15.png"))

    def ClickGapsVerticalHelp( self, event ):
        wx.MessageBox("\
This sets the width of the vertical gaps\n\
within the panel. Vertical gaps run from\n\
the bottom rail to the top rail. The width\n\
is defined in X.\n\
\n\
The gap width should be at least 0.3\" to\n\
aid automated inspection.\
", 'Info', wx.OK | wx.ICON_INFORMATION)

    def ClickGapsHorizontalHelp( self, event ):
        wx.MessageBox("\
This sets the width of the horizontal gaps\n\
within the panel. Horizontal gaps run from\n\
the left rail to the right rail. The width\n\
is defined in Y.\n\
\n\
The gap width should be at least 0.3\" to\n\
aid automated inspection.\
", 'Info', wx.OK | wx.ICON_INFORMATION)

    def ClickFiducialsHelp( self, event ):
        wx.MessageBox("\
By default, the panel fiducials are placed in\n\
the top and bottom edges. Normally we\n\
recommend leaving them there.\n\
\n\
Selecting this option moves them to the left\n\
and right edges.\n\
\n\
This can be useful when using horizontal gaps\n\
and vertical v-scores. It avoids the panel\n\
having to be scrapped if an edge has been\n\
snapped off and the fiducials are missing.\
", 'Info', wx.OK | wx.ICON_INFORMATION)

    def ClickEdgeHelp( self, event ):
        wx.MessageBox("\
Select this option if you are panelizing\n\
a MicroMod Processor or Function Board.\n\
\n\
The bottom and top edges will be exposed\n\
so the fingers and chamfered edge can be\n\
manufactured. The top row of PCBs is\n\
rotated automatically.\
", 'Info', wx.OK | wx.ICON_INFORMATION)

class VScorePanel(dialog_text_base.VScorePanelBase):

    def __init__(self, parent):
        dialog_text_base.VScorePanelBase.__init__(self, parent)

        self.Layout()
        self.LayersGrid.SetColSize(0, 50)
        self.LayersGrid.SetColSize(1, self.GetParent().GetClientSize().x - 80)

    def OnLayersGridCellClicked(self, event):
        self.LayersGrid.ClearSelection()
        #self.LayersGrid.SelectRow(event.Row)
        if event.Col == 0:
            for row in range(self.LayersGrid.GetNumberRows()):
                val = "1" if (row == event.Row) else "0" # JSON style
                self.LayersGrid.SetCellValue(row, 0, val)

