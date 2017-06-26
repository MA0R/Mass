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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 912,265 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		gbSizer2 = wx.GridBagSizer( 0, 0 )
		gbSizer2.SetFlexibleDirection( wx.BOTH )
		gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Masses:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		gbSizer2.Add( self.m_staticText1, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Readings", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		gbSizer2.Add( self.m_staticText3, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		m_comboBox3Choices = [ u"1", u"2", u"3", u"4", u"5", u"2" ]
		self.m_comboBox3 = wx.ComboBox( self, wx.ID_ANY, u"4", wx.DefaultPosition, wx.DefaultSize, m_comboBox3Choices, 0 )
		self.m_comboBox3.SetSelection( 3 )
		gbSizer2.Add( self.m_comboBox3, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button4 = wx.Button( self, wx.ID_ANY, u"Compute", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer2.Add( self.m_button4, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button5 = wx.Button( self, wx.ID_ANY, u"Return", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer2.Add( self.m_button5, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		m_comboBox1Choices = [ u"1", u"2", u"3", u"4", u"5" ]
		self.m_comboBox1 = wx.ComboBox( self, wx.ID_ANY, u"4", wx.DefaultPosition, wx.DefaultSize, m_comboBox1Choices, 0 )
		self.m_comboBox1.SetSelection( 3 )
		gbSizer2.Add( self.m_comboBox1, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_grid2 = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
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
		gbSizer2.Add( self.m_grid2, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 7 ), wx.ALL, 5 )
		
		
		self.SetSizer( gbSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button4.Bind( wx.EVT_BUTTON, self.on_compute )
		self.m_button5.Bind( wx.EVT_BUTTON, self.on_return )
		self.m_comboBox1.Bind( wx.EVT_TEXT_ENTER, self.on_enter_masses )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_compute( self, event ):
		event.Skip()
	
	def on_return( self, event ):
		event.Skip()
	
	def on_enter_masses( self, event ):
		event.Skip()
	

