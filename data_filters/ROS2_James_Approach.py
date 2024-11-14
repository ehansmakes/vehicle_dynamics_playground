import rclpy
import numpy as np

# NEW
import tf_transformations

from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from ackermann_msgs.msg import AckermannDriveStamped
from nav_msgs.msg import Odometry
class KalmanFilter(Node):
    def __init__(self):
        super().__init__('DARCEKF')    #Name of this script) 
        # Vehicle parameters (we'll use these later)
        self.L = 0.324 # Lenth between axles (m)
        self.Lr = 0.1465 # Length from back axle to center of mass (m)
        self.velocity_COM = 0.0
        self.steering_angle = 0.0
        self.current_pose_x = 0.0
        self.current_pose_y = 0.0
        self.current_heading = 0.0
        self.last_time_sec = None
        self.last_time_nsec = None
        # Subscribe to topics, create topic, pull last value of each within 0.05 seconds
        self.publisher = self.create_publisher(TwistStamped, '/KFestimate', 10)
        self.create_subscription(TwistStamped, '/CFVelocity', self.CF_callback, 10) # gives speed
        self.create_subscription(AckermannDriveStamped, '/ackermann_cmd', self.ackermann_callback, 10) #steering angle
        self.create_subscription(Odometry, '/pf/pose/odom', self.lidar_callback, 10) # Gives x y heading
        self.timer = self.create_timer(0.05, self.publish_kf_estimation)
        print("publishing prediction status to /KFEstimate ")
    def lidar_callback(self, msg):
        current_pose = msg.pose.pose
        current_time = msg.header.stamp
        self.current_pose_x = current_pose.position.x
        self.current_pose_y = current_pose.position.y

        # NEW
        self.current_heading = self.quaternion_to_yaw(current_pose.orientation)
       
        if self.last_time_sec is not None: # check if time has passed, if True, set up time stamp value for dt and call function to  predict state
            dt = (current_time.sec - self.last_time_sec) + (current_time.nanosec - self.last_time_nsec) * 1e-9
            self.predict_state(dt)
        self.last_time_sec = current_time.sec
        self.last_time_nsec = current_time.nanosec

    # NEW 
    def quaternion_to_yaw(self, orientation):
            quaternion = (
                orientation.x,
                orientation.y,
                orientation.z,
                orientation.w
            )
            euler = tf_transformations.euler_from_quaternion(quaternion)
            return euler[2]
    

    def ackermann_callback(self, msg):
        steering_angle_radians = msg.steering_angle
        self.steering_angle = steering_angle_radians * (180/np.pi)
    def CF_callback(self, msg):
        self.velocity_COM = msg.linear.x
    
    # Prediction state of the Kalman Filter
    def predict_state(self, dt):
        # Extract current state and inputs
        x_now = self.current_pose_x
        y_now = self.current_pose_y
        psi_now = self.current_heading * (180/np.pi)
        v = self.velocity_COM
        delta = self.steering_angle
        L = self.L
        Lr = self.Lr
        beta = np.arctan((Lr/L) * (np.tan(delta)))
        # Propogate state 1 time step forward with discretized EOMs
        x_next = x_now + (dt * v * (np.cos(psi_now + beta)))
        y_next = y_now + (dt * v * (np.sin(psi_now + beta)))
        psi_next = psi_now + (dt * ((v * np.cos(beta)) * (np.tan(delta) / L)))
        # Update the predicted state
        KF = TwistStamped()
        KF.header.stamp = self.get_clock().now().to_msg()
        KF.twist.linear.x = x_next
        KF.twist.linear.y = y_next
        KF.twist.linear.z = psi_next
        self.publisher.publish(KF)
def main(args=None):
    rclpy.init(args=args)
    node = KalmanFilter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()