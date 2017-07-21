"""A class equipped for collecting all the contants necessary
in order to verify readings against balance tolerances, and to
collect the actual weights of standard masses."""
import csv
    
class Tolerances(object):
    def __init__(self,file_name='tolerances.csv'):
        self.balance_names = []
        self.mass_ranges = []
        self.tolerances = []
        with open(file_name,'r') as f:
            reader = csv.reader(f, delimiter=',')
            reader.next() #skip the first header row.
            for row in reader:
                self.balance_names.append(row[0])
                self.mass_ranges.append(row[1])
                self.tolerances.append(row[2])
        self.all_data = zip(self.balance_names,self.mass_ranges,self.tolerances)
        
    def tolerance_by_mass(self,mass):
        """Given a mass, search for it in the tolerances files.
        returns the balance name and the tolerance."""
        tolerance = 0
        balance = "No balance found"
        #This is the initial value, if balance isnt found
        #0 is clearly wrong.
        for b,m,t in self.all_data:
            if float(m) == float(mass):
                tolerance = t
                balance = b
        return (balance,tolerance)

    def nominal_from_string(self,mass):
        """Simple function to only collect ordered digits from the mass names.
        """
        nom = ''
        for s in mass:
            if s in '0123456789':
                nom+=s
        return nom
                
    def tolerance(self, mass_name):
        """Given a mass name, returns the tolerance from the tolerance files."""
        nominal_mass = self.nominal_from_string(mass_name)
        balance,tolerance = self.tolerance_by_mass(nominal_mass)
        return (balance,tolerance)

if __name__ == "__main__":
    tol = Tolerances()
    print(tol.tolerance("100sdfg"))
