"""
Python implementation of the circular weighing algorithm.
"""
import numpy as np #Numpy module will be used for fast handling of linear algebra
from numpy.linalg import inv
import csv

filename = 'verification.csv'
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

order_in_t = int(raw_input("Order in t: ")) #Order of 2 includes quadratic terms in time.

#Now M can be constructed, initialised as array of zeros.
shape = (readings.size, number_of_masses+order_in_t)
M = np.zeros(shape)
#Now populate M with t, t squarred etc...
for i in range(order_in_t):
    M[:,-i-1] = times**(order_in_t-i)
#And with diagonal 1s to pick up the masses.
for i in range(len(times)):
    row = i
    col = i%number_of_masses
    M[row,col] = 1

m_t_m = np.dot(np.transpose(M),M)
A= np.dot(inv(m_t_m),np.transpose(M))
beta = np.dot(A,readings)

y_minus_xb = readings-np.dot(M,beta)
dof = len(readings) - number_of_masses - order_in_t
sigma_squarred = np.dot(np.transpose(y_minus_xb),y_minus_xb)/dof

covalent_matrix = sigma_squarred*inv(m_t_m)

writing_rows = [["Masses","Difference","1 std"]] #Rows to write to the results file.
for i in range(number_of_masses):
    for j in range(i+1,number_of_masses):
        diff = beta[i]-beta[j]
        error_squared = covalent_matrix[i,j]+covalent_matrix[j,i]
        error = np.sqrt(error_squared)
        writing_row = ["{}-{}".format(names[i],names[j]),diff,error]
        #writing_row = "{} - {},{} +/- {}\n".format(names[i],names[j],diff,error)
        writing_rows.append(writing_row)
        print(writing_row)
for i in range(order_in_t):
    writing_row = ["d_{}".format(i+1),beta[i+number_of_masses]]
    #Need to know the uncertainty of these bits too, somehow from the diagonal?
    writing_rows.append(writing_row)
    print(writing_row)

with open("results_"+filename,'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(writing_rows)
    
    
