import wx
import wx.xrc
import wx.grid
import numpy as np
import pywxgrideditmixin #Mixing to allow ctrl+v adn ctr+c etc for table.
import time #used for a time stamp in file name
import csv #For saving the csv data files, and loading csv data files.
import time

import gui_circ #Gui of the circular algorithm.
from main_collect import Collector #The popup window for data collecting.

import calc_circ #The analysis tool.
import weighing #Circular weighing thread.

import tolerance #For checking readings against tolerances

class Circ_Controller(gui_circ.MyFrame2):
    """The controller for the circular weighing algorithm."""
    def __init__(self, parent):
        gui_circ.MyFrame2.__init__(self, parent)
        self.m_grid2.__init_mixin__()
        self.m_grid4.__init_mixin__()
        self.parent = parent #the parent window.
        self.Show(True)
        self.tol = 0
        #initial tolerance, zero is cleary wrong so if not overriden it will stand out.
        #Other initial objects are none.
        self.masses = None #The names of all the masses in question.
        self.writing_rows = None #Writing rows for printing, contain differnces, values, undert.
        self.supp_writ_rows = None #Supplementary writing rows, contain constants d_1,d_2,d_3.
        self.sigma = None #The standard deviation, whatever it is (list or single float).
        self.weigher = None #The weighing thread.
        self.popup = None #The popup for controlling the data collection.
        self.initial_time = 0 #Time of first entered data point.
        self.positions = [] #Empty array corresponding to the positions of the masses.

    def on_collect_data(self,event):
        if not self.popup: #Only allow one collector.
            self.popup = Collector(self)
            self.popup.setup(self.masses)

    def on_return(self,event):
        """Send the results back to parent frame, and save csv of data+results"""
        #Construct the file name for the csv data:
        name = time.strftime("data/%Y.%m.%d.%H.%M.%S",time.localtime()) #Time stamp
        for mass in self.masses:
            name += "_"+str(mass) #appends the masses involved.
        name += ".csv" #csv file type.

        grid_data = self.read_grid()
        #Save the data to the file, with lots of extra titles around:
        with open(name,'wb') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(["Circular algorithm data and results"])
            writer.writerow(["Mass positions:"]+self.positions)
            writer.writerows(grid_data)
            writer.writerow("")
            writer.writerow(["Mass","-Mass","Diff","Uncert"])
            writer.writerows(self.writing_rows)
            writer.writerow(["Coefficient","Value"])
            writer.writerows(self.supp_writ_rows)
            writer.writerow(["Residual : "+str(self.sigma)])
            
        #There are now (potentially) multiple results for the differences.
        #We want to return to the main table the average difference, if there are multiple
        w = np.array(self.writing_rows)
        new = w[0] #selects the first copy of the many repetitions of results.
        data = np.transpose(w[:,:,2]) #the 2D array of data only.
        #Now data[0] is the first set of diffs, data[1] is second etc.
        #print(data)
        for i in range(len(data)):
            floats = [float(d) for d in data[i]] #They are strings, need floats.
            
            if len(floats)>1:#FIRST READING IS SKIPPED, if there are multiple readings.
                avg = np.mean(floats[1:])
            else:
                avg = floats[0] #In this case there was only one reading, so it is taken.
            new[i][2] = avg #Save the average of the differences.
        
        self.parent.recieve_result(new,self.supp_writ_rows,self.tol)
        #should return the tolerance??

        self.Close()
        #Because Greg wanted it to close once done? could press the "x"

    def on_grid_char(self,event):
        """When the right mouse button is clicked in the grid,
        if it is clicked in one of the mass columns, a time stamp
        is added to the column to the right. This is for manual entry
        of results."""
        col = event.GetCol()
        row = event.GetRow()
        cols = self.m_grid2.GetNumberCols()
        possible_cols = np.arange(0,cols,2)+1 #Only the odd columns.
        
        if col==1 and row==1:
            self.initial_time = time.time()
            self.m_grid2.SetCellValue(1,0,'0')
        elif col in possible_cols and row>0:
            t = time.time()-self.initial_time
            self.m_grid2.SetCellValue(row,col-1,str(t))
            
    
    def recieve_results(self,data,positions):
        """Recieve results is called by the data collection thread,
        it sends the measured times and weights. This uses the populate grid
        function and immediatly calls the compute function too."""
        if data: #IF DATA IS NOT SOMETHING EMPTY, LIKE [], but dosent capture partially filled data and stuff.
            grid_cols = self.m_grid2.GetNumberCols()
            first_row = [self.m_grid2.GetCellValue(0,c) for c in range(grid_cols)]
            data = [first_row]+data
            self.rows_to_grid(data,self.m_grid2)
            #self.compute()
            #Removed compute, incase data is partially filled or something. User
            #must press compute when they want it done now.
            self.positions = positions
        
    def read_grid(self):
        """Return a list of the grid rows for the main grid."""
        rows = []
        for r in range(self.m_grid2.GetNumberRows()):
            row = []
            for c in range(self.m_grid2.GetNumberCols()):
                cell = self.m_grid2.GetCellValue(r,c)
                row.append(cell)
            rows.append(row)
        return rows
    
    def on_compute(self, event):
        """Event driven function, goes straight to compute so it can run without an event."""
        self.compute()
    def compute(self):
        """Compute and save the differences using the circular analysis tool. Independent
        from event so it can be called by other functions. might put them together now?"""
        names,number_of_masses,times,readings = self.extract()
        writing_rows,supp_writ_rows,sigma = calc_circ.unknown_set(names,number_of_masses,times,readings)
        #writing_rows =   [ [mass1,mass2,difference,uncert],
        #                   [mass3,mass4,difference,uncert]]
        #supp_writing_rows = [[d_1,value],
        #                     [d_2,value],
        #                     [d_1,value]]
        # sigma = array of residuals, [sig1,sig2,sig3] or just [sig1] for one weighing.
        self.writing_rows = writing_rows
        self.supp_writ_rows = supp_writ_rows
        self.sigma = sigma
        self.show_results()
        self.get_tolerances()
            
    def get_tolerances(self):
        Tol = tolerance.Tolerances()
        bals = []
        tols = []
        for mass in self.masses:
            b,t = Tol.tolerance(mass)
            t=float(t)
            if b not in bals:
                bals.append(b)
            if t not in tols:
                tols.append(t)
        tol = max(tols)
        bal = bals[tols.index(tol)]
        self.m_textCtrl6.SetValue("{}: {}".format(bal,tol))
        self.tol = tol
        
    def show_results(self):
        """
        Take the results rows ([mass1,mass2,val,uncert])
        and turn them into something suitable for printing, like this:
        ['mass1-mass2',value,uncert]. Do the same with the supplementary
        rows, those being the values of the coefficients d_n, n = 1,2,3.
        """
        tabulated = []
        for writing_row in self.writing_rows:
            for row in writing_row:
                r = [str(row[0])+'-'+str(row[1].replace('+','-')),row[2],row[3]]
                tabulated.append(r)
        for supp_row in self.supp_writ_rows:
            for row in supp_row:
                tabulated.append(row)
        tabulated.append(['sigma',self.sigma])
        #print(tabulated)
        self.rows_to_grid(tabulated,self.m_grid4)
        
    def extract(self):
        """Extract the times and masses from the table,
        perhaps move to csv eventually?"""
        names = np.array(self.masses)
        number_of_masses = len(self.masses)
        times = []
        readings = []
        rows = self.m_grid2.GetNumberRows()-1
        for i in range(number_of_masses*rows):
            row = i//(number_of_masses) + 1
            col = 2*(i%number_of_masses)
            time = self.m_grid2.GetCellValue(row,col)
            mass = float(self.m_grid2.GetCellValue(row,col+1))
            times.append(time)
            readings.append(mass)
        if not all(times): #If some times are invalid.
            times = range(len(times))
        else: #Convert to array of floats, to ensure they are all ok for analysis.
            times = [float(t) for t in times]
        a = [names,number_of_masses,np.array(times),np.array(readings)]
        return a
    
    def setup(self,masses):
        """Like a second initialisation, called immediatly by the parent.
            But not called during testing"""
        self.masses = masses
        self.set_cols(masses)
        self.set_rows(masses)
        
    def minus_rows(self,n,grid):
        last_position = grid.GetNumberRows() -1
        grid.DeleteRows(last_position-n+1,n)
        
    def add_rows(self,n,grid):
        grid.AppendRows(n, True)
        
    def set_rows(self,masses):
        """Set the rows according to the number of masses"""
        g_n = self.m_grid2.GetNumberRows()
        if len(masses) >= 5:
            r_n = 3 + 1
        else:
            r_n = 7 - len(masses) + 1
        if g_n-r_n > 0:
            self.minus_rows(g_n-r_n,self.m_grid2)
        elif g_n-r_n < 0:
            self.add_rows(r_n-g_n,self.m_grid2)
        self.Layout()
        
    def rows_to_grid(self,rows,grid):
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
