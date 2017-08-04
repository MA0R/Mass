"""
Python implementation of the circular weighing algorithm.
Functions here can be used for any other similar regression analysis.
"""
import numpy as np #Numpy module will be used for fast handling of linear algebra
from numpy.linalg import inv
import csv

def generate_m(num_readings,num_masses,order_in_t,times=[]):
    """Generates matrix M based on number of readings,
    number of measured objects, order of time polynomial
    and the measurement times."""
    if times == [] or not all(times): #Fill time as simple ascending array, [1,2,3..]
        times = np.arange(num_readings)
    else: #Ensure that time is a numpy array object.
        times = np.array(times)
    shape = (num_readings, num_masses+order_in_t)
    M = np.zeros(shape) #generate an array of zeros in memory.
    #Now populate M with t, t squarred etc... these fill the columns after the mass columns.
    for i in range(order_in_t):
        M[:,-i-1] = times**(order_in_t-i)
    #The rest of the matrix has repeated identity matrices, to pick up masses.
    for i in range(len(times)):
        row = i
        col = i%num_masses
        M[row,col] = 1
    return M

def extract_file(filename):
    """Given some filename, extract the useful information.
    That is, the measurement times, readings themselves, number of columns
    (and os number of masses) and the names/labels of the masses."""
    rows = []
    with open(filename,'r') as f:
        reader = csv.reader(f,delimiter = ',')
        for row in reader:
            rows.append(row)
    
    names = [rows[2][i] for i in range(len(rows[2])) if i%2==1]
    number_of_masses = len(names) #Each column corresponds to a mass.
    masses = []
    times = []
    for row in rows[3:]:
        if not any(row):#If it is None, or empty.
            break #Stop collecting data, csv file has results beyond this point or is empty.
        for i,val in enumerate(row): #Each item in enumerate is a tuple, (number, object).
            if i%2 == 1:
                masses.append(float(val))
            else:
                if val:
                    times.append(float(val))
                else:
                    times.append(None)

    readings = np.array(masses)
    times = np.array(times)
    return [names,number_of_masses,times,readings]

def analysis(M,readings,num_masses,order_in_t):
    """The guts of the algorithm, using matrix M,
    the readings, and number of masses and order in t
    the beta vector (mass estimates) can be calculated as well as
    covalent matrix and residuals."""
    m_t_m = np.dot(np.transpose(M),M)
    A = np.dot(inv(m_t_m),np.transpose(M))
    beta = np.dot(A,readings)

    y_minus_xb = readings-np.dot(M,beta)
    dof = len(readings) - num_masses - order_in_t
    sigma_squarred = np.dot(np.transpose(y_minus_xb),y_minus_xb)/dof
    sigma = np.sqrt(sigma_squarred)
    covalent = sigma_squarred*inv(m_t_m)
    return [beta,covalent,dof,sigma]

def differences(num_masses,order_in_t,beta,covalent,names):
    """Given the results calculated in analysis, it computes the various
    mass differences and their errors, and generates a list of results.
    Returns an array of arrays that can be saved to csv for data presentation."""
    #writing_rows = [["Masses","Difference","1 std"]] #Rows to write to the results file.
    writing_rows = []
    for i in range(num_masses):
        for j in range(i+1,num_masses):
            diff = beta[i]-beta[j]
            error_squared = covalent[i,j]+covalent[j,i]
            error = np.sqrt(error_squared)
            writing_row = [names[i],names[j],diff,error]
            #writing_row = "{} - {},{} +/- {}\n".format(names[i],names[j],diff,error)
            writing_rows.append(writing_row)
    supp_writ_rows = []
    for i in range(order_in_t):
        supp_writ_row = ["d_{}".format(i+1),beta[i+num_masses]]
        #Need to know the uncertainty of these bits too, somehow from the diagonal?
        supp_writ_rows.append(supp_writ_row)
    return [writing_rows,supp_writ_rows]

