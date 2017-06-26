"""Graphical user interfaces for the circular weighing algorithm,
data colelction, and the final analysis of the masses"""
import wx
import wx.xrc
import wx.grid
import numpy as np
import pywxgrideditmixin

import guimain
import guicirc

import circular

class Circ_Controller(guicirc.MyFrame2):
    """The controller for the circular weighing algorithm."""
    def __init__(self, parent):
        guicirc.MyFrame2.__init__(self, parent)
        self.m_grid2.__init_mixin__()
        self.parent = parent
        self.Show(True)
        self.masses = None
        
    def on_return(self,event):
        """Send the results back to parent frame"""
        print("returning to parent")
        self.parent.recieve_result(self.writing_rows,self.supp_writ_rows,self.sigma)
        
    def on_compute(self, event):
        """Compute and save the differences using circular.py"""
        names,number_of_masses,times,readings = self.extract()
        writing_rows = [0,0,0]
        supp_writ_rows = [0,0,0]
        sigma = [0,0,0]
        for order_in_t in [1,2,3]:
            i = order_in_t - 1
            M = circular.generate_m(readings.size,number_of_masses,order_in_t,times)
            beta,covalent,dof,sigma[i] = circular.analysis(M,readings,number_of_masses,order_in_t)
            writing_rows[i],supp_writ_rows[i] = circular.differences(number_of_masses,order_in_t,beta,covalent,names)
        idx = sigma.index(min(sigma))
        print
        print(idx)
        print
        print(writing_rows[idx])
        print(supp_writ_rows[idx])
        print(sigma)
        self.writing_rows = writing_rows[idx]
        self.supp_writ_rows = supp_writ_rows[idx]
        self.sigma = sigma[idx]
        
    def extract(self):
        """Extract the times and masses from the table, perhaps move to csv eventually?"""
        names = np.array(self.masses)
        number_of_masses = len(self.masses)
        times = []
        readings = []
        rows = self.m_grid2.GetNumberRows()-1
        for i in range(number_of_masses*rows):
            row = i//(number_of_masses) + 1
            col = 2*(i%number_of_masses)
            time = float(self.m_grid2.GetCellValue(row,col))
            mass = float(self.m_grid2.GetCellValue(row,col+1))
            times.append(time)
            readings.append(mass)
        a = [names,number_of_masses,np.array(times),np.array(readings)]
        return a
    
    def setup(self,masses):
        """Like a second initialisation, called immediatly by the parent.
            But not called during testing"""
        self.masses = masses
        self.set_cols(masses)
        self.set_rows(masses)
        
    def set_rows(self,masses):
        """Set the rows according to the number of masses"""
        rows = 7 - len(masses) + 1
        diff = rows - self.m_grid2.GetNumberRows()
        if diff > 0:
            for i in range(diff):
                self.m_grid2.AppendRows(1, True)
        if diff < 0:
            for i in range(-diff):
                last_position = self.m_grid2.GetNumberRows() -1
                self.m_grid2.DeleteRows(last_position)
        self.Layout()
        
    def set_cols(self,masses):
        """Set the columns according to the number of masses"""
        cols = 2*len(masses)
        diff = cols - self.m_grid2.GetNumberCols()
        if diff > 0:
            for i in range(diff):
                self.m_grid2.AppendCols(1, True)
        if diff < 0:
            for i in range(-diff):
                last_position = self.m_grid2.GetNumberCols() -1
                self.m_grid2.DeleteCols(last_position)
        for i in range(cols/2):
            self.m_grid2.SetCellValue(0,2*i+1,masses[i])
        self.Layout()


class Controller(guimain.MyFrame1):
    def __init__(self, parent):
        guimain.MyFrame1.__init__(self, parent)
        wx.grid.Grid.__bases__ += (pywxgrideditmixin.PyWXGridEditMixin,)
        self.m_grid1.__init_mixin__()
        self.Show(True)
        
    def on_plus_row(self, event):
        self.m_grid1.AppendRows(1, True)
        self.Layout()
        
    def on_minus_row(self, event):
        last_position = self.m_grid1.GetNumberRows() -1
        self.m_grid1.DeleteRows(last_position)
        self.Layout()
        
    def on_row_options(self, event):
        selected_rows = self.m_grid1.GetSelectedRows()
        self.new = Circ_Controller(self)
        rows = selected_rows
        masses = []
        for row in rows:
            mass1 =  self.m_grid1.GetCellValue(row,0)
            mass2 =  self.m_grid1.GetCellValue(row,1)
            if mass1 not in masses and mass1 != u'':
                masses.append(mass1)
            if mass2 not in masses and mass2 != u'':
                masses.append(mass2)
        masses = sorted(masses)#for consistancy.
        self.new.setup(masses)
        
    def recieve_result(self, writing_rows, supp_writ_rows, sigma):
        print(writing_rows)
        for input_row in writing_rows:
            print(input_row)
            for row in range(self.m_grid1.GetNumberRows()):
                mass1 = self.m_grid1.GetCellValue(row,0)
                mass2 = self.m_grid1.GetCellValue(row,1)
                #print(mass1,mass2)
                #print(input_row[0],input_row[1])
                if mass1 == input_row[0] and mass2 == input_row[1]:
                    self.m_grid1.SetCellValue(row,2,str(input_row[2]))
                    self.m_grid1.SetCellValue(row,3,str(input_row[3]))
                    self.m_grid1.SetCellValue(row,4,str(sigma))
                elif mass1 == input_row[1] and mass2 == input_row[0]:
                    self.m_grid1.SetCellValue(row,2,str(-input_row[2]))#negative
                    self.m_grid1.SetCellValue(row,3,str(input_row[3]))
                    self.m_grid1.SetCellValue(row,4,str(sigma))
                    
    def on_run(self, event):
        pass
    
if __name__ == "__main__":
    app = wx.App()
    Controller(None)
    app.MainLoop()
