#include <BluetoothHardware.h>
#include <ros.h>
#include <soft_exterior_hand/UInt16Array.h>

ros::NodeHandle_<BluetoothHardware> nh;

soft_exterior_hand::UInt16Array pub_msg;
ros::Publisher chatter("sensor_states", &pub_msg);
//
//unsigned short voltages[14];
uint16_t voltages[14];
int pins[14] = {2,4,12,14,15,25,26,27,32,33,34,35,36,39};

void setup()
{
  Serial.begin(115200);
  analogReadResolution(12);
  nh.initNode();
  nh.advertise(chatter);
  Serial.print("Bluetooth connected.");
  delay(10);
}

void loop()
{
  for (int i = 0; i < 14; i++){
    int pin_num = pins[i];
    int analogValue = analogRead(pin_num);
    char log_msg[50]; // ログメッセージを保存するためのバッファ
    sprintf(log_msg, "pin %d analog value = %d\n",pin_num, analogValue); // 数値を文字列に変換
    nh.loginfo(log_msg); // ログに情報を出力
    voltages[i] = analogValue;
    delay(10);
  }
  pub_msg.data = voltages;
  pub_msg.data_length = 14;
  chatter.publish( &pub_msg );
  nh.spinOnce();
}
