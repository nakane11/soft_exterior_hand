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

const int servo_pins[] = {23,22,21,19,18,17,16};
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
soft_exterior_hand::UInt16Array pub_msg;
ros::Publisher pub("sensor_states", &pub_msg);

uint16_t voltages[14];
int sensor_pins[] = {2,4,12,14,15,25,26,27,32,33,34,35,36,39};

void setup() {
  Serial.begin(BAUDRATE);
  krs.begin();
  nh.initNode();
  nh.advertise(pub);
  nh.subscribe(sub);
  for(int i=0;i<7;i++){
    servos[i] = new Servo();
    servos[i]->attach(servo_pins[i]);
  }
  delay(10);
}

void loop() {
  for (int i = 0; i < 14; i++){
    int pin_num = sensor_pins[i];
    int analogValue = analogRead(pin_num);
    voltages[i] = analogValue;
    delay(1);
  }
  pub_msg.data = voltages;
  pub_msg.data_length = 14;
  pub.publish( &pub_msg );
    
  nh.spinOnce();
  delay(1);
}
