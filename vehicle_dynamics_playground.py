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

yaw_angle = np.deg2rad(5)    #radians; denoted as uppercase_psi
steer_angle = np.deg2rad(60) #radians; denoted as lowercase_delta
vehicle_vel = 5              #speed in [m/s]


# VEHICLE MODEL PARAMETERS (Bicycle) --------------------------------------------------

L = 324    #length between Front and Rear axles (millimeters)
C = 146.5  #center of mass - in reference to the Rear axle (millimeters)

## Rigid Body Cooridinate Setup 

# Body Coordinate matrix for: 
# rear, front, center of gravity and center of rotation (respectively)
rigid_body = np.array([[0,L,C,0],
                       [0,0,0,1]])

# Velocity Coordinate matrix for:
# rear wheel, front wheel, and center of mass velocity
vel_matrix = np.array([[0,0,L,0,C,0],
                       [0,0,0,0,0,0]])                          

# SETTING UP CENTER OF ROTATION COORDINATES [In Vehicle Frame] -------------------------
if steer_angle == 0: 
    print("   STEERING ANGLE IS ZERO    ")
    print("-----------------------------")
    print("NO CENTER OF ROTOTATION FOUND")
    exit()

elif steer_angle >= np.deg2rad(90) or steer_angle <= np.deg2rad(-90):
    print("oops")
    exit()

else:
    rigid_body[1,3] = L / (np.tan(steer_angle))

# Rotate Coordinates to Set Up Model in Inertial Frame

yaw_rotation_matrix = np.array([[np.cos(yaw_angle), -np.sin(yaw_angle)],
                                [np.sin(yaw_angle), np.cos(yaw_angle)]])

rigid_body = np.matmul(yaw_rotation_matrix,rigid_body)      # This rotates the rigid body coordinates by the yaw angle
vel_matrix = np.matmul(yaw_rotation_matrix,vel_matrix)

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

# VARIABLE CHECK ----------------------------------------------------------------
print()
print("------------------------")
print(rigid_body)

# Radias of Curvature 
# Radius of Curvature of Rear Axle 

# Velocity at CoM 
# Body Slip Angle (body_slip_angle)
OA = [rigid_body[0,0]-rigid_body[0,3],rigid_body[1,0]-rigid_body[1,3]]
OC = [rigid_body[0,2]-rigid_body[0,3],rigid_body[1,2]-rigid_body[1,3]]

body_slip_angle = np.arccos(np.dot(OA,OC)/(np.linalg.norm(OA)*np.linalg.norm(OC)))

print(np.rad2deg(body_slip_angle))


# VEHICLE MODEL PLOT -------------------------------------------------------------
reference_lines = True                                  # Turn refence line on (True) or off (False)

plt.axis((-C*0.75, C*3, -C*.75, C*3))            # Plot Rigid Body
ax.add_patch(tire_front)                                # Plot the Front Tire Model
ax.add_patch(tire_rear)                                 # Plot the Rear Tire Model

ax.add_patch

plt.xlabel('X-Axis Inertial Frame (mm)')
plt.ylabel('Y-Axis Inertial Frame (mm)')
plt.title('Bicycle Model with Linear Tires')

# Plot Rigid Body Model
plt.plot(rigid_body[0,0:2],rigid_body[1,0:2], "-")

# Plot Center of Gravity 
plt.plot(rigid_body[0,2], rigid_body[1,2],"o")

# Plot Center of Rotation
plt.plot(rigid_body[0,3], rigid_body[1,3],"ro")

# Plot Reference Lines
if reference_lines: 
    plt.plot([rigid_body[0,0], rigid_body[0,3]], [rigid_body[1,0], rigid_body[1,3]],"r--")
    plt.plot([rigid_body[0,1], rigid_body[0,3]], [rigid_body[1,1], rigid_body[1,3]],"r--")

    plt.plot([rigid_body[0,2], rigid_body[0,3]], [rigid_body[1,2], rigid_body[1,3]],"y--")
    plt.arrow(vel_matrix[0,4], vel_matrix[1,4], 20, 20, 
          head_width = 5,
          width = 1.5,
          ec ='yellow')
    
plt.show()