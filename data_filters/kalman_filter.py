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
      where 1 is our highest confidence, and 0 is our lowest.  
''' 

import numpy as np
from collections import namedtuple
gaussian = namedtuple('Gaussian', ['mean', 'var'])
gaussian.__repr__ = lambda s: '(={:.3f}, ²={:.3f})'.format(s[0], s[1])

def gaussian_multiply(g1, g2):
    mean = (g1.var * g2.mean + g2.var * g1.mean) / (g1.var + g2.var)
    variance = (g1.var * g2.var) / (g1.var + g2.var)
    return gaussian(mean, variance)

def predict(pos, movement):
    return gaussian(pos.mean + movement.mean, pos.var + movement.var)

def update(prior, likelihood):
    posterior = gaussian_multiply(likelihood, prior)
    return posterior

def kalman_filter(data, process_var, sensor_var, dt):

    results =[] # This array stores the results

    x = gaussian(0., 1.**2) # vehicles' velocity, N(0, 20**2)
    acceleration = 0.25
    process_model = gaussian(acceleration*dt, process_var) # displacement to add to x

    for z in data:
        prior = predict(x, process_model)
        likelihood = gaussian(z, sensor_var)
        x = update(prior, likelihood)
        results.append(x[1])
    return np.array(results)