def large_set(names,number_of_masses,times,readings,reads_per_mass):
    """Splits a large set into smaller ones and does the analysis on them."""
    writing_rows = []
    supp_writ_rows = []
    sigma = []
    
    cycles = len(readings)/int(reads_per_mass*number_of_masses)
    for cycle in range(cycles):
        start = cycle*reads_per_mass*number_of_masses
        end = (cycle+1)*reads_per_mass*number_of_masses
        #t_ for temporary
        t_times = times[start:end]
        t_readings = readings[start:end]

        #With the set split into subsets of cicular weighings,
        #each is seperately analysed. 
        t_writing_rows,t_supp_writ_rows,t_sigma = main_single_set(t_readings,number_of_masses,t_times,names)
        
        writing_rows.append(t_writing_rows)
        supp_writ_rows.append(t_supp_writ_rows)
    #This section of code is essentailly repeated later main_circ
    #under on_return.
    #Data is not very easily accesible here, and sigma is the average standard dev of each of the
    #differences. So all data needs to be read and dealth with.
    #A better data structure could be used instead maybe. 
    number = len(writing_rows[0])
    
    diff_cols = np.array(writing_rows)[:,:,2]
    for col in np.transpose(diff_cols):
        values = [float(c) for c in col]
        #FIRST READING IS SKIPPED
        #Should this be the case? It then prints the would-be sigma of the data,
        #but that is not the sigma for the entire reading set.
        sigma.append(np.std(values[1:]))
       
    return writing_rows,supp_writ_rows,sigma

def main_single_set(readings,number_of_masses,times,names,max_order=3):
    """For a single set, this function uses the other functions to produce the writing rows.
    It does the fit three times, linear, parabola, cubic and pics best option.
    Other orders of fit can be chosen by setting max_order."""
    #Create array of suffiient length
    writing_rows = [0]*max_order
    supp_writ_rows = [0]*max_order
    sigma = [0]*max_order
    
    for i in range(max_order): #For each order, do the fits.
        order_in_t = i+1
        M = generate_m(readings.size,number_of_masses,order_in_t,times)
        beta,covalent,dof,sigma[i] = analysis(M,readings,number_of_masses,order_in_t)
        writing_rows[i],supp_writ_rows[i] = differences(number_of_masses,order_in_t,beta,covalent,names)
    idx = sigma.index(min(sigma)) #Index of best fit (smallest residual)
    return writing_rows[idx],supp_writ_rows[idx],sigma[idx]

def unknown_set(names,number_of_masses,times,readings):
    """A function to deal with a set of unknown number of cycles."""
    #Find the number of reads per mass.
    if len(names) >= 5:
        reads_per_mass = 3
    else:
        reads_per_mass = 7 - len(names)
    
    if reads_per_mass*len(names) == len(readings):
        #Then we know that there is only one cycle.
        w,s,c = main_single_set(readings,number_of_masses,times,names)
        w = [w]
        s = [s]
        c = [c] #So it is the same format as before, but only one element in each array.
    elif float(len(readings))%float(reads_per_mass) == 0:
        #Then there are several cycles, large_set deals with it.
        w,s,c = large_set(names,number_of_masses,times,readings,reads_per_mass)
    else:
        print("Failed, error with dimensions of data.")
        return [],[],[]
    return w,s,c
    
def save(filename,writing_rows):
    """Given some filename and rows to write, simply dumbs all
    the rows to the csv file and saves."""
    with open("results_"+filename,'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(writing_rows)

def analyse_file(filename,order_in_t):
    """Manages the smaller funcitons, calculates M sends to analysis file and so on."""
    names,number_of_masses,times,readings = extract_file(filename)
    
    #Now M can be constructed, initialised as array of zeros.
    M = generate_m(readings.size,number_of_masses,order_in_t,times)
    beta,covalent,dof,sigma = analysis(M,readings,number_of_masses,order_in_t)
    print(sigma)
    writing_rows,supp_writ_rows = differences(number_of_masses,order_in_t,beta,covalent,names)
    return writing_rows

if __name__ == "__main__":
    filename = '2017.07.24.13.47.54_100A_100.csv'
    info = extract_file(filename)
    names,number_of_masses,times,readings = info
    w,s,c = unknown_set(names,number_of_masses,times,readings)
    print "Results: "
    for v in w: print v
    print "Constants: ", s
    print "sigma: ", c


    

