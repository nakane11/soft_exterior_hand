#include <BluetoothHardware.h>
#include <ros.h>
#include <std_msgs/String.h>

ros::NodeHandle_<BluetoothHardware> nh;

std_msgs::String str_msg;
ros::Publisher chatter("chatter", &str_msg);

char hello[13] = "hello world!";

void setup()
{
  Serial.begin(115200);
  
  nh.initNode();
  nh.advertise(chatter);
  Serial.print("Bluetooth connected.");
  delay(10);
}

void loop()
{
  str_msg.data = hello;
  chatter.publish( &str_msg );
  nh.spinOnce();
  delay(1000);
}
