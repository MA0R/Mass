"""Graphical user interfaces for the circular weighing algorithm,
data colelction, and the final analysis of the masses. The first class
if the gui and handling of circular pop-up window. The second class is for the
main body of the program and final least squares analysis."""
import wx
import wx.xrc
import wx.grid
import numpy as np
import time #Used for a time stamp in file name.
import csv #For saving the csv data files, and loading csv data files.
import os.path #For joining some file path names.

import modules.pywxgrideditmixin as pywxgrideditmixin #Mixing to allow ctrl+v adn ctr+c etc for table.
import modules.gui_main as gui_main #Gui of the main parent table.
import modules.calc_mass as calc_mass #Final least squares for mass calculations.
from modules.main_circ import Circ_Controller #Circullar controller
from modules.main_set import Set_Loader


class Controller(gui_main.MyFrame1):
    def __init__(self, parent):
        gui_main.MyFrame1.__init__(self, parent)
        wx.grid.Grid.__bases__ += (pywxgrideditmixin.PyWXGridEditMixin,)
        self.m_grid1.__init_mixin__()
        self.m_grid3.__init_mixin__()
        self.Show(True)
        self.results = [[0],[0],[0]]
        self.new = None #The pop up window for circular algorithm handling.
        
    def on_plus_row(self, event):
        self.add_rows(1,self.m_grid1)
        self.Layout()
        
    def add_rows(self,n,grid):
        grid.AppendRows(n, True)
        
    def on_minus_row(self, event):
        selected_rows = self.m_grid1.GetSelectedRows()
        if selected_rows == []:
            self.minus_rows(1,self.m_grid1)
        else:
            for row in selected_rows[::-1]: #must read the rows form end to start!
                self.m_grid1.DeleteRows(row,1)
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
            mass1 = mass1.replace('-','+')
            mass2 = mass2.replace('-','+')
            if mass1 not in masses and mass1 not in (u'',u' ','',' '):
                masses.append(mass1)
            if mass2 not in masses and mass2 not in (u'',u' ','',' '):
                masses.append(mass2)
        #masses = sorted(masses)#for consistancy.
        self.new.setup(masses)
        
    def recieve_result(self, writing_rows, supp_writ_rows, sigma):
        """
        Recieve the result from the circular algorithm, and print
        just the differences to the correct place in the table. If
        multiple differences are give, it takes the averge of them.
        """
        
        for input_row in writing_rows:
            for row in range(self.m_grid1.GetNumberRows()):
                mass_name = self.m_grid1.GetCellValue(row,0)
                #First do first minus the second, replacing + with - in second.
                #first_sec = first minus second
                first_sec = input_row[0]+'-'+input_row[1].replace('+','-')
                #sec_first is secon minus first
                sec_first = input_row[1]+'-'+input_row[0].replace('+','-')
                if mass_name == first_sec:
                    self.m_grid1.SetCellValue(row,1,str(input_row[2]))
                    self.m_grid1.SetCellValue(row,2,str(sigma))
                elif mass_name == sec_first:
                    #Then we need the negative of the difference, but ofcourse sigma is the same.
                    self.m_grid1.SetCellValue(row,1,str(-1*float(input_row[2])))
                    self.m_grid1.SetCellValue(row,2,str(sigma))
                    
    def extract(self):
        """
        Extracts the data from the table, ensuring to remove
        unwanted spaces from the numbers and so on. 
        """
        named_diffs = [] #The text differences, like '50','50s' corresponding to '50-50s'.
        diffs = []       #The actual differences, as floats.
        masses = []      #The names of the masses involved.
        uncrtnties = []  #The uncertainties of the balances.
        string_diffs = []#The full differences as strings such as '50-50s'
        failed_rows = [] #Rows that did not have sufficient info.

        rows = self.m_grid1.GetNumberRows()
        
        selected_rows = self.m_grid1.GetSelectedRows()
        if selected_rows == []:
            selected_rows = range(rows)
        
        for row in range(rows):
            #We have 3 cels to read.
            named_diff = self.m_grid1.GetCellValue(row,0).replace(' ','')
            diff = self.m_grid1.GetCellValue(row,1).replace(' ','')
            uncert = self.m_grid1.GetCellValue(row,2).replace(' ','')
            if all([named_diff,diff,uncert]) and row in selected_rows:
                #So if none of those are empty, and if its in the selected rows.
                string_diffs.append(named_diff)
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
                diff = float(diff)
                diffs.append(diff)
                #Uncertianty values as floats.
                uncert = float(uncert)
                uncrtnties.append(uncert)
                #Append to list of masses, if these mass names are new.
                sub_list = named_diff.replace('+','') #remove plus signs, now it is mass names seperated by '-'.
                sub_list = sub_list.split('-') #Just mass names, no signs, as an array.
                masses = masses + [n for n in sub_list if n not in masses]
            else:
                failed_rows.append(row)
        diffs = np.array(diffs)
        uncrtnties = np.array(uncrtnties)
        return [named_diffs,string_diffs,diffs,masses,uncrtnties,failed_rows]

    def on_run(self,event):
        """
        Compute! uses extracted info from the tables and the calc_masses
        module for the analysis.
        """
        named_diffs,string_diffs,diffs,masses,uncert,failed_rows = self.extract()
        if len(named_diffs) > 1:
            M = calc_mass.generate_m(named_diffs,diffs,masses)
            b,R0,psi_bmeas = calc_mass.analysis(M,diffs,uncert)
            Ub,psi_b = calc_mass.buoyancy_uncert(M,b,psi_bmeas)
            #Now print residuals (R0) into the last column in the grid.
            rows = self.m_grid1.GetNumberRows()
            to_table = np.transpose([string_diffs,diffs,uncert,R0])
            self.rows_to_grid(to_table,self.m_grid1,failed_rows)
            #And save the results.
            self.results = [masses,b,Ub,2*Ub] #update the class variable
            self.present_results()
        else:
            #Perhaps change to a pop up window that closes on ok.
            print("Cannot run, no data loaded")
            
    def on_load_set(self,event):
        """Selects a file name, and calls set_to_table to print the set at the bottom of the grid"""
        dirname, filename = self.get_file_name()
        proj_file = os.path.join(dirname, filename)
        self.set_loader = Set_Loader(self)
        self.set_loader.recieve_file_name(proj_file)
        
    def set_to_table(self,proj_file,set_id):
        """Reads a set file and appends it to the bottom of the grid."""
        if proj_file != "":
            old_rows = self.m_grid1.GetNumberRows()
            names = []
            #collect all names already in grid
            for r in range(old_rows):
                name = self.m_grid1.GetCellValue(r,0)
                names.append(name)

            last_row = old_rows
            with open(proj_file,'r') as f:
                reader = csv.reader(f,delimiter=',')
                for row in reader:
                    if row[0] not in names:
                        self.add_rows(1,self.m_grid1)
                        last_row+=1
                        for c in range(min(4,len(row))):
                            #-1 since we start counting at zero
                            value = row[c]
                            if c == 0: #Add the set identifier to the name.
                                value = str(value)+str(set_id)
                            self.m_grid1.SetCellValue(last_row-1,c,value)            
    
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
        dirname = ""
        filename = ""
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
        dlg.Destroy()
        return [dirname, filename]
    
    def on_load_file(self, event):
        dirname, filename = self.get_file_name()
        proj_file = os.path.join(dirname, filename)
        
        if proj_file != "":
            with open(proj_file,'r') as f:
                reader = csv.reader(f,delimiter=',')
                rows = []
                for row in reader:
                    if row[0] in ('Results',''):
                        break
                    rows.append(row)
                    #Note the first two rows are just header.
                self.rows_to_grid(rows[2:],self.m_grid1)
    
    def rows_to_grid(self, rows, grid, failed_rows=[]):
        """Put a list of rows into a specified grid. Enlarges or shrinks the grid to match the rows.
        Has an optional parameter, a list of rows that failed in reading and should therefore be skipped."""
        g_n = grid.GetNumberRows()
        r_n = len(rows)+len(failed_rows)
        if g_n-r_n > 0:
            self.minus_rows(g_n-r_n,grid)
        elif g_n-r_n < 0:
            self.add_rows(r_n-g_n,grid)
        rows_counter = 0
        for r in range(r_n):
            if r not in failed_rows:
                for c in range(len(rows[rows_counter])):
                    grid.SetCellValue(r,c,str(rows[rows_counter][c]))
                rows_counter += 1
        self.Layout()
        
    def on_save_results(self, event):
        dirname,filename = self.get_file_name()
        proj_file = os.path.join(dirname, filename)
            
        if proj_file != None:
            with open(proj_file,'wb') as f:
                rows = self.m_grid1.GetNumberRows()
                selected_rows = self.m_grid1.GetSelectedRows()
                if selected_rows == []:
                    selected_rows = range(rows)
                writer = csv.writer(f,delimiter=',')
                writer.writerow(['Input data'])
                writer.writerow(['Masses','Difference (g)','Uncert (ug)','Residual (ug)'])
                for r in selected_rows:
                    row = []
                    for c in range(self.m_grid1.GetNumberCols()):
                        row.append(self.m_grid1.GetCellValue(r,c))
                    writer.writerow(row)
                    
                writer.writerow(['Results'])
                writer.writerow(['Masses name','Value (g)','Uncert (ug)','95% ci (ug)'])
                writer.writerows(np.transpose(self.results))
                
    def on_save_set(self,event):
        dirname,filename = self.get_file_name()
        proj_file = os.path.join(dirname, filename)

        if proj_file != None:
            with open(proj_file,'wb') as f:
                rows = self.m_grid3.GetNumberRows()
                selected_rows = self.m_grid3.GetSelectedRows()
                if selected_rows == []:
                    selected_rows = range(rows)
                writer = csv.writer(f,delimiter=',')
                for r in selected_rows:
                    row = []
                    for c in range(self.m_grid3.GetNumberCols()):
                        val = self.m_grid3.GetCellValue(r,c)
                        if c==0: #Just the value, need to remove all letters.
                            val = self.nom_from_str(val)
                        row.append(val)
                    writer.writerow(row)
                    
    def nom_from_str(self,mass):
        """Nominal mass from string, following the convention:
        mass_name = [nominal_mass_value][set identifier] such as 100MAd."""
        nom = ''
        for s in mass:
            if s in '0123456789':
                nom+=s
        return nom
        
if __name__ == "__main__":
    #Should usually be run as main, but can be run as a child too.
    app = wx.App()
    Controller(None)
    app.MainLoop()
