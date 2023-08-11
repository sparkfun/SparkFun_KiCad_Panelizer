# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from .compat import DialogShim
import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class DIALOG_TEXT_BASE
###########################################################################

class DIALOG_TEXT_BASE ( DialogShim ):

    def __init__( self, parent ):
        DialogShim.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"SparkFun KiCad Panelizer"), pos = wx.DefaultPosition, size = wx.Size( 345,610 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.SYSTEM_MENU )

        self.SetSizeHints( wx.Size( 345,610 ), wx.DefaultSize )

        bMainSizer = wx.BoxSizer( wx.VERTICAL )

        bSizer6 = wx.BoxSizer( wx.VERTICAL )

        self.m_dimensionsLabel = wx.StaticText( self, wx.ID_ANY, _(u"Dimensions:"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
        self.m_dimensionsLabel.Wrap( -1 )

        self.m_dimensionsLabel.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer6.Add( self.m_dimensionsLabel, 0, wx.ALIGN_LEFT|wx.ALL, 5 )

        self.m_dimensionsInchesBtn = wx.RadioButton( self, wx.ID_ANY, _(u"Inches"), wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
        bSizer6.Add( self.m_dimensionsInchesBtn, 0, wx.ALL, 5 )

        self.m_dimensionsMmBtn = wx.RadioButton( self, wx.ID_ANY, _(u"Millimeters"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_dimensionsMmBtn, 0, wx.ALL, 5 )


        bMainSizer.Add( bSizer6, 1, wx.ALL|wx.FIXED_MINSIZE, 5 )

        self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bMainSizer.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        self.m_panelSizeLabel = wx.StaticText( self, wx.ID_ANY, _(u"Panel Size:"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
        self.m_panelSizeLabel.Wrap( -1 )

        self.m_panelSizeLabel.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer8.Add( self.m_panelSizeLabel, 0, wx.ALIGN_LEFT|wx.ALL, 5 )

        self.m_panelSizeSmallerBtn = wx.RadioButton( self, wx.ID_ANY, _(u"Must be smaller than"), wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
        bSizer8.Add( self.m_panelSizeSmallerBtn, 0, wx.ALL, 5 )

        self.m_panelSizeLargerBtn = wx.RadioButton( self, wx.ID_ANY, _(u"Must be larger than"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.m_panelSizeLargerBtn, 0, wx.ALL, 5 )

        fgSizerPanelSize = wx.FlexGridSizer( 0, 2, 4, 4 )
        fgSizerPanelSize.SetFlexibleDirection( wx.BOTH )
        fgSizerPanelSize.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_panelSizeXLabel = wx.StaticText( self, wx.ID_ANY, _(u"X:  "), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
        self.m_panelSizeXLabel.Wrap( -1 )

        fgSizerPanelSize.Add( self.m_panelSizeXLabel, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_panelSizeXCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self.m_panelSizeXCtrl.SetMaxLength( 0 )
        self.m_panelSizeXCtrl.SetMinSize( wx.Size( 64,-1 ) )

        fgSizerPanelSize.Add( self.m_panelSizeXCtrl, 1, wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_panelSizeYLabel = wx.StaticText( self, wx.ID_ANY, _(u"Y:  "), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
        self.m_panelSizeYLabel.Wrap( -1 )

        fgSizerPanelSize.Add( self.m_panelSizeYLabel, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_panelSizeYCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self.m_panelSizeYCtrl.SetMaxLength( 0 )
        self.m_panelSizeYCtrl.SetMinSize( wx.Size( 64,-1 ) )

        fgSizerPanelSize.Add( self.m_panelSizeYCtrl, 1, wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer8.Add( fgSizerPanelSize, 1, wx.ALL, 5 )


        bMainSizer.Add( bSizer8, 1, wx.ALL|wx.FIXED_MINSIZE, 5 )

        self.m_staticline11 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bMainSizer.Add( self.m_staticline11, 0, wx.EXPAND |wx.ALL, 5 )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.m_GapsLabel = wx.StaticText( self, wx.ID_ANY, _(u"Gaps:"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
        self.m_GapsLabel.Wrap( -1 )

        self.m_GapsLabel.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer3.Add( self.m_GapsLabel, 0, wx.ALL, 5 )

        fgSizerGaps = wx.FlexGridSizer( 0, 2, 4, 4 )
        fgSizerGaps.SetFlexibleDirection( wx.BOTH )
        fgSizerGaps.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_gapsVerticalLabel = wx.StaticText( self, wx.ID_ANY, _(u"Vertical Gap (X):"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
        self.m_gapsVerticalLabel.Wrap( -1 )

        fgSizerGaps.Add( self.m_gapsVerticalLabel, 1, wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_gapsVerticalCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self.m_gapsVerticalCtrl.SetMaxLength( 0 )
        self.m_gapsVerticalCtrl.SetMinSize( wx.Size( 64,-1 ) )

        fgSizerGaps.Add( self.m_gapsVerticalCtrl, 1, wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_gapsHorizontalLabel = wx.StaticText( self, wx.ID_ANY, _(u"Horizontal Gap (Y):"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
        self.m_gapsHorizontalLabel.Wrap( -1 )

        fgSizerGaps.Add( self.m_gapsHorizontalLabel, 1, wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_gapsHorizontalCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self.m_gapsHorizontalCtrl.SetMaxLength( 0 )
        self.m_gapsHorizontalCtrl.SetMinSize( wx.Size( 64,-1 ) )

        fgSizerGaps.Add( self.m_gapsHorizontalCtrl, 1, wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer3.Add( fgSizerGaps, 0, wx.ALL, 10 )

        self.m_removeRightVerticalCheck = wx.CheckBox( self, wx.ID_ANY, _(u"Remove right-most vertical gap and use v-score instead"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.m_removeRightVerticalCheck, 0, wx.ALL, 5 )


        bMainSizer.Add( bSizer3, 1, wx.ALL|wx.FIXED_MINSIZE, 5 )

        self.m_staticline = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bMainSizer.Add( self.m_staticline, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 10 )

        bSizer9 = wx.BoxSizer( wx.VERTICAL )

        self.m_productionBitsLabel = wx.StaticText( self, wx.ID_ANY, _(u"Extra Production Bits:"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
        self.m_productionBitsLabel.Wrap( -1 )

        self.m_productionBitsLabel.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer9.Add( self.m_productionBitsLabel, 0, wx.ALL, 5 )

        self.m_productionBordersCheck = wx.CheckBox( self, wx.ID_ANY, _(u"Add Panel Borders and Fiducials"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.m_productionBordersCheck, 0, wx.ALL, 5 )

        self.m_productionFiducialsCheck = wx.CheckBox( self, wx.ID_ANY, _(u"Move Panel Fiducials to Left+Right Edges"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.m_productionFiducialsCheck, 0, wx.ALL, 5 )

        self.m_productionExposeCheck = wx.CheckBox( self, wx.ID_ANY, _(u"Expose Bottom/Card Edge"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.m_productionExposeCheck, 0, wx.ALL, 5 )


        bMainSizer.Add( bSizer9, 1, wx.ALL|wx.FIXED_MINSIZE, 5 )

        self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bMainSizer.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

        lowerSizer = wx.BoxSizer( wx.HORIZONTAL )


        lowerSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_buttonPanelize = wx.Button( self, wx.ID_ANY, _(u"Panelize"), wx.DefaultPosition, wx.DefaultSize, 0 )

        self.m_buttonPanelize.SetDefault()
        lowerSizer.Add( self.m_buttonPanelize, 0, wx.ALL, 5 )

        self.m_buttonCancel = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        lowerSizer.Add( self.m_buttonCancel, 0, wx.ALL, 5 )


        bMainSizer.Add( lowerSizer, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5 )


        self.SetSizer( bMainSizer )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_INIT_DIALOG, self.OnInitDlg )
        self.m_buttonPanelize.Bind( wx.EVT_BUTTON, self.OnPanelizeClick )
        self.m_buttonCancel.Bind( wx.EVT_BUTTON, self.OnCancelClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def OnInitDlg( self, event ):
        pass

    def OnPanelizeClick( self, event ):
        pass

    def OnCancelClick( self, event ):
        pass


