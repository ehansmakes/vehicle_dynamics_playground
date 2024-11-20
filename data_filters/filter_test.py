from moving_avg_filter import moving_avg_filter
import matplotlib.pyplot as plt
import csv
'''
# GIVEN DATA (Remove hashmarks if you want to use hard-coded data) 
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

# EXAMPLE ---------------------------------------------------------------------
# UPLOAD DATA FROM CSV --------------------------------------------------------
time = []
eRPM = []
LIDAR_Vel = []

with open("test_data\\summer_run_3.csv", "r") as csv_file:
   raw_data = csv.reader(csv_file)

   next(raw_data)

   for line in raw_data: 
       time.append(float(line[0]))
       eRPM.append(float(line[1]))
       LIDAR_Vel.append(float(line[2]))

# APPLY g-h FILTER to GIVEN DATA ----------------------------------------------
data = moving_avg_filter(data=LIDAR_Vel, n=10)

plt.style.use('classic')
plt.grid(color ='k', linestyle='--')
plt.plot(time, LIDAR_Vel, 'o')
plt.plot(time, data)
plt.plot(time, eRPM, '-')
plt.show()