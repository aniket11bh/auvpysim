#
# (c) PySimiam Team 2013
# 
# Contact person: Tim Fuchs <typograph@elec.ru>
#
# This class was implemented for the weekly programming excercises
# of the 'Control of Mobile Robots' course by Magnus Egerstedt.
#
from controller import Controller
import math
import numpy
from fuzzy import Fuzzy

############### fuzzy subset for trimf
f_ssets = [[
            [-60,-60,-30], # -ve medium   
            [-60,-30 , 0], # -ve small
            [-30, 0  ,30], # zero
            [ 0 , 30 ,60], # +ve small
            [ 30, 60 ,60], # +ve medium
           ],        
            # delta_error
           [          
            [-45,-45,-10], # -ve medium   
            [-45,-10 , 0], # -ve small
            [-10, 0  ,10], # zero
            [ 0 , 10 ,45], # +ve small
            [ 10, 45 ,45], # +ve medium
           ],              
            # u
           [                 
            [-3,-3,-1],  # -ve medium
            [-3,-1 , 0],  # -ve small
            [-1, 0 ,1],  # zero
            [ 0 ,1 ,3], # +ve small
            [ 1 ,3 ,3], # +ve medium
           ] 
          ]
# yapf: enable

io_ranges = [  # range of e
              [-180,180],
               # range of d_e
              [-180,180],
               # range of u
              [-5,5]
            ]

mf_types = ['trimf','trimf','trimf']

################## fuzzy subset for gaussmf

# f_ssets = [[ # error
#             [-180,70], # -ve medium   
#             [-50,20], # -ve small
#             [ 0 ,20], # zero
#             [50 ,20], # +ve small
#             [180 ,70], # +ve medium
#            ],        
#             # delta_error
#            [          
#             [-180,70], # -ve medium   
#             [-50,20], # -ve small
#             [ 0 ,20], # zero
#             [50 ,20], # +ve small
#             [180 ,70], # +ve medium
#            ],              
#             # u
#            [                 
#             [-3,2], # -ve medium   
#             [-1,2], # -ve small
#             [ 0,1], # zero
#             [ 1,2], # +ve small
#             [ 3,2], # +ve medium           
#            ] 
#           ]
# # yapf: enable

# io_ranges = [  # range of e
#               [-180,180],
#                # range of d_e
#               [-180,180],
#                # range of u
#               [-10,10]
#             ]
# mf_types = ['gaussmf','gaussmf','gaussmf']


class GoToGoal(Controller):
    """Go-to-goal steers the robot to a predefined position in the world."""
    def __init__(self, params, yaw = Fuzzy(mf_types, f_ssets)):
        '''Initialize some variables'''
        
        Controller.__init__(self,params)
        self.heading_angle = 0
        self.yaw = yaw

    def set_parameters(self, params):
        """Set PID values
        
        The params structure is expected to have in the `gains` field three
        parameters for the PID gains.
        
        :param params.gains.kp: Proportional gain
        :type params.gains.kp: float
        :param params.gains.ki: Integral gain
        :type params.gains.ki: float
        :param params.gains.kd: Differential gain
        :type params.gains.kd: float
        """
        self.kp = params.gains.kp
        self.ki = params.gains.ki
        self.kd = params.gains.kd

    def restart(self):
        #Week 3 Assignment Code:
        #Place any variables you would like to store here
        #You may use these variables for convenience
        self.E_k = 0 # Integrated error
        self.e_k_1 = 0 # Previous error calculation
        
        #End Week 3 Assigment

    def get_heading_angle(self, state):
        """Get the heading angle in the world frame of reference."""
        
        #Insert Week 3 Assignment Code Here
        # Here is an example of how to get goal position
        # and robot pose data. Feel free to name them differently.
        
        x_g, y_g = state.goal.x, state.goal.y
        x_r, y_r, theta = state.pose

        theta_d = math.atan2((y_g - y_r), (x_g - x_r))
        
        return theta_d
        #End Week 3 Assigment        

    def execute(self, state, dt):
        """Executes avoidance behavior based on state and dt.
        state --> the state of the robot and the goal
        dt --> elapsed time
        return --> unicycle model list [velocity, omega]"""
        
        self.heading_angle = self.get_heading_angle(state)
        self.yaw.io_ranges = io_ranges

        #Insert Week 3 Assignment Code Here
        
        # error between the heading angle and robot's angle
        x_r, y_r, theta = state.pose
        e_k = self.heading_angle - theta;
        e_k = numpy.arctan2(numpy.sin(e_k),numpy.cos(e_k))* 180 / numpy.pi
        # e_k = numpy.arctan2(numpy.sin(e_k),numpy.cos(e_k))

        # error for the proportional term
        self.yaw.error = e_k
        
        # error for the integral term. Hint: Approximate the integral using
        # the accumulated error, self.E_k, and the error for
        # this time step, e_k.
        e_I = (self.E_k + e_k)*dt
                    
        # error for the derivative term. Hint: Approximate the derivative
        # using the previous error, obj.e_k_1, and the
        # error for this time step, e_k.
        self.yaw.delta_e = (e_k - self.e_k_1)/dt
        w_ = self.yaw.run() 
        print "output : ",w_,"Error : ",e_k

        # w_ = self.kp*e_P+ self.ki*e_I + self.kd*e_D
        
        v_ = state.velocity.v
        
        # save errors
        self.e_k_1 = e_k
        self.E_k = e_I
        
        #End Week 3 Assignment
        
        return [v_, w_]