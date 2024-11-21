# The following script is a generic moving average filter
# This script is heavily influenced by the lecture done by: 
# 'Kalman Filter for Beginners, Part 1 - Recursive Filters & MATLAB Examples' [2023]
# By Dr. Shane Ross 
#
# This is a first order low-pass filter
# This filter allows low frequencies to pass and filters out high frequencies (noise)
'''
NOTATION [GENERAL] ------------------------------------------------------------
'z' ----- Measurements (Sometimes literature use 'y')
'k' ----- Time Step (For example 'z_k' will be the measurement at time step 'k')
'x' ----- State 
'x_0' --- Initial state estimate
'x_est' - State estimate after passing through filter

NOTE: x_dot denotes our state 'x' derived in respect to time

NOTATION [g-h Filter] ---------------------------------------------------------
'data' -- Contains the data to be filtered
'alpha' - ranges from 0 to 1. Dicatates the strength of the low-pass filter. 
''' 

import numpy as np

def low_pass_filter(data, alpha):

    results =[] # This array stores the results
    x_est = 0 # Set the initial state estimate x_0 to 0 

    for z in data:

        x_est = alpha * x_est + (1-alpha) * z

        results.append(round(x_est,3))
    return np.array(results)