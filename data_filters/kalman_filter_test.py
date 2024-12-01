import matplotlib.pyplot as plt
import numpy as np
import csv
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

'''
def update_car(car_vel, measurement):
    estimated_vel = gaussian_multiply(measurement, car_vel)
    return(estimated_vel)
'''

predicted_pos = gaussian(0., 0.5**2)
measured_pos = gaussian(0., 2.0**2)
estimated_pos = update(predicted_pos, measured_pos)
print(estimated_pos)


#---------------------------------
# First Kalman Filter Variables

process_var = 0.25  # variance in the cars's movement
sensor_var = 150.0  # variance in the sensor measurements 

x = gaussian(0., 1.**2) # vehicles' velocity, N(0, 20**2)
acceleration = 0.25
dt = 0.05 # time step in seconds
process_model = gaussian(acceleration*dt, process_var) # displacement to add to x

# get measurements 
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


# Here is the Kalman Filter!!!! 

results =[] # This array stores the results
filter_variance = [] # The variance of the Kalmnan Filter prediction 
                     # This should converge to near-zero 

# perform Kalman filter on measurement z
for z in LIDAR_Vel:
    prior = predict(x, process_model)
    likelihood = gaussian(z, sensor_var)
    x = update(prior, likelihood)
    results.append(x[0])


print(results)



#PLOT RESULTS -----------------------------------------------------------------
plt.style.use('dark_background')
plt.grid(color ='k', linestyle='--')
plt.plot(time, LIDAR_Vel, linewidth=0.75,alpha=0.4)
plt.plot(time, results, label="kalman filter", linewidth=3.0,)
plt.legend(loc="upper left")
#figure, axis = plt.subplots(1,1)
#plt.plot(time, filter_variance, label="filter_variance", linewidth=3.0,)
plt.show()