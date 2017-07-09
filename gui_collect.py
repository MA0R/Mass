# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame11
###########################################################################

class MyFrame11 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 737,608 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		gbSizer1 = wx.GridBagSizer( 0, 0 )
		gbSizer1.SetFlexibleDirection( wx.BOTH )
		gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_button21 = wx.Button( self, wx.ID_ANY, u"Refresh adresses", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.m_button21, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		m_comboBox3Choices = []
		self.m_comboBox3 = wx.ComboBox( self, wx.ID_ANY, u"ASRL2::INSTR", wx.DefaultPosition, wx.DefaultSize, m_comboBox3Choices, 0 )
		gbSizer1.Add( self.m_comboBox3, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		m_comboBox4Choices = [ u"Semi-auto", u"Automatic" ]
		self.m_comboBox4 = wx.ComboBox( self, wx.ID_ANY, u"Semi-auto", wx.DefaultPosition, wx.DefaultSize, m_comboBox4Choices, 0 )
		self.m_comboBox4.SetMinSize( wx.Size( 100,-1 ) )
		
		gbSizer1.Add( self.m_comboBox4, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl5 = wx.TextCtrl( self, wx.ID_ANY, u"Event reports.", wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.VSCROLL )
		self.m_textCtrl5.SetMinSize( wx.Size( 300,200 ) )
		
		gbSizer1.Add( self.m_textCtrl5, wx.GBPosition( 0, 3 ), wx.GBSpan( 5, 1 ), wx.ALL, 5 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Mass names:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		gbSizer1.Add( self.m_staticText2, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, u"20,20s,20d", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl2.SetMinSize( wx.Size( 250,-1 ) )
		
		gbSizer1.Add( self.m_textCtrl2, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Mass positions:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		gbSizer1.Add( self.m_staticText3, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, u"1,2,3", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl3.SetMinSize( wx.Size( 250,-1 ) )
		
		gbSizer1.Add( self.m_textCtrl3, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Number of centerings:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		gbSizer1.Add( self.m_staticText4, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )
		
		self.m_textCtrl4 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer1.Add( self.m_textCtrl4, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button22 = wx.Button( self, wx.ID_ANY, u"RUN!", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button22.SetFont( wx.Font( 15, 70, 90, 92, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.m_button22, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_button23 = wx.Button( self, wx.ID_ANY, u"STOP", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button23.SetFont( wx.Font( 15, 70, 90, 92, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.m_button23, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Instructions", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		self.m_staticText5.SetFont( wx.Font( 90, 70, 90, 92, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.m_staticText5, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 5 ), wx.ALL, 5 )
		
		
		self.SetSizer( gbSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_KEY_DOWN, self.on_char_click )
		self.m_button21.Bind( wx.EVT_BUTTON, self.on_refresh_adresses )
		self.m_button21.Bind( wx.EVT_KEY_DOWN, self.on_char_click )
		self.m_comboBox3.Bind( wx.EVT_KEY_DOWN, self.on_char_click )
		self.m_comboBox4.Bind( wx.EVT_KEY_DOWN, self.on_char_click )
		self.m_textCtrl5.Bind( wx.EVT_KEY_DOWN, self.on_char_click )
		self.m_staticText2.Bind( wx.EVT_KEY_DOWN, self.on_char_click )
		self.m_staticText3.Bind( wx.EVT_KEY_DOWN, self.on_char_click )
		self.m_textCtrl3.Bind( wx.EVT_KEY_DOWN, self.on_char_click )
		self.m_staticText4.Bind( wx.EVT_KEY_DOWN, self.on_char_click )
		self.m_textCtrl4.Bind( wx.EVT_KEY_DOWN, self.on_char_click )
		self.m_button22.Bind( wx.EVT_BUTTON, self.on_run )
		self.m_button22.Bind( wx.EVT_KEY_DOWN, self.on_char_click )
		self.m_button23.Bind( wx.EVT_BUTTON, self.on_stop )
		self.m_button23.Bind( wx.EVT_KEY_DOWN, self.on_char_click )
		self.m_staticText5.Bind( wx.EVT_KEY_DOWN, self.on_char_click )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_char_click( self, event ):
		event.Skip()
	
	def on_refresh_adresses( self, event ):
		event.Skip()
	
	
	
	
	
	
	
	
	
	
	def on_run( self, event ):
		event.Skip()
	
	
	def on_stop( self, event ):
		event.Skip()
	
	
	

