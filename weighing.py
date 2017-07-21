"""
An independent thread that does a circular weighing.
"""
import threading
import visa2 as visa
#import visa
import time
import numpy as np

class Thread(threading.Thread):
    def __init__(self,port,masses,mass_positions,reads_per_mass,centerings,parent,run_option,num_cycles,simulated=False):
        threading.Thread.__init__(self)
        rm = visa.ResourceManager()
        self.balance = rm.open_resource(port)
        if not simulated:
            self.balance.baud_rate = 2400
            self.balance.parity = visa.constants.Parity.even
            self.balance.stop_bits = visa.constants.StopBits.one
            self.balance.data_bits = 7
        self.simulated = simulated
        
        self.masses = masses
        self.mass_positions = mass_positions
        self.reads_per_mass = reads_per_mass
        self.parent = parent
        self.num_cycles = num_cycles
        self.run_option = run_option
        self.first_read_time = None #Time of first reading
        self._want_abort = False
        self.space_pressed = False
        self.start()
        
    def run(self):
        """Run either the automatic or semi options"""
        if self.run_option == 'AUTO':
            self.auto()
        elif self.run_option == 'SEMI':
            self.semi_auto()
        else:
            print("Valid run options are AUTO or SEMI")
            
    def write_to_popup(self,s):
        """Call the parent.update_popup method if a prent exists"""
        if not self._want_abort:
            if self.parent:
                self.parent.update_popup(s)
            else:
                print(s)
            
    def semi_auto(self):
        """Data gathering for semi-auto option"""
        self.report_event("Semi auto measurement")
        self.reset_instrument_semi()
        result_rows = []
        for reading in range(self.reads_per_mass):
            row = []
            for mass in self.masses:
                if not self._want_abort:
                    s = "Set mass:\n"+str(mass)
                    self.write_to_popup(s)
                    self.report_event("Reading {} for mass {}".format(reading,mass))
                    #Could wait for balance to read something similar
                    #to some nominal value, then waits for it to settle
                    #and finally reads, somehow avoiding settling down
                    #on the zero measurement. OR for now, just wait 10secs
                    #so waits can be changed.
                    self.wait_for_space()
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
        """Data gathering for automatic options, INCOMPLETE"""
        #How to handle multople readings and centerings?
        self.reset_instrument_auto()
        result_rows = []
        for cycle in range(self.num_cycles):
            for reading in range(self.reads_per_mass):
                row = []
                string = "Measuring"
                for pos,mass in zip(self.mass_positions,self.masses):
                    if not self._want_abort:
                        self.report_event("Reading number {} for mass {}".format(reading,mass))
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
        """Saves the time of the first reading, then calculates
        the time with that as reference. returns time in minutes for no reason"""
        if self.first_read_time == None:
            self.first_read_time = time.time()
            t_in_s = 0.0
        else:
            t_in_s = float(time.time()-self.first_read_time)
        return t_in_s/60.0
    
    def reset_instrument_auto(self):
        """Just a sub function to reset the instrument, for the automatic case"""
        self.balance.write("@")
        self.balance.write("LIFT")
        self.wait(2)
        self.balance.write("Z")
        
    def reset_instrument_semi(self):
        """Reset the instrument for the semi auto case, maybe unecessary"""
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
        """Once data is collected into a table format, cal the parent.recieve_results method if one exists."""
        if not self._want_abort:
            if self.parent == None:
                pass
                #print(data)
            else:
                self.parent.recieve_results(data)
                
    def report_event(self,text):
        """Report some text, calls parent.report_event. This prints to the parent event report box."""
        #Perhaps save a log file idk.
        if self.parent:
            self.parent.report_event(text)
        else:
            print(text)
        
    def position(self,pos):
        """A sub routine to positions masses, incomplete. Used by the auto measuring thing"""
        self.lift()
        self.lift()
        self.report_event("Moving to "+str(pos))
        self.lift_sink_move("MOVE"+str(pos))
        self.sink()
        self.sink()
        self.wait(20)
        
    def lift(self):
        self.report_event("Lifting")
        self.lift_sink_move("LIFT")
        
    def sink(self):
        self.report_event("Sinking")
        self.lift_sink_move("SINK")
        
    def lift_sink_move(self,word):
        """Lift sink or move once and check for ready state from balance.
        If it takes too long just abort"""
        start_time = time.time()
        self.balance.write(word)
        done = False
        while not done:
            if self._want_abort:
                break
            try:
                r = self.balance.read()
                self.report_event(repr(r))
            except visa.VisaIOError:
                r=''
                
            if not self.simulated:
                if r == 'ready\r\n':
                    done = True
                elif r =='ERROR: In weighing position already.ready\r\n':
                    self.report_event("Balance was already in position")
                    done = True
                elif time.time()-start_time > 120:
                    self.report_event("Waited too long")
            else:
                self.report_event("Simulated, not waiting for 'ready'")
                done = True
                
    def read_weight(self):
        """A funcntion to read the weight of the balance once it is stable"""
        self.balance.write("S")
        stable = False
        while stable == False:
            if self._want_abort:
                break
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
        avg = np.average(readings)
        self.report_event("Average reading:")
        self.report_event(avg)
        return avg
    
    def float_reading(self):
        """Reads the balance, and removes spaces and letters from the reading preparing it to be cast into a float"""
        val = 0
        if not self._want_abort:
            try:
                val = self.balance.read().replace(' ','')
                val = val.replace('S','')
                val = val.replace('kg','*1e3')
                val = val.replace('g','')
            except visa.VisaIOError:
                val = 'Failed'
        return val
    
    def abort(self):
        """The abort of the thread, flags it as aborted"""
        self.write_to_popup("Aborted")
        self._want_abort = True
        
    def wait_for_space(self):
        """Waits until space key is hit, checks the abort flag."""
        #Waits for space key to be pressed in main table
        self.space_pressed = False
        if not self._want_abort:
            self.report_event("Waiting for [space] key press")
        while not self.space_pressed:
            if self._want_abort:
                break
            
    def wait(self, period):
        """Waits a desired period of time, checking the abort flag."""
        initial = time.time()
        period = 0
        if self._want_abort == False:
            self.report_event("Waiting for {}s".format(period))
            while time.time()-initial < period:
                if self._want_abort:
                    period = 0
    
if __name__ == "__main__":
    #sample setup here, for running tests or running this without a parent.
    #perhaps it can save the reading results to csv is no parent is present, that way
    #it is possible to run the whole thing without the gui.
    port = 'ASRL2::INSTR'
    masses = ['100A','100']
    mass_positions = [1,2]
    reads_per_mass = 3
    parent = None
    run_option = 'AUTO'
    centerings = 1
    num_cycles = 1
    a = Thread(port,masses,mass_positions,reads_per_mass,centerings,parent,run_option,num_cycles)
    
