# The following script is a generic g-h algorithm used for reference in future filters
# This script is heavily influenced by the 
'''
NOTATION [GENERAL] ------------------------------------------------------------
'z' ----- Measurements (Sometimes literature use 'y')
'k' ----- Time Step (For example 'z_k' will be the measurement at time step 'k')
'x' ----- State 
'x_0' --- Initial state estimate

NOTE: x_dot denotes our state 'x' derived in respect to time

NOTATION [Low-Pass Filter] ----------------------------------------------------
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


def moving_average_filter(data, x_0, dx, g, h, dt):

    x_est = x_0 #State Estimate
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


# EXAMPLE ---------------------------------------------------------------------
# UPLOAD DATA FROM CSV --------------------------------------------------------
time = []
weights = []
weights_actual = []

with open('test_data\\sample_data_weight.csv', "r") as csv_file:
   raw_data = csv.reader(csv_file)

   next(raw_data)

   for line in raw_data: 
       time.append(float(line[0]))
       weights.append(float(line[1]))
       weights_actual.append(float(line[2]))

# GIVEN DATA (Remove hashmarks if you want to use hard-coded data) 
# weights = [158.0, 164.2, 160.3, 159.9, 162.1, 164.6,
#           169.6, 167.4, 166.4, 171.0, 171.2, 172.6]
# weights_actual = [160.0, 161.0, 162.0, 163.0, 164.0,165.0, 166.0, 167.0, 168.0, 169.0, 170.0, 171.0]


# APPLY g-h FILTER to GIVEN DATA ----------------------------------------------
data = g_h_filter(data=weights, x_0=160., dx=1., g=6./10, h=2./3, dt=1.)

print(weights)
print("")
print(data)

plt.style.use('classic')
plt.grid(color ='k', linestyle='--')
plt.plot(time, weights,'o')
plt.plot(time, data)
plt.plot(time, weights_actual, '--')
plt.show()