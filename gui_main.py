# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1089,735 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		gbSizer1 = wx.GridBagSizer( 0, 0 )
		gbSizer1.SetFlexibleDirection( wx.BOTH )
		gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_button8 = wx.Button( self, wx.ID_ANY, u"Load file", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.m_button8, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button2 = wx.Button( self, wx.ID_ANY, u"- row", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.m_button2, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button7 = wx.Button( self, wx.ID_ANY, u"Save results", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.m_button7, wx.GBPosition( 1, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button3 = wx.Button( self, wx.ID_ANY, u"Run least squares", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.m_button3, wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button1 = wx.Button( self, wx.ID_ANY, u"+ row", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.m_button1, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_grid3 = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_grid3.CreateGrid( 30, 4 )
		self.m_grid3.EnableEditing( True )
		self.m_grid3.EnableGridLines( True )
		self.m_grid3.EnableDragGridSize( False )
		self.m_grid3.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid3.SetColSize( 0, 67 )
		self.m_grid3.SetColSize( 1, 119 )
		self.m_grid3.SetColSize( 2, 113 )
		self.m_grid3.SetColSize( 3, 80 )
		self.m_grid3.EnableDragColMove( False )
		self.m_grid3.EnableDragColSize( True )
		self.m_grid3.SetColLabelSize( 30 )
		self.m_grid3.SetColLabelValue( 0, u"Name" )
		self.m_grid3.SetColLabelValue( 1, u"Value (g)" )
		self.m_grid3.SetColLabelValue( 2, u"Uncert (ug)" )
		self.m_grid3.SetColLabelValue( 3, u"95% cl (ug)" )
		self.m_grid3.SetColLabelValue( 4, wx.EmptyString )
		self.m_grid3.SetColLabelValue( 5, wx.EmptyString )
		self.m_grid3.SetColLabelValue( 6, wx.EmptyString )
		self.m_grid3.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid3.EnableDragRowSize( True )
		self.m_grid3.SetRowLabelSize( 80 )
		self.m_grid3.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid3.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		gbSizer1.Add( self.m_grid3, wx.GBPosition( 2, 6 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_grid1 = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_grid1.CreateGrid( 30, 4 )
		self.m_grid1.EnableEditing( True )
		self.m_grid1.EnableGridLines( True )
		self.m_grid1.EnableDragGridSize( False )
		self.m_grid1.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid1.SetColSize( 0, 120 )
		self.m_grid1.SetColSize( 1, 120 )
		self.m_grid1.SetColSize( 2, 120 )
		self.m_grid1.SetColSize( 3, 120 )
		self.m_grid1.EnableDragColMove( False )
		self.m_grid1.EnableDragColSize( True )
		self.m_grid1.SetColLabelSize( 30 )
		self.m_grid1.SetColLabelValue( 0, u"Masses" )
		self.m_grid1.SetColLabelValue( 1, u"Difference (g)" )
		self.m_grid1.SetColLabelValue( 2, u"Uncert (ug)" )
		self.m_grid1.SetColLabelValue( 3, u"Residual (ug)" )
		self.m_grid1.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid1.EnableDragRowSize( True )
		self.m_grid1.SetRowLabelSize( 80 )
		self.m_grid1.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		gbSizer1.Add( self.m_grid1, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 6 ), wx.ALL, 5 )
		
		
		self.SetSizer( gbSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button8.Bind( wx.EVT_BUTTON, self.on_load_file )
		self.m_button2.Bind( wx.EVT_BUTTON, self.on_minus_row )
		self.m_button7.Bind( wx.EVT_BUTTON, self.on_save_results )
		self.m_button3.Bind( wx.EVT_BUTTON, self.on_run )
		self.m_button1.Bind( wx.EVT_BUTTON, self.on_plus_row )
		self.m_grid1.Bind( wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.on_row_options )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_load_file( self, event ):
		event.Skip()
	
	def on_minus_row( self, event ):
		event.Skip()
	
	def on_save_results( self, event ):
		event.Skip()
	
	def on_run( self, event ):
		event.Skip()
	
	def on_plus_row( self, event ):
		event.Skip()
	
	def on_row_options( self, event ):
		event.Skip()
	

