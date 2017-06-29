"""
An independent thread that does a circular weighing.
"""
import threading
import visa
import time

class Thread(threading.Thread):
    def __init__(self,port,masses,reads_per_mass,parent):
        threading.Thread.__init__(self)
        rm = visa.ResourceManager()
        self.balance = rm.open_resource(port)
        self.masses = masses
        self.reads_per_mass = reads_per_mass
        self._want_abort = False
        self.start()
        
    def run(self):
        self.reset_instrument()
        result_rows = []
        for reading in range(self.reads_per_mass):
            row = []
            for mass in range(self.masses):
                self.position(mass)
                self.wait(3) 
                row.append(self.read_weight())
            result_rows.append(row)
        self.return_results(result_rows)

    def reset_instrument(self):
        pass
    
    def return_results(data):
        if parent == None:
            print(data)
        else:
            parent.recieve_results(data)
        
    def position(self,mass):
        print("Positioning mass "+str(mass))

    def read_weight(self):
        print("Reading")
        return 1
    
    def abort(self):
        self._want_abort = True
        
    def wait(self, period):
        initial = time.time()
        if self._want_abort == False:
            print("Waiting {} seconds".format(period))
            while time.time()-initial < period:
                if self._want_abort == True:
                    period = 0
    
if __name__ == "__main__":
    a = Thread('ASRL2::INSTR',2,5,None)
