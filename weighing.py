"""
An independent thread that does a circular weighing.
"""
import threading
import visa2 as visa
import time
import numpy as np

class Thread(threading.Thread):
    def __init__(self,port,masses,mass_positions,reads_per_mass,parent,run_option):
        threading.Thread.__init__(self)
        rm = visa.ResourceManager()
        self.balance = rm.open_resource(port)
        self.masses = masses
        self.mass_positions = mass_positions
        self.reads_per_mass = reads_per_mass
        self.parent = parent
        self.run_option = run_option
        self.first_read_time = None #Time of first reading
        self._want_abort = False
        self.start()
        
    def run(self):
        if self.run_option == 'AUTO':
            self.auto()
        elif self.run_option == 'SEMI':
            self.semi_auto()
        else:
            print("Valid run options are AUTO or SEMI")
            
    def write_to_popup(self,s):
        if not self._want_abort:
            if self.parent:
                self.parent.update_popup(s)
            else:
                print(s)
            
    def semi_auto(self):
        #print("Semi auto run")
        self.reset_instrument_semi()
        result_rows = []
        for reading in range(self.reads_per_mass):
            row = []
            for mass in self.masses:
                if not self._want_abort:
                    s = "Set mass:\n"+str(mass)
                    self.write_to_popup(s)
                    #Could wait for balance to read something similar
                    #to some nominal value, then waits for it to settle
                    #and finally reads, somehow avoiding settling down
                    #on the zero measurement. OR for now, just wait 10secs
                    #so waits can be changed.
                    self.wait(10)
                    s = "Measuring:\n"+mass
                    self.write_to_popup(s)
                    weight_reading = self.read_weight()
                    row.append(self.time_from_first())
                    row.append(weight_reading)
            result_rows.append(row)
        self.write_to_popup("Done")
        self.balance.close()
        self.return_results(result_rows)
    
    def auto(self):
        self.reset_instrument_auto()
        result_rows = []
        
        for reading in range(self.reads_per_mass):
            row = []
            string = "Measuring"
            for pos in self.mass_positions:
                if not self._want_abort:
                    string +="."
                    self.write_to_popup(string)
                    #print("Reading at pos: "+str(pos))
                    self.position(pos)
                    weight_reading = self.read_weight()
                    row.append(self.time_from_first())
                    row.append(weight_reading)
            result_rows.append(row)
        self.write_to_popup("Done")
        self.balance.close()
        self.return_results(result_rows)
        
    def time_from_first(self):
        if self.first_read_time == None:
            self.first_read_time = time.time()
            t_in_s = 0.0
        else:
            t_in_s = float(time.time()-self.first_read_time)
        return t_in_s/60.0
    
    def reset_instrument_auto(self):
        self.balance.write("@")
        self.balance.write("LIFT")
        self.wait(2)
        self.balance.write("Z")
        
    def reset_instrument_semi(self):
        self.balance.write("@")
        for i in range(3):
            string = None
            try:
                string = self.balance.read()
            except visa.VisaIOError:
                pass
            #print(i)
            #print(string)
            if string == 'I4 A "B525073136"':
                break
    
    def return_results(self,data):
        if not self._want_abort:
            if self.parent == None:
                pass
                #print(data)
            else:
                self.parent.recieve_results(data)
        
    def position(self,pos):
        self.balance.write("LIFT")
        self.wait(3)
        self.balance.write("TURN 1")
        self.wait(3)
        self.balance.write("SINK")
        self.wait(3)

    def read_weight(self):
        self.balance.write("S")
        stable = False
        while stable == False:
            try:
                #Tries to read and also turn reading into a float.
                #If either fails, tries again.
                discarded = self.float_reading()
                #will not get rid of 'd' characters and stuff,
                #so fails if wait is not stable
                discarded = float(discarded)
                stable = True
                #print("Initial reading sucessfull")
            except ValueError:
                self.wait(0.1)
        self.wait(5)
        readings = []
        for i in range(3):
            self.balance.write("SI")
            self.wait(0.1)
            reading = self.float_reading()
            readings.append(float(reading))
            
        return np.average(readings)
    
    def float_reading(self):
        try:
            val = self.balance.read().replace(' ','')
            val = val.replace('S','')
            val = val.replace('g','')
            val = val.replace('kg','*1e3')
        except visa.VisaIOError:
            val = 'Failed'
        return val
    
    def abort(self):
        self.write_to_popup("Aborted")
        self._want_abort = True
        
    def wait(self, period):
        initial = time.time()
        if self._want_abort == False:
            #print("Waiting {} seconds".format(period))
            while time.time()-initial < period:
                if self._want_abort == True:
                    period = 0
    
if __name__ == "__main__":
    port = 'ASRL2::INSTR'
    masses = ['100A','100']
    mass_positions = [1,2]
    reads_per_mass = 3
    parent = None
    run_option = 'SEMI'
    a = Thread(port,masses,mass_positions,reads_per_mass,parent,run_option)
