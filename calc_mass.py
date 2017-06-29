"""
Python implementation of the least squares for the final mass analysis.
Buoyancy corrections not really working.
"""
import numpy as np #Numpy module will be used for fast handling of linear algebra
from numpy.linalg import inv
from numpy.linalg import norm
from numpy import dot
from numpy import transpose as tr
import csv
from decimal import Decimal

def extract_file(filename):
    """
    Given some filename, extract the useful information.
    That is, the masses measured, the differences taken
    (in terms of mass names), and the results for the differences.
    """
    rows = []
    with open(filename,'r') as f:
        reader = csv.reader(f,delimiter = ',')
        for row in reader:
            rows.append(row)
            
    named_diffs = []
    diffs = []
    masses = []
    uncert = []
    for row in rows[2:]:
        #First ensure there are no spaces:
        name = row[0].replace(" ","")
        sub_list = name.split('-') #Array of mass names.
        named_diffs.append(sub_list)
        #At this stage, name1+name2 is parsed as a single name, while:
        #name1-name2-name3 for example is split into seperate bits.
        diffs.append(float(row[1]))#Array of float differences.
        uncert.append(float(row[2]))
        masses = masses + [n for n in sub_list if n not in masses]
        #This list comprehension is equivalent to the set statement:
        #{all n such that n is in sublist, and not already in masses}
        #Masses is the unique list of mass names, no repetitions.
        #masses = sorted(masses) #Built in sorting function, alphabetical and numerical.
    return [named_diffs,diffs,masses,uncert]

def generate_m(named_diffs,diffs,masses):
    """
    Generates the M matrix that picks up masses form a list
    of masses and turns it into a list of differences.
    Only allows for one mass minus a few other, like A-B-C.
    Inputtin gthings such as A+B-C will not at this stage work,
    the plus sign is ignored.
    """
    shape = (len(diffs), len(masses))
    M = np.zeros(shape) #generate an array of zeros in memory.
    for i in range(len(diffs)): #i takes index of rows.
        sub_list = named_diffs[i]
        for k in range(len(sub_list)):
            idx = masses.index(sub_list[k])
            if k == 0:
                M[i][idx] = 1
            else:
                M[i][idx] = -1
    #Hand-inputted matrix only for testing:
    m = [
        [1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,-1,-1,0,-1,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,-1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,0,-1,-1,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,-1,-1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,1,0,-1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,-1,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,-1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1],
        [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]
        ]
    m = np.array(m)
    #"m" can be returned also.
    return M

def analysis(M,diffs,uncert):
    """
    Following the mathcad example in Tech proc MSLT.M.001.007.
    Matrix maths to do the least squares.
    """
    Y = np.array(diffs) #Ensure it is a numpy object.
    uncert = np.array(uncert)*0.000001

    psi_y = np.diag(uncert**2/norm(uncert**2)) #actuall thats the same.
    
    psi_b = inv( dot( tr(M), dot( inv(psi_y),M) ) )
    b = dot(psi_b, dot(tr(M), dot(inv(psi_y),Y)))
    R0 = (Y-dot(M,b))
    return [b,R0,psi_b]

def buoyancy_uncert(M,b,psi_bmeas):
    """
    Currenlty not working, (I think this is where the bug is).
    The results are a little off from the example, but analysis function
    works fine.
    """
    cnx = np.zeros(len(M))
    i = 0
    for row in M*M:
        if sum(row)>1:
            cnx[i] = 0 #zero for unknown
        else:
            cnx[i] = 1#1 for reference standard
        i+=1
    cmx = dot(tr(M),cnx)#create vector of affected comparisons
    cmx = [np.abs(c-1) for c in cmx]#make it 1 for unknown, 0 for reference standard.
    reluncert = 0.1
    Unbc = reluncert*b*cmx*1e-6
    psi_nbc = np.diag(Unbc**2) #diag is used to create a diagonal matrix here.
    psi_b = psi_bmeas+psi_nbc
    Ub = np.sqrt(np.diag(psi_b))#And here it returns the diagonal of a matrix.
    return[Ub,psi_b]

def save(filename,writing_rows):
    """Given some filename and rows to write, simply puts all
    the rows to the csv file and saves."""
    with open("results_"+filename,'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(writing_rows)

def analyse_file(filename):
    """Manages the smaller funcitons, calculates M sends to analysis file and so on."""
    named_diffs,diffs,masses,uncert = extract_file(filename)
    M = generate_m(named_diffs,diffs,masses)
    b,R0,psi_bmeas = analysis(M,diffs,uncert)
    Ub,psi_b = buoyancy_uncert(M,b,psi_bmeas)
    #print(tr(np.array([b,np.diag(psi_bmeas),Ub])))
    #print(R0)
    #print(sum(R0**2))
if __name__ == "__main__":
    d = analyse_file('1.csv')


    

