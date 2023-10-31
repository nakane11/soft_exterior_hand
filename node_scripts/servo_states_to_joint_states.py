#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import math
from sensor_msgs.msg import JointState
from soft_exterior_hand.msg import UInt16Array

class ServoStatesToJointStates():
    hand_jointname = ["index_joint_0",
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
                      "thumb_joint_0",
                      "thumb_joint_1",
                      "thumb_joint_2",
                      "thumb_joint_3",]
    def __init__(self, parent=None):
        self.servo_msg_default = UInt16Array(data=[80, 107, 128, 120, 160, 30, 180, 270])
        self.servo_msg = self.servo_msg_default
        self.pub = rospy.Publisher("/joint_states_with_hand", JointState, queue_size=1)
        self.servo_sub = rospy.Subscriber("/servo_states", UInt16Array, self.servo_cb)
        self.joint_sub = rospy.Subscriber("/joint_states", JointState, self.republish)

    def servo_cb(self, msg):
        self.servo_msg = msg
        
    def republish(self, joint_state_msg):
        pub_joint_state_msg = joint_state_msg
        # joint_state_msg.header.stamp = rospy.Time.now()
        # joint_state_msg.name = ["index_joint_0",
        #                         "index_joint_1",
        #                         "index_joint_2",
        #                         "index_joint_3",
        #                         "middle_joint_0",
        #                         "middle_joint_1",
        #                         "middle_joint_2",
        #                         "middle_joint_3",
        #                         "ring_joint_0",
        #                         "ring_joint_1",
        #                         "ring_joint_2",
        #                         "ring_joint_3",
        #                         "little_joint_0",
        #                         "little_joint_1",
        #                         "little_joint_2",
        #                         "little_joint_3",                                
        #                         "thumb_joint_0",
        #                         "thumb_joint_1",
        #                         "thumb_joint_2",
        #                         "thumb_joint_3",]
        pub_joint_state_msg.name.extend(self.hand_jointname)
        rad_data = [(x-d)/180.0*math.pi for x, d in zip(self.servo_msg.data, self.servo_msg_default.data)]
        pub_joint_state_msg.position = joint_state_msg.position + tuple([rad_data[0],0,0,0,
                                                                     rad_data[1],0,0,0,
                                                                     rad_data[2],0,0,0,
                                                                     rad_data[3],0,0,0,
                                                                     rad_data[4],0,0,0])
        self.pub.publish(pub_joint_state_msg)
        
if __name__ == "__main__":
    rospy.init_node('servo_states_to_joint_states')
    S = ServoStatesToJointStates()
    rospy.spin()
