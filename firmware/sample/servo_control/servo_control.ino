#include <BluetoothHardware.h>
#include <ros.h>
#include <ESP32Servo.h>
#include <IcsHardSerialClass.h>
#include <soft_exterior_hand/UInt16Array.h>

const byte EN_PIN = 13;
const long BAUDRATE = 115200;
const int TIMEOUT = 1000;
const int ID = 2;

IcsHardSerialClass krs(&Serial,EN_PIN,BAUDRATE,TIMEOUT);

const int pins[] = {23,22,21,19,18,17,16};
Servo *servos[7];
int pos = 0;

void cb(const soft_exterior_hand::UInt16Array& sub_msg){
  for(int i=0;i<7;i++){
    servos[i]->write(sub_msg.data[i]);
  }
  
  pos = 3500+8000*sub_msg.data[7]/270; 
  krs.setPos(ID,pos); 
}

ros::NodeHandle_<BluetoothHardware> nh;
ros::Subscriber<soft_exterior_hand::UInt16Array> sub("servo_states", cb);

void setup() {
  Serial.begin(BAUDRATE);
  krs.begin();
  nh.initNode();
  nh.subscribe(sub);
  for(int i=0;i<7;i++){
    servos[i] = new Servo();
    servos[i]->attach(pins[i]);
  }
  delay(10);
}

void loop() {
  nh.spinOnce();
  delay(1);
}
