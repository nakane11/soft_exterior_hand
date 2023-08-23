#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import numpy as np
import math
from soft_exterior_hand.msg import UInt16Array

class InterpolateNode():
    def __init__(self):
        self.angle = [110, 117, 120, 100, 160, 30, 180, 270]
        self.rate = rospy.Rate(rospy.get_param("~rate", 20))
        self.min_angle = rospy.get_param("~min_angle", 1)
        self.pub = rospy.Publisher('/servo_states', UInt16Array, queue_size=1)
        self.sub = rospy.Subscriber("/cmd_angle", UInt16Array, self.cb)
        
    def cb(self, msg):
        self.min_angle = rospy.get_param("~min_angle", 1)
        target_array = np.array(msg.data)
        max_diff = np.max(np.abs(target_array - np.array(self.angle)))
        div_num = int(math.ceil(max_diff/self.min_angle))
        angle_list = self._interpolation(np.array(self.angle), target_array, div_num)
        for segment_angle in angle_list:
            msg = UInt16Array(data = [int(i) for i in segment_angle])
            self.pub.publish(msg)
            self.angle = segment_angle
            self.rate.sleep()

    def _interpolation(self, initial, target, div_num):
        ret = np.zeros((div_num, initial.size))
        for i in range(initial.size):
            for j in range(div_num): 
                ret[j][i] = math.ceil(initial[i]+(target[i]-initial[i])/div_num * (j+1))
        return ret.tolist()
    
if __name__=='__main__':
    rospy.init_node("interpolate_node")
    marker_publisher = InterpolateNode()
    rospy.spin()
