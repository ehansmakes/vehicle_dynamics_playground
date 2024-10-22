import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


# This is part of a vehicle dynamics library
# We will start simple with a bicycle model using linear tires
# Eventually we will add additional models as functions

# GLOBAL SETTINGS FOR PLOTS ----------------------------------------------------------
plt.style.use('dark_background')    # Set Plot 𝔸 𝔼 𝕊 𝕋 ℍ 𝔼 𝕋 𝕀 ℂ 𝕊 
fig, ax = plt.subplots()            # Create a figure containing a single Axes.


# GENERAL PARAMETERS -----------------------------------------------------------------

yaw_angle = np.deg2rad(0)      #radians; denoted as uppercase_psi
steer_angle = np.deg2rad(25)    #radians; denoted as lowercase_delta
vel_long = 3; 


# ADD Different Powertrain versions; we are modeling an AWD system 


yaw_rotation_matrix = np.array([[np.cos(yaw_angle), -np.sin(yaw_angle)],
                                [np.sin(yaw_angle), np.cos(yaw_angle)]])


# VEHICLE MODEL PARAMETERS (Bicycle) --------------------------------------------------

L = 324   #length between Front and Rear axles (millimeters)
C = 146.5     #center of mass - in reference to the Rear axle (millimeters)

## Rigid Body Cooridinate Setup 

rigid_body = np.array([[0,L,C],
                       [0,0,0]])                            # Rigid body x,y coordinates for: rear, front, center of gravity (in order)

rigid_body = np.matmul(yaw_rotation_matrix,rigid_body)      # This rotates the rigid body coordinates by the yaw angle

# TIRE MODEL PARAMETERS (Linear) -------------------------------------------------------

## General Parameters
rim_dia = 60                            # millimeters
section_height = 22.5                   # millimeters
section_width = 45                      # millimeters
tread_width = 45                        # millimeters
tire_dia = rim_dia + section_height     # millimeters

tire_coordinates = rigid_body[:, 0:2] - 0.5*np.array([[tire_dia,tire_dia],
                                                      [section_width,section_width]])

# Front Tire Model
tire_front = Rectangle(tire_coordinates[:,1], 
                      width = tire_dia,
                      height = section_width,
                      angle = np.rad2deg(yaw_angle + steer_angle),
                      rotation_point = 'center',
                      color = 'teal',
                      alpha = 0.5)

# Rear Tire Model
tire_rear = Rectangle(tire_coordinates[:,0],
                      width = tire_dia,
                      height = section_width,
                      angle = np.rad2deg(yaw_angle),
                      rotation_point = 'center',
                      color = 'teal',
                      alpha = 0.5)

# VEHICLE MODEL PLOT -------------------------------------------------------------

plt.axis((-L*0.25, L*1.25, -L*0.25, L*1.25))          # Plot Rigid Body
ax.add_patch(tire_front)                                # Plot the Front Tire Model
ax.add_patch(tire_rear)                                 # Plot the Rear Tire Model

ax.add_patch

plt.xlabel('Inertial Frame (X-Axis)')
plt.ylabel('Inertial Frame (Y-Axis)')
plt.title('Bicycle Model with Linear Tires')
plt.plot(rigid_body[0,:],rigid_body[1,:], rigid_body[0,2], rigid_body[1,2], 's')

x_new = [2, 3, 4, 5]
y_new = [2, 5, 10, 17]
plt.plot(x_new, y_new)

plt.show()