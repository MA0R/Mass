"""A tiny little popup window for simply choosing a
set identifier before loading a set"""

import wx
import wx.xrc
import gui_set

class Set_Loader(gui_set.MyDialog1):
    """The popup window for choosing a set identification."""
    def __init__(self, parent):
        gui_set.MyDialog1.__init__(self, parent)
        self.Show(True)
        self.parent = parent
        
    def recieve_file_name(self,name):
        """Recieve a file name, save it as class variable and display in text cntrl"""
        self.file_name = name
        self.m_button15.SetLabel("Load")
        self.m_staticText10.SetLabel(name)
        
    def on_load_set(self,event):
        """Event driven function for returning the set id and file name to the parent,
        which does the actual loading of the file"""
        set_id = self.m_textCtrl9.GetValue()
        self.parent.set_to_table(self.file_name,set_id)
        self.Close()
