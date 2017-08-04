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
## Class MyFrame2
###########################################################################

class MyFrame2 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 907,418 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		gbSizer2 = wx.GridBagSizer( 0, 0 )
		gbSizer2.SetFlexibleDirection( wx.BOTH )
		gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_scrolledWindow1 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		self.m_scrolledWindow1.SetMinSize( wx.Size( 920,405 ) )
		
		gbSizer6 = wx.GridBagSizer( 0, 0 )
		gbSizer6.SetFlexibleDirection( wx.BOTH )
		gbSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_textCtrl6 = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer6.Add( self.m_textCtrl6, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Balance tolerance:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		gbSizer6.Add( self.m_staticText6, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_grid4 = wx.grid.Grid( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_grid4.CreateGrid( 6, 3 )
		self.m_grid4.EnableEditing( True )
		self.m_grid4.EnableGridLines( True )
		self.m_grid4.EnableDragGridSize( False )
		self.m_grid4.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid4.SetColSize( 0, 120 )
		self.m_grid4.SetColSize( 1, 120 )
		self.m_grid4.SetColSize( 2, 120 )
		self.m_grid4.EnableDragColMove( False )
		self.m_grid4.EnableDragColSize( True )
		self.m_grid4.SetColLabelSize( 30 )
		self.m_grid4.SetColLabelValue( 0, u"Item" )
		self.m_grid4.SetColLabelValue( 1, u"Value" )
		self.m_grid4.SetColLabelValue( 2, u"Uncert" )
		self.m_grid4.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid4.EnableDragRowSize( True )
		self.m_grid4.SetRowLabelSize( 80 )
		self.m_grid4.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid4.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		gbSizer6.Add( self.m_grid4, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 4 ), wx.ALL, 5 )
		
		self.m_grid2 = wx.grid.Grid( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_grid2.CreateGrid( 6, 10 )
		self.m_grid2.EnableEditing( True )
		self.m_grid2.EnableGridLines( True )
		self.m_grid2.EnableDragGridSize( False )
		self.m_grid2.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid2.EnableDragColMove( False )
		self.m_grid2.EnableDragColSize( True )
		self.m_grid2.SetColLabelSize( 30 )
		self.m_grid2.SetColLabelValue( 0, u"time" )
		self.m_grid2.SetColLabelValue( 1, u"Mass 1" )
		self.m_grid2.SetColLabelValue( 2, u"time" )
		self.m_grid2.SetColLabelValue( 3, u"Mass 2" )
		self.m_grid2.SetColLabelValue( 4, u"time" )
		self.m_grid2.SetColLabelValue( 5, u"Mass 3" )
		self.m_grid2.SetColLabelValue( 6, u"time" )
		self.m_grid2.SetColLabelValue( 7, u"Mass 4" )
		self.m_grid2.SetColLabelValue( 8, u"time" )
		self.m_grid2.SetColLabelValue( 9, u"Mass 5" )
		self.m_grid2.SetColLabelValue( 10, u"time" )
		self.m_grid2.SetColLabelValue( 11, u"Mass 6" )
		self.m_grid2.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid2.EnableDragRowSize( True )
		self.m_grid2.SetRowLabelSize( 80 )
		self.m_grid2.SetRowLabelValue( 0, u"Labels" )
		self.m_grid2.SetRowLabelValue( 1, u"1" )
		self.m_grid2.SetRowLabelValue( 2, u"2" )
		self.m_grid2.SetRowLabelValue( 3, u"3" )
		self.m_grid2.SetRowLabelValue( 4, u"4" )
		self.m_grid2.SetRowLabelValue( 5, u"5" )
		self.m_grid2.SetRowLabelValue( 6, u"6" )
		self.m_grid2.SetRowLabelValue( 7, u"7" )
		self.m_grid2.SetRowLabelValue( 8, wx.EmptyString )
		self.m_grid2.SetRowLabelValue( 9, wx.EmptyString )
		self.m_grid2.SetRowLabelValue( 10, wx.EmptyString )
		self.m_grid2.SetRowLabelValue( 11, wx.EmptyString )
		self.m_grid2.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		self.m_grid2.SetLabelTextColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		# Cell Defaults
		self.m_grid2.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		gbSizer6.Add( self.m_grid2, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 6 ), wx.ALL, 5 )
		
		self.m_button24 = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Collect data", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer6.Add( self.m_button24, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button5 = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Return", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer6.Add( self.m_button5, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button4 = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Compute", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer6.Add( self.m_button4, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		self.m_scrolledWindow1.SetSizer( gbSizer6 )
		self.m_scrolledWindow1.Layout()
		gbSizer6.Fit( self.m_scrolledWindow1 )
		gbSizer2.Add( self.m_scrolledWindow1, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( gbSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_grid2.Bind( wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.on_grid_char )
		self.m_button24.Bind( wx.EVT_BUTTON, self.on_collect_data )
		self.m_button5.Bind( wx.EVT_BUTTON, self.on_return )
		self.m_button4.Bind( wx.EVT_BUTTON, self.on_compute )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_grid_char( self, event ):
		event.Skip()
	
	def on_collect_data( self, event ):
		event.Skip()
	
	def on_return( self, event ):
		event.Skip()
	
	def on_compute( self, event ):
		event.Skip()
	

