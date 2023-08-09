#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import math
from sensor_msgs.msg import JointState
from soft_exterior_hand.msg import UInt16Array

class ServoStatesToJointStates():
    def __init__(self, parent=None):
        self.pub = rospy.Publisher("/joint_states", JointState, queue_size=1)
        self.sub = rospy.Subscriber("/servo_states", UInt16Array, self.republish)

    def republish(self, msg):
        joint_state_msg = JointState()
        joint_state_msg.header.stamp = rospy.Time.now()
        joint_state_msg.name = ["index_joint_0",
                                "index_joint_1",
                                "index_joint_2",
                                "index_joint_3",
                                "middle_joint_0",
                                "middle_joint_1",
                                "middle_joint_2",
                                "middle_joint_3",
                                "ring_joint_0",
                                "ring_joint_1",
                                "ring_joint_2",
                                "ring_joint_3",
                                "little_joint_0",
                                "little_joint_1",
                                "little_joint_2",
                                "little_joint_3",                                
                                "thumb_joint_0"]
        rad_data = [(x-90)/180.0*math.pi for x in msg.data]
        joint_state_msg.position = [rad_data[0],0,0,0,
                                    rad_data[1],0,0,0,
                                    rad_data[2],0,0,0,
                                    rad_data[3],0,0,0,
                                    rad_data[4]]
        self.pub.publish(joint_state_msg)
        
if __name__ == "__main__":
    rospy.init_node('servo_states_to_joint_states')
    S = ServoStatesToJointStates()
    rospy.spin()
