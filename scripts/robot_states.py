#!/usr/bin/env python
"""
.. module:: robot_states
	:platform: Unix
	:synopsis: Python code for interface of the modalities
	
.. moduleauthor:: Awais Tahir <awaistahir29@gmail.com>

This node implements the robot state for controlling the robot in the environment.

Services:
- GetPose
- SetPose
- GetBattery
- SetBattery
"""


import threading
import random
import rospy
# Import constant name defined to structure the architecture.
from survailence_robot import architecture_name_mapper as anm
# Import the messages used by services and publishers.
from std_msgs.msg import Bool
from survailence_robot.srv import GetPose, GetPoseResponse, SetPose, SetPoseResponse, GetBattery, SetBattery, GetBatteryResponse, SetBatteryResponse
from survailence_robot.msg import Point


# A tag for identifying logs producer.
LOG_TAG = anm.NODE_ROBOT_STATE


# The node manager class.
# This class defines two services to get and set the current 
# robot pose, and a publisher to notify that the battery is low. 
class RobotState:
    """
The node manager class. This class defines two services to get and set the current robot pose, and a publisher to notify that the battery is low. Also additional services to get and set battery level.
    """
    def __init__(self):
    """
    Initializeing the module getting the parameters from the parameter server, the initial position x and y. Also setting the battery level to 20.
    """
    
        # Initialise this node.
        rospy.init_node(anm.NODE_ROBOT_STATE, log_level=rospy.INFO)
        # Initialise robot position.
        self._pose = Point()
        point_param = rospy.get_param("/state/initial_pose")
        self._pose.x = point_param[0]
        self._pose.y = point_param[1]

        # Robot Battery Level
        self._battery_level = 20
        

        # Define services.
        rospy.Service(anm.SERVER_GET_POSE, GetPose, self.get_pose)
        rospy.Service(anm.SERVER_SET_POSE, SetPose, self.set_pose)
        rospy.Service(anm.SERVER_GET_BATTERY, GetBattery, self.get_battery)
        rospy.Service(anm.SERVER_SET_BATTERY, SetBattery, self.set_battery)
        # Log information.
        log_msg = (f'Initialise node `{anm.NODE_ROBOT_STATE}` with services `{anm.SERVER_GET_POSE}` and '
                   f'`{anm.SERVER_SET_POSE}`, and topic {anm.SERVER_GET_BATTERY}, and topic {anm.SERVER_SET_BATTERY}.')
        rospy.loginfo(anm.tag_log(log_msg, LOG_TAG))

    # The `robot/set_pose` service implementation.
    # The `request` input parameter is the current robot pose to be set,
    # as given by the client. This server returns an empty `response`.
    def set_pose(self, request):
    """
    Function to set the position
    """
        if request.pose is not None:
            # Store the new current robot position.
            self._pose = request.pose
            # Log information.
            log_msg = (f'Set current robot position through `{anm.SERVER_SET_POSE}` '
                             f'as ({self._pose.x}, {self._pose.y}).')
            rospy.loginfo(anm.tag_log(log_msg, LOG_TAG))
        else:
            rospy.logerr(anm.tag_log('Cannot set an unspecified robot position', LOG_TAG))
        # Return an empty response.
        return SetPoseResponse()

    # The `robot/get_pose` service implementation.
    # The `request` input parameter is given by the client as empty. Thus, it is not used.
    # The `response` returned to the client contains the current robot pose.
    def get_pose(self, response):
    """
    Function to get the position
    """
        # Log information.
        if self._pose is None:
            rospy.logerr(anm.tag_log('Cannot get an unspecified robot position', LOG_TAG))
        else:
            log_msg = f'Get current robot position through `{anm.SERVER_GET_POSE}` as ({self._pose.x}, {self._pose.y})'
            rospy.loginfo(anm.tag_log(log_msg, LOG_TAG))
        # Create the response with the robot pose and return it.
        response = GetPoseResponse()
        response.pose = self._pose
        return response

    # The `robot/set_pose` service implementation.
    # The `request` input parameter is the current robot pose to be set,
    # as given by the client. This server returns an empty `response`.
    def set_battery(self, request):
    """
    Function to set the battery level
    """
        if request.level is not None:
            # Store the new current robot position.
            self._battery_level = request.level
            # Log information.
            log_msg = (f'Set current robot battery through `{anm.SERVER_SET_BATTERY}` '
                             f'as ({self._battery_level}).')
            rospy.loginfo(anm.tag_log(log_msg, LOG_TAG))
        else:
            rospy.logerr(anm.tag_log('Cannot get an unspecified robot battery level', LOG_TAG))
        # Return an empty response.
        return SetBatteryResponse()

    # The `robot/get_pose` service implementation.
    # The `request` input parameter is given by the client as empty. Thus, it is not used.
    # The `response` returned to the client contains the current robot pose.
    def get_battery(self, response):
    """
    Function to get the battery level
    """
        # Log information.
        if self._battery_level is None:
            rospy.logerr(anm.tag_log('Cannot get an unspecified robot battery level', LOG_TAG))
        else:
            log_msg = f'Get current robot battery through `{anm.SERVER_GET_BATTERY}` as ({self._battery_level})'
            rospy.loginfo(anm.tag_log(log_msg, LOG_TAG))
        # Create the response with the robot pose and return it.
        response = GetBatteryResponse()
        response.level = self._battery_level
        return response


if __name__ == "__main__":
    # Instantiate the node manager class and wait.
    RobotState()
    rospy.spin()

