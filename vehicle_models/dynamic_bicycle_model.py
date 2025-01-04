import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


# This script provides a general overview of the Dynamic Bicycle Model 

# REFERENCE LIST -----------------------------------------------------------------------
# HowDynamic, Lec 03 | Vehicle Dynamics | Kinematic Bicycle (part 2 - derivation)
# (https://youtu.be/I9Myqu6GgAQ?si=7OBfDNqUK1y3qdxy)
# HowDynamic, Lec 02 Vehicle Dynamics | Kinematic Bicycle Model (Part 1)
# (https://youtu.be/d4WW-Fcm4_k?si=mf04h-CnUQ3IAK1M)
# Prof. Georg Schildbach, University of Luebeck, Vehicle Dynamics & Control - 05 Kinematic bicycle model
# (https://www.youtube.com/watch?v=HqNdBiej23I)

# GLOBAL SETTINGS FOR PLOTS ------------------------------------------------------------
print_out = True                    # Prints out values from EOM (Inertial Frame)
reference_lines = True              # Turn refence line on (True) or off (False)


# STATE PARAMETERS ---------------------------------------------------------------------

yaw_angle = np.deg2rad(30)    #radians; denoted as uppercase_psi
steer_angle = np.deg2rad(20) #radians; denoted as lowercase_delta
vehicle_vel = 5              #vehicle speed in (m/s)


# VEHICLE MODEL PARAMETERS (Bicycle) ---------------------------------------------------

L = 324    #length between Front and Rear axles (millimeters)
C = 146.5  #center of mass - in reference to the Rear axle (millimeters)

body_slip_angle = np.arctan(C*np.tan(steer_angle)/L)

# Rigid Body Coordinate matrix for: 
# rear, front, center of gravity and center of rotation (respectively by column)
rigid_body = np.array([[0,L,C,0],
                       [0,0,0,1]])                        


# FINDING THE CENTER OF ROTATION COORDINATES [In Vehicle Frame] ------------------------

if steer_angle == 0: 
    print("   STEERING ANGLE IS ZERO    ")
    print("-----------------------------")
    print("NO CENTER OF ROTOTATION FOUND")
    exit()

elif steer_angle >= np.deg2rad(90) or steer_angle <= np.deg2rad(-90):
    print("STEERING ANGLE IS OVER 90 deg")
    print("-----------------------------")
    print("NO CENTER OF ROTOTATION FOUND")
    exit()

else:
    rigid_body[1,3] = L / (np.tan(steer_angle))


# Set Up Velocity Coordinate matrix from the Center of Mass ----------------------------
# rear wheel, front wheel, and center of mass velocity
vel_matrix = np.array([[C,0],
                       [0,0]])  

vel_matrix[0,1] = vehicle_vel*np.cos(body_slip_angle)
vel_matrix[1,1] = vehicle_vel*np.sin(body_slip_angle)


# ROTATION MATRIX SETUP =--------------------------------------------------------------

yaw_rotation_matrix = np.array([[np.cos(yaw_angle), -np.sin(yaw_angle)],
                                [np.sin(yaw_angle), np.cos(yaw_angle)]])

# Rotates the rigid body coordinate and velocity matrices using the yaw rotation matrix
rigid_body = np.matmul(yaw_rotation_matrix,rigid_body)     
vel_matrix = np.matmul(yaw_rotation_matrix,vel_matrix)


# TIRE MODEL PARAMETERS (Linear) -------------------------------------------------------

## General Parameters
rim_dia = 60                            # (millimeters)
section_height = 22.5                   # (millimeters)
section_width = 45                      # (millimeters)
tread_width = 45                        # (millimeters)
tire_dia = rim_dia + section_height     # (millimeters)

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


# CALCULATE KINEMATIC BICYCLE MODEL EQUATIONS OF MOTIONS -------------------------------

x_dot = vehicle_vel*np.cos(yaw_angle+body_slip_angle)
y_dot = vehicle_vel*np.sin(yaw_angle+body_slip_angle)
yaw_rate = vehicle_vel*np.cos(body_slip_angle)*np.tan(steer_angle)/L

if print_out:
    print("       Equation of Motion Calculations       ")
    print("---------------------------------------------")
    print ("Velocity [Inertial Frame x-axis]: ", round(x_dot, 2), "(m/s)")
    print ("Velocity [Inertial Frame y-axis]: ", round(y_dot, 2), "(m/s)")
    print ("Yaw Rate: ", round(np.rad2deg(yaw_rate), 2), "(deg)")
    print("---------------------------------------------")


# VEHICLE MODEL PLOT -------------------------------------------------------------------

plt.style.use('dark_background')    # Set Plot 𝔸 𝔼 𝕊 𝕋 ℍ 𝔼 𝕋 𝕀 ℂ 𝕊 
fig, ax = plt.subplots()            # Create a figure containing a single axis.
plt.gca().set_aspect('equal')       # Sets axis equal (this avoids distortion)
plt.axis("equal")                  # Plot Rigid Body
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
    # Plot the radii about the center of rotation at the rear wheel, front wheel and center of mass (respectively)
    plt.plot([rigid_body[0,0], rigid_body[0,3]], [rigid_body[1,0], rigid_body[1,3]],"r--")
    plt.plot([rigid_body[0,1], rigid_body[0,3]], [rigid_body[1,1], rigid_body[1,3]],"r--")
    plt.plot([rigid_body[0,2], rigid_body[0,3]], [rigid_body[1,2], rigid_body[1,3]],"y--")

    # Plot the velocity vector about the center of mass (the vector is amplified by 10 for visibility)
    plt.arrow(vel_matrix[0,0], vel_matrix[1,0], vel_matrix[0,1]*10, vel_matrix[1,1]*10, 
          head_width = 5,
          width = 1.5,
          ec ='yellow')

plt.show()