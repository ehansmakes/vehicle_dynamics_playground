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

NOTATION [g-h Filter] ---------------------------------------------------------
'data' -- Contains the data to be filtered
'dx' ---- The initial change rate for our state variable
'dt' ---- The length of the time step
'g' ----- The g-h's g scale factor
'h' ----- The g-h's h scale factor

NOTE: "g is the scaling we use for the measurement"
      "h is the scaling for the change of meausurement" 
      
      We can consider these values as our confidence level for measured values.
      where 1 is our highest confidence.  
''' 

import matplotlib.pyplot as plt
import numpy as np
import csv


def g_h_filter(data, x_0, dx, g, h, dt):

    x_est = x_0 #State Estimate using initial values 
    results =[] # This array stores the results

    for z in data: 

        # PREDICTION STEP -----------------------------------------------------
        x_pred = x_est + (dx*dt)
        dx = dx

        # UPDATE STEP ---------------------------------------------------------
        residual = z - x_pred 
        dx = dx + h * (residual) / dt
        x_est = x_pred + g * residual
        results.append(round(x_est,3))
    return np.array(results)