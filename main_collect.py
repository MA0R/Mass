"""Graphical user interfaces for the circular weighing algorithm,
data colelction, and the final analysis of the masses. The first class
if the gui and handling of circular pop-up window. The second class is for the
main body of the program and final least squares analysis."""
import wx
import wx.xrc
import wx.grid
import numpy as np
import time #Used for a time stamp in file name.
import visa

import gui_collect #Gui of the main parent table.

import weighing #Circular weighing thread.

class Collector(gui_collect.MyFrame11):
    def __init__(self, parent):
        gui_collect.MyFrame11.__init__(self, parent)
        self.parent = parent
        self.Show(True)
        self.weigher = None
        
    def setup(self,masses):
        self.masses = masses
        self.m_textCtrl2.SetValue(",".join(masses))
        positions = range(1,len(masses)+1)
        positions = [str(p) for p in positions]
        self.m_textCtrl3.SetValue(",".join(positions))
        
    def on_stop(self,event):
        """Calls abort on the thread, the thread can't be killed but this will
        inform it that it is time to stop working now. It will stop when it wants."""
        if self.weigher:
            self.weigher.abort()
            self.weigher = None

    def on_run(self, event):
        """Collects the run options from the input buttons and then
        sends it to a independent thread. The thread then sends the
        info back. The thread is then independent."""
        port = self.m_comboBox3.GetValue()
        masses = self.m_textCtrl2.GetValue().split(",")
        positions = self.m_textCtrl3.GetValue()
        num_cycles = self.m_textCtrl51.GetValue().replace(" ","")
        centerings = self.m_textCtrl4.GetValue().replace(" ","")
        simulated = False
        
        if positions in ('',' '):
            positions = range(1,len(masses)+1)
        else:
            positions = positions.split(',')
            positions = [int(p) for p in positions] #Make sure they are all ints
        
        if len(masses) >=5:
            reads_per_mass = 3
        else:
            reads_per_mass = 7 - len(masses)
            
        parent = self
        
        selection = self.m_comboBox4.GetValue()
        if "Auto" in selection:
            run_option = 'AUTO'
            try:
                num_cycles = int(num_cycles)
            except ValueError:
                num_cycles = 1
                self.m_textCtrl51.SetValue('1')
            try:
                centerings = int(centerings)
            except ValueError:
                centerings = 1
                self.m_textCtrl4.SetValue('1')
        else:
            run_option = 'SEMI'
        if "Sim." in selection:
            simulated = True
        if not self.weigher:
            self.weigher = weighing.Thread(port,masses,positions,reads_per_mass,centerings,parent,run_option,num_cycles,simulated)
        
    def on_refresh_adresses(self, event):
        """Refresh the connected visa adresses and add to the selection box"""
        #No need for a try block?
        rm = visa.ResourceManager()#new Visa
        resources = rm.list_resources()
        self.m_comboBox3.Clear()
        for adress in resources:
            self.m_comboBox3.Append(adress)

    def update_popup(self,text):
        """Updates the large instruction text"""
        self.m_staticText5.SetLabel(text)

    def report_event(self,text):
        """Report something in the text box, used like live updates"""
        self.m_textCtrl5.AppendText(str(text)+"\n")
        
    def on_char_click(self,event):
        """When a character is clicked, if it is teh space key, move to the next mass.
Used in the semi-auto reading mode, program waits for user to put a new mass on."""
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SPACE:
            if self.weigher:
                self.weigher.space_pressed = True

    def recieve_results(self,data):
        """Passes the data to the parent window"""
        self.parent.recieve_results(data)
