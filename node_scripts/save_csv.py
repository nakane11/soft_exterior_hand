#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import rospy
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from soft_exterior_hand.msg import UInt16Array

class SaveCSV(QDialog):
    def __init__(self, parent=None):
        super(SaveCSV, self).__init__(parent)
        self.count = 0
        self.sensor_data = []
        self.filepath = rospy.get_param('~filepath', '/home/nakane/Documents/servo.csv')

        self.layout = QHBoxLayout()
        left_layout = QGridLayout()
        right_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        path_layout = QHBoxLayout()

        self.servo_label = [QLabel() for x in range(8)]
        servo_name = ["index", "middle", "ring", "little", "thumb1", "thumb2", "thumb3", "kondo"]
        for name, label in zip(servo_name, self.servo_label):
            label.setText(name)
            label.setFont(QFont('Arial', 15))

        self.angle_label = [QSpinBox() for x in range(8)]
        for i in range(4):
            self.angle_label[i].setMaximum(140)
            self.angle_label[i].setMinimum(40)
        self.angle_label[0].setValue(110)
        self.angle_label[1].setValue(117)
        self.angle_label[2].setValue(120)
        self.angle_label[3].setValue(100)

        self.angle_label[4].setMaximum(160)
        self.angle_label[4].setMinimum(60)
        self.angle_label[4].setValue(160)

        self.angle_label[5].setMaximum(105)
        self.angle_label[5].setMinimum(0)
        self.angle_label[5].setValue(30)

        self.angle_label[6].setMaximum(180)
        self.angle_label[6].setMinimum(20)
        self.angle_label[6].setValue(180)

        self.angle_label[7].setMaximum(270)
        self.angle_label[7].setMinimum(0)
        self.angle_label[7].setValue(270)

        for each_label in self.angle_label:
            each_label.setFont(QFont('Arial', 15))
            each_label.valueChanged.connect(self.spin_value_change)

        self.angle_slider = [QSlider(QtCore.Qt.Orientation.Horizontal)
                             for x in range(8)]        
        for each_slider, each_label in zip(self.angle_slider, self.angle_label):
            each_slider.setMaximum(each_label.maximum())
            each_slider.setMinimum(each_label.minimum())
            each_slider.setValue(each_label.value())
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

        save_button = QPushButton("Save")
        save_button.setFont(QFont('Arial', 15))
        save_button.clicked.connect(self.save)
        right_layout.addWidget(save_button)

        path_label = QLabel()
        path_label.setText("path:")
        path_layout.addWidget(path_label)
        self.path_box = QLineEdit()
        self.path_box.setText(self.filepath)
        self.path_box.textChanged.connect(self.path_text_change)
        path_layout.addWidget(self.path_box)
        right_layout.addLayout(path_layout)

        self.count_label = QLabel()
        self.count_label.setText("count: {}".format(self.count))
        self.count_label.setFont(QFont('Arial', 15))
        right_layout.addWidget(self.count_label)

        self.layout.addLayout(left_layout)
        self.layout.addLayout(right_layout)
        self.setLayout(self.layout)

        self.pub = rospy.Publisher("/servo_states", UInt16Array, queue_size=1)
        rospy.sleep(1)
        pub_msg = UInt16Array()
        pub_msg.data = [x.value() for x in self.angle_slider]
        self.pub.publish(pub_msg)
        self.sub = rospy.Subscriber("/sensor_states", UInt16Array, self.sensor_cb)

    def slider_value_change(self):
        pub_msg = UInt16Array()
        pub_msg.data = [x.value() for x in self.angle_slider]
        self.pub.publish(pub_msg)
        for i in range(8):
            self.angle_label[i].setValue(self.angle_slider[i].value())
        rospy.sleep(0.3)

    def spin_value_change(self):
        pub_msg = UInt16Array()
        pub_msg.data = [x.value() for x in self.angle_label]
        self.pub.publish(pub_msg)
        for i in range(8):
            self.angle_slider[i].setValue(self.angle_label[i].value())
        rospy.sleep(0.3)

    def path_text_change(self):
        self.filepath = self.path_box.text()

    def sensor_cb(self, msg):
        self.sensor_data = list(msg.data)
        for val, each_sensor in zip(msg.data, self.sensor_label):
            each_sensor.setText(str(val))

    def save(self):
        save_data = [x.value() for x in self.angle_slider] + self.sensor_data
        with open(self.filepath, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(save_data)
        self.count += 1
        self.count_label.setText("count: {}".format(self.count))

if __name__ == "__main__":
    rospy.init_node('save_cv')
    import sys
    app = QApplication(sys.argv)
    form = SaveCSV()
    form.show()
    sys.exit(app.exec_())
