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
import wx.grid

import gettext
_ = gettext.gettext

###########################################################################
## Class DialogPanelBase
###########################################################################

class DialogPanelBase ( DialogShim ):

    def __init__( self, parent ):
        DialogShim.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"SparkFun KiCad Panelizer"), pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP|wx.BORDER_DEFAULT )

        self.SetSizeHints( wx.Size( -1,-1 ), wx.DefaultSize )


        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_INIT_DIALOG, self.OnInitDlg )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def OnInitDlg( self, event ):
        pass


###########################################################################
## Class DialogPanel
###########################################################################

class DialogPanel ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        bSizer7 = wx.BoxSizer( wx.VERTICAL )

        self.notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_TOP|wx.BORDER_DEFAULT )
        self.notebook.SetMinSize( wx.Size( 350,450 ) )


        bSizer7.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 5 )

        lowerSizer = wx.BoxSizer( wx.HORIZONTAL )


        lowerSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_buttonPanelize = wx.Button( self, wx.ID_ANY, _(u"Panelize"), wx.DefaultPosition, wx.DefaultSize, 0 )

        self.m_buttonPanelize.SetDefault()
        lowerSizer.Add( self.m_buttonPanelize, 0, wx.ALL, 5 )

        self.m_buttonCancel = wx.Button( self, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        lowerSizer.Add( self.m_buttonCancel, 0, wx.ALL, 5 )


        bSizer7.Add( lowerSizer, 0, wx.EXPAND, 5 )


        self.SetSizer( bSizer7 )
        self.Layout()
        bSizer7.Fit( self )

        # Connect Events
        self.m_buttonPanelize.Bind( wx.EVT_BUTTON, self.OnPanelizeClick )
        self.m_buttonCancel.Bind( wx.EVT_BUTTON, self.OnCancelClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def OnPanelizeClick( self, event ):
        pass

    def OnCancelClick( self, event ):
        pass


###########################################################################
## Class GeneralPanelBase
###########################################################################

class GeneralPanelBase ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        bMainSizer = wx.BoxSizer( wx.VERTICAL )

        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Dimensions:") ), wx.VERTICAL )

        self.m_dimensionsInchesBtn = wx.RadioButton( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"Inches"), wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
        sbSizer1.Add( self.m_dimensionsInchesBtn, 0, wx.ALL, 5 )

        self.m_dimensionsMmBtn = wx.RadioButton( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"Millimeters"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer1.Add( self.m_dimensionsMmBtn, 0, wx.ALL, 5 )


        bMainSizer.Add( sbSizer1, 0, wx.ALL|wx.EXPAND, 5 )

        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Panel Size:") ), wx.VERTICAL )

        self.m_panelSizeSmallerBtn = wx.RadioButton( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Must be smaller than"), wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
        sbSizer2.Add( self.m_panelSizeSmallerBtn, 0, wx.ALL, 5 )

        self.m_panelSizeLargerBtn = wx.RadioButton( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Must be larger than"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer2.Add( self.m_panelSizeLargerBtn, 0, wx.ALL, 5 )

        fgSizerPanelSize = wx.FlexGridSizer( 0, 2, 4, 4 )
        fgSizerPanelSize.SetFlexibleDirection( wx.BOTH )
        fgSizerPanelSize.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_panelSizeXLabel = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"X:  "), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
        self.m_panelSizeXLabel.Wrap( -1 )

        fgSizerPanelSize.Add( self.m_panelSizeXLabel, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_panelSizeXCtrl = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self.m_panelSizeXCtrl.SetMaxLength( 0 )
        self.m_panelSizeXCtrl.SetMinSize( wx.Size( 64,-1 ) )

        fgSizerPanelSize.Add( self.m_panelSizeXCtrl, 1, wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_panelSizeYLabel = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Y:  "), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
        self.m_panelSizeYLabel.Wrap( -1 )

        fgSizerPanelSize.Add( self.m_panelSizeYLabel, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_panelSizeYCtrl = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self.m_panelSizeYCtrl.SetMaxLength( 0 )
        self.m_panelSizeYCtrl.SetMinSize( wx.Size( 64,-1 ) )

        fgSizerPanelSize.Add( self.m_panelSizeYCtrl, 1, wx.ALIGN_CENTER_VERTICAL, 5 )


        sbSizer2.Add( fgSizerPanelSize, 1, wx.ALL, 5 )


        bMainSizer.Add( sbSizer2, 0, wx.EXPAND, 5 )

        sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Gaps:") ), wx.VERTICAL )

        fgSizerGaps = wx.FlexGridSizer( 0, 2, 4, 4 )
        fgSizerGaps.SetFlexibleDirection( wx.BOTH )
        fgSizerGaps.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_gapsVerticalLabel = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Vertical Gap (X):"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
        self.m_gapsVerticalLabel.Wrap( -1 )

        fgSizerGaps.Add( self.m_gapsVerticalLabel, 1, wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_gapsVerticalCtrl = wx.TextCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self.m_gapsVerticalCtrl.SetMaxLength( 0 )
        self.m_gapsVerticalCtrl.SetMinSize( wx.Size( 64,-1 ) )

        fgSizerGaps.Add( self.m_gapsVerticalCtrl, 1, wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_gapsHorizontalLabel = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Horizontal Gap (Y):"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
        self.m_gapsHorizontalLabel.Wrap( -1 )

        fgSizerGaps.Add( self.m_gapsHorizontalLabel, 1, wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_gapsHorizontalCtrl = wx.TextCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self.m_gapsHorizontalCtrl.SetMaxLength( 0 )
        self.m_gapsHorizontalCtrl.SetMinSize( wx.Size( 64,-1 ) )

        fgSizerGaps.Add( self.m_gapsHorizontalCtrl, 1, wx.ALIGN_CENTER_VERTICAL, 5 )


        sbSizer3.Add( fgSizerGaps, 0, wx.ALL, 10 )

        self.m_removeRightVerticalCheck = wx.CheckBox( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Remove right-most vertical gap and use v-score instead"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer3.Add( self.m_removeRightVerticalCheck, 0, wx.ALL, 5 )


        bMainSizer.Add( sbSizer3, 0, wx.EXPAND, 5 )

        sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Extra Production Bits:") ), wx.VERTICAL )

        self.m_productionBordersCheck = wx.CheckBox( sbSizer4.GetStaticBox(), wx.ID_ANY, _(u"Add Panel Borders and Fiducials"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer4.Add( self.m_productionBordersCheck, 0, wx.ALL, 5 )

        fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer3.SetFlexibleDirection( wx.BOTH )
        fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_productionFiducialsCheck = wx.CheckBox( sbSizer4.GetStaticBox(), wx.ID_ANY, _(u"Move Panel Fiducials to Left+Right Edges"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer3.Add( self.m_productionFiducialsCheck, 0, wx.ALL, 5 )

        self.m_buttonFiducialsHelp = wx.Button( sbSizer4.GetStaticBox(), wx.ID_ANY, _(u"MyButton"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_buttonFiducialsHelp.SetMinSize( wx.Size( 15,15 ) )

        fgSizer3.Add( self.m_buttonFiducialsHelp, 0, wx.ALL, 5 )


        sbSizer4.Add( fgSizer3, 1, wx.EXPAND, 5 )

        fgSizer5 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer5.SetFlexibleDirection( wx.BOTH )
        fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_productionExposeCheck = wx.CheckBox( sbSizer4.GetStaticBox(), wx.ID_ANY, _(u"Expose Bottom/Card Edge"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer5.Add( self.m_productionExposeCheck, 0, wx.ALL, 5 )

        self.m_buttonEdgeHelp = wx.Button( sbSizer4.GetStaticBox(), wx.ID_ANY, _(u"MyButton"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_buttonEdgeHelp.SetMinSize( wx.Size( 15,15 ) )

        fgSizer5.Add( self.m_buttonEdgeHelp, 0, wx.ALL, 5 )


        sbSizer4.Add( fgSizer5, 1, wx.EXPAND, 5 )


        bMainSizer.Add( sbSizer4, 0, wx.EXPAND, 5 )


        self.SetSizer( bMainSizer )
        self.Layout()
        bMainSizer.Fit( self )

        # Connect Events
        self.m_buttonFiducialsHelp.Bind( wx.EVT_BUTTON, self.ClickFiducialsHelp )
        self.m_buttonEdgeHelp.Bind( wx.EVT_BUTTON, self.ClickEdgeHelp )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def ClickFiducialsHelp( self, event ):
        pass

    def ClickEdgeHelp( self, event ):
        pass


###########################################################################
## Class VScorePanelBase
###########################################################################

class VScorePanelBase ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        bSizer11 = wx.BoxSizer( wx.VERTICAL )

        sbSizer5 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"V-Score Layer:") ), wx.VERTICAL )

        LayersGridSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        LayersGridSizer.SetFlexibleDirection( wx.BOTH )
        LayersGridSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.LayersGrid = wx.grid.Grid( sbSizer5.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

        # Grid
        self.LayersGrid.CreateGrid( 1, 2 )
        self.LayersGrid.EnableEditing( True )
        self.LayersGrid.EnableGridLines( True )
        self.LayersGrid.EnableDragGridSize( False )
        self.LayersGrid.SetMargins( 0, 0 )

        # Columns
        self.LayersGrid.AutoSizeColumns()
        self.LayersGrid.EnableDragColMove( False )
        self.LayersGrid.EnableDragColSize( True )
        self.LayersGrid.SetColLabelValue( 0, _(u"Use") )
        self.LayersGrid.SetColLabelValue( 1, _(u"Layer") )
        self.LayersGrid.SetColLabelSize( 30 )
        self.LayersGrid.SetColLabelAlignment( wx.ALIGN_LEFT, wx.ALIGN_CENTER )

        # Rows
        self.LayersGrid.AutoSizeRows()
        self.LayersGrid.EnableDragRowSize( False )
        self.LayersGrid.SetRowLabelSize( 1 )
        self.LayersGrid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Label Appearance

        # Cell Defaults
        self.LayersGrid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        LayersGridSizer.Add( self.LayersGrid, 0, wx.ALL|wx.EXPAND, 5 )


        sbSizer5.Add( LayersGridSizer, 1, wx.EXPAND, 5 )


        bSizer11.Add( sbSizer5, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer11 )
        self.Layout()
        bSizer11.Fit( self )

        # Connect Events
        self.LayersGrid.Bind( wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnLayersGridCellClicked )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def OnLayersGridCellClicked( self, event ):
        pass


