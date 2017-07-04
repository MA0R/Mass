"""Graphical user interfaces for the circular weighing algorithm,
data colelction, and the final analysis of the masses. The first class
if the gui and handling of circular pop-up window. The second class is for the
main body of the program and final least squares analysis."""
import wx
import wx.xrc
import wx.grid
import numpy as np
import pywxgrideditmixin #Mixing to allow ctrl+v adn ctr+c etc for table.
import time #Used for a time stamp in file name.
import csv #For saving the csv data files, and loading csv data files.
import os.path #For joining some file path names.

import gui_main #Gui of the main parent table.
import calc_mass #Final least squares for mass calculations.
from pop_up import Circ_Controller #Circullar controller

class Controller(gui_main.MyFrame1):
    def __init__(self, parent):
        gui_main.MyFrame1.__init__(self, parent)
        wx.grid.Grid.__bases__ += (pywxgrideditmixin.PyWXGridEditMixin,)
        self.m_grid1.__init_mixin__()
        self.Show(True)
        self.results = [[0],[0],[0]]
        self.new = None #The pop up window for circular algorithm handling.
        
    def on_plus_row(self, event):
        self.add_rows(1,self.m_grid1)
        self.Layout()
        
    def add_rows(self,n,grid):
        grid.AppendRows(n, True)
        
    def on_minus_row(self, event):
        self.minus_rows(1,self.m_grid1)
        self.Layout()
        
    def minus_rows(self,n,grid):
        last_position = grid.GetNumberRows() -1
        grid.DeleteRows(last_position-n+1,n)
        
    def on_row_options(self, event):
        """
        Read selected rows, and send the mass names used to the circular weighing gui.
        """
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
        """
        Recieve the result from the circular algorithm, and print
        just the differences to the correct place in the table
        """
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
        """
        Extracts the data from the table, ensuring to remove
        unwanted spaces from the numbers and so on. 
        """
        named_diffs = []
        diffs = []
        masses = []
        uncrtnties = []
        string_diffs = []
        
        rows = self.m_grid1.GetNumberRows()
        for row in range(rows):
            #We have 3 cels to read.
            named_diff = self.m_grid1.GetCellValue(row,0)
            if named_diff not in ('',' ',u'',u' ',None): #So if it is not an empty segment.
                string_diffs.append(named_diff)
                #Ensure there are no spaces floating around:
                named_diff = named_diff.replace(" ","")
                #This next step stores information seemingly incorrectly,
                #the string is split at thte "-" signs so we replace each "+"
                #with a "-+", this means after splitting the mass that was positive
                #before now has a reminder plus sign.
                #so: 50+50-100 goes to 50-+50-100
                #which is then split into: [50,+50,100]
                #This plus sign is later read and interpreted by the program
                #when matrix M is constructed.
                named_diff = named_diff.replace('+','-+')
                named_diffs.append(named_diff.split('-'))
                #the difference values as floats.
                diff = float(self.m_grid1.GetCellValue(row,1).replace(' ',''))
                diffs.append(diff)
                #Uncertianty values as floats.
                uncert = float(self.m_grid1.GetCellValue(row,2).replace(' ',''))
                uncrtnties.append(uncert)
                #Append to list of masses, if these mass names are new.
                sub_list = named_diff.replace('+','') #remove plus signs now.
                sub_list = sub_list.split('-') #Just mass names, no signs.
                masses = masses + [n for n in sub_list if n not in masses]
        diffs = np.array(diffs)
        uncrtnties = np.array(uncrtnties)
        return [named_diffs,string_diffs,diffs,masses,uncrtnties]

    def on_run(self,event):
        """
        Compute! uses extracted info from the tables and the calc_masses
        module for the analysis.
        """
        named_diffs,string_diffs,diffs,masses,uncert = self.extract()
        if len(named_diffs) > 1:
            M = calc_mass.generate_m(named_diffs,diffs,masses)
            b,R0,psi_bmeas = calc_mass.analysis(M,diffs,uncert)
            Ub,psi_b = calc_mass.buoyancy_uncert(M,b,psi_bmeas)
            #Now print residuals (R0) into the last column in the grid.
            rows = self.m_grid1.GetNumberRows()
            to_table = np.transpose([string_diffs,diffs,uncert,R0])
            self.rows_to_grid(to_table,self.m_grid1)
            #And save the results.
            self.results = [masses,b,Ub] #update the class variable
            self.present_results()
        else:
            #Perhaps change to a pop up window that closes on ok.
            print("Cannot run, no data loaded")
        
    def present_results(self):
        """Put results into the results grid."""
        results = np.transpose(np.array(self.results))
        self.rows_to_grid(results,self.m_grid3)
        
    def get_file_name(self):
        """Uses the wx file navigator to select a file, and then opens.
        Ignores first two rows in file."""
        #More wild card options are available like this:
        #wildcard = "Poject source (*.csv; *.xls; *.xlsx; *.xlsm)|*.csv;*.xls; *.xlsx; *.xlsm|" \
        # "All files (*.*)|*.*"
        #But currently only interested in csv files:
        wildcard = "Poject source (*.csv)|*.csv|All files (*.*)|*.*"
        proj_file = None
        dlg = wx.FileDialog(self, "Choose a project file", 'dirname,space filler', "",
        wildcard, wx.OPEN | wx.MULTIPLE)
        
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
        dlg.Destroy()
        return [dirname,filename]
    
    def on_load_file(self,event):
        dirname,filename = self.get_file_name()
        proj_file = os.path.join(dirname, filename)
        
        if proj_file != None:
            with open(proj_file,'r') as f:
                reader = csv.reader(f,delimiter=',')
                rows = []
                for row in reader:
                    rows.append(row)
                    #Note the first two rows are just header.
                self.rows_to_grid(rows[2:],self.m_grid1)
            
    def rows_to_grid(self,rows,grid):
        """Put a list of rows into a specified grid. Enlarges or shrinks the grid to match the rows."""
        g_n = grid.GetNumberRows()
        r_n = len(rows)
        if g_n-r_n > 0:
            self.minus_rows(g_n-r_n,grid)
        elif g_n-r_n < 0:
            self.add_rows(r_n-g_n,grid)
        for r in range(r_n):
            for c in range(len(rows[r])):
                grid.SetCellValue(r,c,str(rows[r][c]))
        self.Layout()
        
    def on_save_results(self,event):
        dirname,filename = self.get_file_name()
        proj_file = os.path.join(dirname, filename)
        if proj_file != None:
            with open(proj_file,'wb') as f:
                writer = csv.writer(f,delimiter=',')
                writer.writerow(['Results file'])
                writer.writerow(['Masses','Difference (g)','Uncert (ug)','Residual (ug)'])
                writer.writerows(np.transpose(self.results))
            data_name = "lesq_"+filename
            data_file = os.path.join(dirname, data_name)

            with open(data_file,'wb') as f:
                writer = csv.writer(f,delimiter=',')
                writer.writerow(['Data file'])
                writer.writerow(['Masses','Difference (g)','Uncert (ug)','Residual (ug)'])
                for r in range(self.m_grid1.GetNumberRows()):
                    row = []
                    for c in range(self.m_grid1.GetNumberCols()):
                        row.append(self.m_grid1.GetCellValue(r,c))
                    writer.writerow(row)

if __name__ == "__main__":
    #Should usually be run as main, but can be run as a child too.
    app = wx.App()
    Controller(None)
    app.MainLoop()
