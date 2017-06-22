"""
Python implementation of the circular weighing algorithm.
"""
import numpy as np #Numpy module will be used for fast handling of linear algebra
from numpy.linalg import inv

#All arrays will be numpy objects
#simulated readings list, really it should be read from a GUI or data file.
readings = np.array([
    22.1, 743.7, 3080.4, 4003.4,\
    18.3, 739.2, 3075.5, 3998.2,\
    14.2, 734.7, 3071.6, 3994.8])
times = np.arange(len(readings))*0.01 #Needs to be the same length, that is all.
number_of_masses = 4 #Any number, Could it be interpreted form the number of columns in readings?
order_in_t = 2 #Order of 1 corresponds to linear terms.
#The order governs how many constants are estimated, in this case 2.

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
beta = np.dot(np.dot(inv(m_t_m),np.transpose(M)),readings)

y_minus_xb = readings-np.dot(M,beta)
dof = len(readings) - number_of_masses - order_in_t
sigma_squarred = np.dot(np.transpose(y_minus_xb),y_minus_xb)/dof

covalent_matrix = sigma_squarred*inv(m_t_m)

#generate w vectors, for each vector print mass diff and uncertainty.
#Notice that the total number of printing points is 0.5*N!/(N-1)!:
for i in range(number_of_masses):
    for j in range(i+1,number_of_masses):
        diff = beta[i]-beta[j]
        error_squared = covalent_matrix[i,j]+covalent_matrix[j,i]
        error = np.sqrt(error_squared)
        print("Mass_{} - Mass_{} : {} +/- {}".format(i+1,j+1,diff,error))
