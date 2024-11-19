# The following script is a generic g-h algorithm used for reference in future filters
# This script is heavily influenced by the textbook: 
# 'Kalman and Bayesian Filters in Python' by Roger R Labb Jr. (2020)

'''
NOTATION [GENERAL] ------------------------------------------------------------
'z' ----- Measurements (Sometimes literature use 'y')
'k' ----- Time Step (For example 'z_k' will be the measurement at time step 'k')
'x' ----- State 
'x_0' --- Initial state estimate

NOTE: x_dot denotes our state 'x' derived in respect to time

NOTATION [Bayesian Filter] ----------------------------------------------------
'belief'   
'data' -- Contains the data to be filtered


NOTE: 
''' 

import matplotlib.pyplot as plt
import numpy as np
import csv

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

def scaled_update(hall, belief, z, z_prob):
    scale = z_prob / (1. - z_prob)
    belief[hall==z] *= scale



# Textbook Example 

# system setup, where 1 represents a doorway and 0 represents a wall
hallway = np.array([1, 1, 0, 0, 0, 0, 0, 0, 1, 0])

belief = np.array([0.1] * 10)

scaled_update(hallway, belief, z=1, z_prob=.75) 

belief = belief / sum(belief)


print('sum =', sum(belief))

print('probability of door =', belief[0])
print('probability of wall =', belief[2])