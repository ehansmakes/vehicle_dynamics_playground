
from moving_avg_filter import moving_avg_filter
from low_pass_filter import low_pass_filter
from g_h_filter import g_h_filter
from bayesian_filter import bayesian_filter
import numpy as np
import matplotlib.pyplot as plt
import csv
'''
# GIVEN DATA ------------------------------------------------------------------
weights = [158.0, 164.2, 160.3, 159.9, 162.1, 164.6,169.6, 167.4, 166.4, 171.0, 171.2, 172.6]
weights_actual = [160.0, 161.0, 162.0, 163.0, 164.0,165.0, 166.0, 167.0, 168.0, 169.0, 170.0, 171.0]

data = moving_avg_filter(data=weights, n=3)

plt.style.use('classic')
plt.grid(color ='k', linestyle='--')
plt.plot(weights,'o')
plt.plot(data)
plt.plot(weights_actual, '--')
plt.show()

print(data)
'''

# UPLOAD DATA FROM CSV --------------------------------------------------------
time = []
eRPM = []
eRPM_velocity = []
LIDAR_Vel = []
# Converting eRPM to velocity with no slip 
# Gear Ratio from Motor to Differential: 13:54 
# Differential ratio: 1:2.85 

eRPM_convert = (13/54) * (1/2.85) * (np.pi * 0.105 / 60)

with open("test_data\\summer_run_2.csv", "r") as csv_file:
   raw_data = csv.reader(csv_file)

   next(raw_data)

   for line in raw_data: 
       time.append(float(line[0]))
       eRPM.append(float(line[1]))
       eRPM_velocity.append(abs(float(line[1])*eRPM_convert))
       LIDAR_Vel.append(float(line[2]))

# APPLY g-h FILTER to GIVEN DATA ----------------------------------------------

data1 = moving_avg_filter(data=LIDAR_Vel, n=50)

data2 = low_pass_filter(data=LIDAR_Vel, alpha=.95)

data3 = g_h_filter(data=LIDAR_Vel, x_0 = 0 , dx = 0.5, g = .05, h =.005, dt = 0.05)

plt.style.use('bmh')
plt.grid(color ='k', linestyle='--')
plt.plot(time, LIDAR_Vel, linewidth=0.75)
plt.plot(time, data1, label="moving_avg", linewidth=3.0)
plt.plot(time, data2, label="low-pass", linewidth=3.0)
plt.plot(time, data3, label="g-h filter", linewidth=3.0)
# plt.plot(time, eRPM, '-')
plt.legend(loc="upper left")
plt.show()