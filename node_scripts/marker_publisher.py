#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import rospy
from visualization_msgs.msg import Marker, MarkerArray
from soft_exterior_hand.msg import UInt16Array

class MarkerPublisher():

    index2frame = ["thumb_link_3",
                   "thumb_link_2",
                   "index_link_3",
                   "index_link_2",
                   "index_link_1",
                   "middle_link_3",
                   "middle_link_2",
                   "middle_link_1",
                   "ring_link_3",
                   "ring_link_2",
                   "ring_link_1",
                   "little_link_3",
                   "little_link_2",
                   "little_link_1"]

    def __init__(self):
        self.pub = rospy.Publisher('~output', MarkerArray, queue_size=1)
        self.sub = rospy.Subscriber("/sensor_states", UInt16Array, self.cb)

    def cb(self, msg):
        marker_array = MarkerArray()
        stamp = rospy.Time.now()
        for i, val in enumerate(msg.data):
            marker = Marker()
            marker.header.stamp = stamp
            marker.header.frame_id = self.index2frame[i]
            marker.type = Marker.CYLINDER;
            marker.pose.position.x = 0.008
            marker.pose.position.y = 0.0
            marker.pose.position.z = 0.0
            marker.pose.orientation.w = 1.0
            marker.scale.x = 0.012
            marker.scale.y = 0.008
            marker.scale.z = 0.004
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            marker.color.a = min(1.2*math.log(1+val/4095*(math.e-1.0)), 1.0)
            # marker.color.a = min(val/3500, 1.0)
            marker.id = i
            marker.lifetime = rospy.Duration(0.25)
            marker.action = Marker.ADD
            marker_array.markers.append(marker)
        self.pub.publish(marker_array)

if __name__=='__main__':
    rospy.init_node("marker_publisher")
    marker_publisher = MarkerPublisher()
    rospy.spin()
