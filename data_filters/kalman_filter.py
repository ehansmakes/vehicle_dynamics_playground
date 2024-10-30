import numpy as np

# AUTHOR'S NOTES -----------------------------------------------------------------------

# Design the KF 

# goal: estimate x, v (position and velocity) given measurement z = x + R_k

# x_bar_k = [[x_k],[v_k]]  # The bar suffix indicates the estimate matrix[v_k]]

# z_bar_k = [z_k]    # The bar suffix indicates the measurement matrix 

# TIME EVOLUTION
# NOTE: t_Step can also be delta_t

# x_k1 = x_k + v_k*t_step + 0.5 * a * t_step^2 
# v_k1 = v_k + a * t_step 

# Let's get this into matrix form! (Denoted by 'bar')

#                   F                              B
# x_bar_k1 = [[1, t_step],[0, 1]]*x_bar_k + [[0.5 * t_step^2],[t_step]] * a

# we assume 'a' is constant and a normally distributed random variable with mean = 0 

# MEASUREMENT UPDATE
# z_k = x_k + R_k 
#             H
# z_bar_k = [1,0]*x_bar_k + R_bar_k 

# How can we go from x_bar_k to x_bar_k1

# PREDICTION STEP 
# We calculate the mean (x_bar_hat) and covariance (P)

# we are using the covariance between the measured state and estimate 
'''
▛~~~~~~~~~~~~~~~~~~~~~~~~▜
  Kalman Predict Equations
▙~~~~~~~~~~~~~~~~~~~~~~~~▟

x_bar_hat_k1 = F * x_bar_hat_k 
P_k1 = F* P_k * F.T + B * variance_a^2 * B.T 

'''

# MEASUREMENT STEP (incorporate the knowledge of the measurement z_k into our estimate x_bar_k


# REFERENCE LIST -----------------------------------------------------------------------
# CppMonk, Understanding & Code a Kalman Filter: Python and C++ 
# (https://www.youtube.com/playlist?list=PLvKAPIGzFEr8n7WRx8RptZmC1rXeTzYtA) 
# 
#
# LINEAR DYNAMIC SYSTEM MODEL SETUP ----------------------------------------------------

class Kalman_Filter: 
    def __init__(self, F_k, B_k, H_k, Q_k, R_k, x_0, P_0):
        self.F_k = F_k      # The state-transition model
        self.B_k = B_k      # The control input model (if there is control)
        self.H_k = H_k      # The observation model 
        self.Q_k = Q_k      # The covariance of the process noise ░▒▓
        self.R_k = R_k      # The covatiance of the measurement noise ░▒▓ 
        self.x_k = x_0      # Initial conditions for state estimate mean 
        self.P_k = P_0      # Initial conditions for covariance matrix estimate 

    # Note: 
    # We assume measurement noise to be zero mean Guassian white noise with covariance R_k


    # PREDICTION STEP ------------------------------------------------------------------
    # We calculate the mean (x_bar_hat) and covariance (P)
    def predict(self, u_k): 
        
        # Predict state estimate mean
        self.x_k = np.dot(self.F_k, self.x_k) + np.dot(self.B_k,u_k)

        # Predict estimate covariance 
        self.P_k = np.dot(np.dot(self.F_k, self.P_k), np.transpose(self.F_k)) + self.Q_k

        return self.x_k   # This is our predicted value of x_k 


    # UPDATE STEP ----------------------------------------------------------------------
    # We calculate the mean (x_bar_hat) and covariance (P)
    def update(self, z_k):
        
        # Innovation; the difference between the observed value of a variable at time t
        # and the optimal forecast if that value based on information available prior to
        # time t. 
        y_k = z_k - np.dot(self.H_k, self.x_k)

        # Innovation (or pre-fit residual) covariance
        S_k = np.dot(np.dot(self.H_k, self.P_k), np.transpose(self.H_k)) + self.R_k

        # Optimal Kalman gain 
        K_k = np.dot(np.dot(self.P_k, np.transpose(self.H_k)), np.linalg.inv(S_k))

        # Update state estimate given updated Innovation (y_k), and Kalman gain (K_k) 
        self.x_k = self.x_k + np.dot(K_k,y_k)
        
        # Update estimate covariance
        # Note, change the identity matrix accounding 
        self.P_k = np.dot((np.identity(self.P_k.shape[0])- np.dot(K_k, self.H_k)), self.P_k)

        return self.x_k

# Example usage
F = np.array([[1, 1], [0, 1]])
B = np.array([[0.5], [1]])
H = np.array([[1, 0]])

# Q = np.array([[1, 0], [0, 1]]) 
Q = np.array([[0, 0], [0, 0]])
R = np.array([[1]])

# Initial state and covariance
x0 = np.array([[0], [1]]) 
P0 = np.array([[1, 0], [0, 1]]) 

# Create Kalman Filter instance
kf = Kalman_Filter(F, B, H, Q, R, x0, P0)
# Predict and update with the control input and measurement
u = np.array([[1]])  
z = np.array([[1]]) 

# Predict step
predicted_state = kf.predict(u)
print("Predicted state:\n", predicted_state)
# Update step
updated_state = kf.update(z)
print("Updated state:\n", updated_state)