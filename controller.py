"""Graphical user interfaces for the circular weighing algorithm,
data colelction, and the final analysis of the masses"""
import wx
import wx.xrc
import wx.grid
import numpy as np
import pywxgrideditmixin #Mixing to allow ctrl+v adn ctr+c etc for table.
import time #used for a time stamp in file name
import csv #For saving the csv data files, and loading csv data files.

import gui_main #Gui of the main parent table.
import gui_circ #Gui of the circular algorithm.

import calc_circ #The analysis tool.
import calc_mass #Final least squares for mass calculations.
import weighing #Circular weighing thread.

class Circ_Controller(gui_circ.MyFrame2):
    """The controller for the circular weighing algorithm."""
    def __init__(self, parent):
        gui_circ.MyFrame2.__init__(self, parent)
        self.m_grid2.__init_mixin__()
        self.parent = parent
        self.Show(True)
        self.masses = None
        self.writing_rows = None
        self.supp_writ_rows = None
        self.sigma = None
        
    def on_run_auto(self):
        port = m_comboBox3.GetValue()
        masses = len(self.masses)
        reads_per_mass = 7 - masses
        weigher = weighing.Thread(port,masses,reads_per_mass,self)
    
    def on_return(self,event):
        """Send the results back to parent frame, and save csv of data+results"""
        #Construct the file name for the csv data:
        name = time.strftime("%Y.%m.%d.%H.%M.%S, ",time.localtime()) #Time stamp
        for mass in self.masses:
            name += "_"+str(mass) #appends the masses involved.
        name += ".csv" #csv file type.

        grid_data = self.read_grid()
        
        with open(name,'wb') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(["Circular algorithm data and results"])
            writer.writerow(["Data:"])
            writer.writerows(grid_data)
            writer.writerow("")
            writer.writerow(["Mass","-Mass","Diff","Uncert"])
            writer.writerows(self.writing_rows)
            writer.writerow(["Coefficient","Value"])
            writer.writerows(self.supp_writ_rows)
            writer.writerow(["Residual : "+str(self.sigma)])
        self.parent.recieve_result(self.writing_rows,self.supp_writ_rows,self.sigma)
        
        self.Close() #Because Greg wanted it to close once done? could press th "x"
        
    def recieve_results(self,data):
        self.populate_grid(data)
    def populate_grid(self,info):
        for r in range(self.m_grid2.GetNumberRows()):
            for c in range(self.m_grid2.GetNumberCols()):
                val = str(info[r][c])
                self.m_grid2.SetCellValue(r,c,val)
                
    def read_grid(self):
        rows = []
        for r in range(self.m_grid2.GetNumberRows()):
            row = []
            for c in range(self.m_grid2.GetNumberCols()):
                cell = self.m_grid2.GetCellValue(r,c)
                row.append(cell)
            rows.append(row)
        return rows
    
    def on_compute(self, event):
        """Compute and save the differences using circular.py"""
        names,number_of_masses,times,readings = self.extract()
        writing_rows = [0,0,0]
        supp_writ_rows = [0,0,0]
        sigma = [0,0,0]
        for order_in_t in [1,2,3]:
            i = order_in_t - 1
            M = calc_circ.generate_m(readings.size,number_of_masses,order_in_t,times)
            beta,covalent,dof,sigma[i] = calc_circ.analysis(M,readings,number_of_masses,order_in_t)
            writing_rows[i],supp_writ_rows[i] = calc_circ.differences(number_of_masses,order_in_t,beta,covalent,names)
        idx = sigma.index(min(sigma))

        print(writing_rows[idx])
        print(supp_writ_rows[idx])
        print(sigma[idx])
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


class Controller(gui_main.MyFrame1):
    def __init__(self, parent):
        gui_main.MyFrame1.__init__(self, parent)
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
            mass_names =  self.m_grid1.GetCellValue(row,0)
            mass1,mass2 = mass_names.split('-',1)
            
            if mass1 not in masses and mass1 not in (u'',u' ','',' '):
                masses.append(mass1)
            if mass2 not in masses and mass2 not in (u'',u' ','',' '):
                masses.append(mass2)
        #masses = sorted(masses)#for consistancy.
        self.new.setup(masses)
        
    def recieve_result(self, writing_rows, supp_writ_rows, sigma):
        print(writing_rows)
        for input_row in writing_rows:
            for row in range(self.m_grid1.GetNumberRows()):
                mass_name = self.m_grid1.GetCellValue(row,0)

                if mass_name == str(input_row[0])+'-'+str(input_row[1]):
                    self.m_grid1.SetCellValue(row,1,str(input_row[2]))
                    #Only need the difference value printed.
                    #self.m_grid1.SetCellValue(row,2,str(input_row[3]))
                    #self.m_grid1.SetCellValue(row,3,str(sigma))
                    
    def extract(self):
        named_diffs = []
        diffs = []
        masses = []
        uncrtnties = []
    
        rows = self.m_grid1.GetNumberRows()
        for row in range(rows):
            print(row)
            #We have 3 cels to read.
            named_diff = self.m_grid1.GetCellValue(row,0)
            #ensure there are no spaces floating around
            named_diff = named_diff.replace(" ","")
            named_diffs.append(named_diff.split('-'))
            #the difference values as floats.
            diff = float(self.m_grid1.GetCellValue(row,1))
            diffs.append(diff)
            #Uncertianty values as floats.
            uncert = float(self.m_grid1.GetCellValue(row,2))
            uncrtnties.append(uncert)
            #Append to list of masses, if these mass names are new.
            sub_list = named_diff.split('-')
            masses = masses + [n for n in sub_list if n not in masses]
        diffs = np.array(diffs)
        uncrtnties = np.array(uncrtnties)
        return [named_diffs,diffs,masses,uncrtnties]

    def on_run(self,event):
        named_diffs,diffs,masses,uncert = self.extract()
        M = calc_mass.generate_m(named_diffs,diffs,masses)
        b,R0,psi_bmeas = calc_mass.analysis(M,diffs,uncert)
        Ub,psi_b = calc_mass.buoyancy_uncert(M,b,psi_bmeas)
        print("Done")
        

    
if __name__ == "__main__":
    app = wx.App()
    Controller(None)
    app.MainLoop()
