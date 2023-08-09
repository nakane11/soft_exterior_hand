#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from soft_exterior_hand.msg import UInt16Array

class SaveCSV(QDialog):
    def __init__(self, parent=None):
        super(SaveCSV, self).__init__(parent)
        self.count = 0
        
        self.layout = QHBoxLayout()
        left_layout = QGridLayout()
        right_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        self.servo_label = [QLabel() for x in range(8)]
        servo_name = ["index", "middle", "ring", "little", "thumb1", "thumb2", "thumb3", "kondo"]
        for name, label in zip(servo_name, self.servo_label):
            label.setText(name)
            label.setFont(QFont('Arial', 15))

        self.angle_label = [QSpinBox() for x in range(8)]
        for each_label in self.angle_label:
            each_label.setMaximum(170)
            each_label.setMinimum(10)
            each_label.setValue(90)
            each_label.setFont(QFont('Arial', 15))
            each_label.valueChanged.connect(self.spin_value_change)
        
        self.angle_slider = [QSlider(QtCore.Qt.Orientation.Horizontal)
                             for x in range(8)]        
        for each_slider in self.angle_slider:
            each_slider.setMaximum(170)
            each_slider.setMinimum(10)
            each_slider.setValue(90)
            each_slider.valueChanged.connect(self.slider_value_change)

        for i in range(8):
            left_layout.addWidget(self.servo_label[i], 2*i,0)
            left_layout.addWidget(self.angle_label[i], 2*i,1)
            left_layout.addWidget(self.angle_slider[i], 2*i+1,0)

        self.sensor_label = [QLabel() for x in range(14)]
        for i, each_sensor in enumerate(self.sensor_label):
            each_sensor.setText("")
            each_sensor.setFont(QFont('Arial', 15))
            each_sensor.setLineWidth(2)
            each_sensor.setFrameStyle(QFrame.Box)
            grid_layout.addWidget(each_sensor, (i+1)%3,(i+1)//3)
        right_layout.addLayout(grid_layout)
        self.sub = rospy.Subscriber("/sensor_states", UInt16Array, self.sensor_cb)
        
        save_button = QPushButton("Save")
        save_button.setFont(QFont('Arial', 15))
        right_layout.addWidget(save_button)

        count_label = QLabel()
        count_label.setText("count: {}".format(self.count))
        count_label.setFont(QFont('Arial', 15))
        right_layout.addWidget(count_label)
        
        self.layout.addLayout(left_layout)
        self.layout.addLayout(right_layout)
        self.setLayout(self.layout)

    def slider_value_change(self):
        for i in range(8):
            self.angle_label[i].setValue(self.angle_slider[i].value())

    def spin_value_change(self):
        for i in range(8):
            self.angle_slider[i].setValue(self.angle_label[i].value())

    def sensor_cb(self, msg):
        for val, each_sensor in zip(msg.data, self.sensor_label):
            each_sensor.setText(str(val))

if __name__ == "__main__":
    rospy.init_node('save_cv')
    import sys
    app = QApplication(sys.argv)
    form = SaveCSV()
    form.show()
    sys.exit(app.exec_())
