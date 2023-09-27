#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import UInt8, Float64
import numpy as np

class SampleFlexSensor():
    def __init__(self):
        self._length = rospy.get_param('~length', 20)
        self.arr = np.zeros(self._length)
        self.pub = rospy.Publisher('~output', Float64, queue_size=1)
        self.sub = rospy.Subscriber("/chatter", UInt8, self.cb)

    def cb(self, msg):
        self.arr = np.append(self.arr, msg.data)
        self.arr = np.delete(self.arr, 0)
        pub_msg = Float64()
        pub_msg.data = np.average(self.arr)
        self.pub.publish(pub_msg)

if __name__=='__main__':
    rospy.init_node("sample_flex_sensor")
    sfs = SampleFlexSensor()
    rospy.spin()
