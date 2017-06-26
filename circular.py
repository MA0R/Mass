"""
Python implementation of the circular weighing algorithm.
Functions here can be used for any other similar regression analysis.
"""
import numpy as np #Numpy module will be used for fast handling of linear algebra
from numpy.linalg import inv
import csv

def generate_m(num_readings,num_masses,order_in_t,times=None):
    """Generates matrix M based on number of readings,
    number of measured objects, order of time polynomial
    and the measurement times."""
    if times == None: #Fill time as simple ascending array, [1,2,3..]
        times = np.arrange(num_readings)
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
        floats = [float(m) for m in row]
        temp_mass = []
        for i in range(len(floats)): #not a very nice line but need to know if i is even or odd
            if i%2 == 1:
                masses.append(floats[i])
            else:
                times.append(floats[i])
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
    for t in [1,2,3,4]:
        d = analyse_file('verification3.csv',t)
        for a in d:
            print a
        print


    

