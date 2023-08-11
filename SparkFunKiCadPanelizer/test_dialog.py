#!/usr/bin/env python
from dialog.dialog import *

import sys
import subprocess

from panelizer.panelizer import Panelizer

class MyApp(wx.App):
    def OnInit(self):

        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'panel_config.json')
        ordering_instructions = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ordering_instructions.txt')

        self.frame = frame = Dialog(None, config_file, ordering_instructions, Panelizer(), self.run)
        if frame.ShowModal() == wx.ID_OK:
            print("Graceful Exit")
        frame.Destroy()
        return True

    def run(self, dlg, p_panelizer):

        self.frame.EndModal(wx.ID_OK)


app = MyApp()
app.MainLoop()

print("Done")