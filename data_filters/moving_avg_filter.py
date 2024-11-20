# The following script is a generic moving average filter
# This script is heavily influenced by the lecture done by: 
# 'Kalman Filter for Beginners, Part 1 - Recursive Filters & MATLAB Examples' [2023]
# By Dr. Shane Ross
#
# NOTE: 

'''
NOTATION [GENERAL] ------------------------------------------------------------
'z' ----- Measurements (Sometimes literature use 'y')
'k' ----- Time Step (For example 'z_k' will be the measurement at time step 'k')
'x' ----- State 
'x_est' - State estimate generated by moving average

NOTE: x_dot denotes our state 'x' derived in respect to time

NOTATION [g-h Filter] ---------------------------------------------------------
'data' -- Contains the data to be filtered
'n' ----- The number of samples used for the moving average filter
'x_bar' - The average over 'sample' amount of data points
''' 

import matplotlib.pyplot as plt
import numpy as np
import csv


def moving_avg_filter(data, n):

    n_array = [] # Raw data array that is used to calculate average
    results =[] # This array stores the results

    for z in data:

        if len(n_array) < n: 
            n_array = np.append(z, n_array)
            x_est = np.average(n_array)
        else:
            n_array = np.append(z, n_array[0:-1])
            x_est = np.average(n_array)

        results.append(round(x_est,3))
    return np.array(results)