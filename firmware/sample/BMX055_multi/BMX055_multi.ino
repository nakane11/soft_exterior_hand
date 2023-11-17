//================================================================//
//  AE-BMX055             Arduino UNO                             //
//    VCC                    +5V                                  //
//    GND                    GND                                  //
//    SDA                    A4(SDA)                              //
//    SCL                    A5(SCL)                              //
//                                                                //
//   (JP4,JP5,JP6はショートした状態)                                //
//   http://akizukidenshi.com/catalog/g/gK-13010/                 //
//================================================================//
#include <ros.h>
#include <std_msgs/Float32MultiArray.h>

#include<Wire.h>

// BMX055 加速度センサのI2Cアドレス  
#define Addr_Accl0 0x19  // (JP1,JP2,JP3 = Openの時)
// BMX055 ジャイロセンサのI2Cアドレス
#define Addr_Gyro0 0x69  // (JP1,JP2,JP3 = Openの時)
// BMX055 磁気センサのI2Cアドレス
#define Addr_Mag0 0x13   // (JP1,JP2,JP3 = Openの時)

// BMX055 加速度センサのI2Cアドレス  
#define Addr_Accl1 0x18  // (JP1,JP2,JP3 = Shortの時)
// BMX055 ジャイロセンサのI2Cアドレス
#define Addr_Gyro1 0x68  // (JP1,JP2,JP3 = Shortの時)
// BMX055 磁気センサのI2Cアドレス
#define Addr_Mag1 0x10   // (JP1,JP2,JP3 = Shortの時)

// センサーの値を保存するグローバル変数
float xAccl = 0.00;
float yAccl = 0.00;
float zAccl = 0.00;
float xGyro = 0.00;
float yGyro = 0.00;
float zGyro = 0.00;
int   xMag  = 0;
int   yMag  = 0;
int   zMag  = 0;

unsigned long time;
#define LOOP_TIME 20
ros::NodeHandle nh;
float force_data0[9];
float force_data1[9];
float arr[18];
std_msgs::Float32MultiArray force_msg;
ros::Publisher force_pub("force_sensor", &force_msg);

void setup()
{
  nh.initNode();
  nh.advertise(force_pub);
  while(!nh.connected())
  {
    nh.spinOnce();
  }
  // Wire(Arduino-I2C)の初期化
  Wire.begin();
  // デバッグ用シリアル通信は9600bps
  //Serial.begin(115200);
  //BMX055 初期化
  BMX055_Init(Addr_Accl0, Addr_Gyro0, Addr_Mag0);
  BMX055_Init(Addr_Accl1, Addr_Gyro1, Addr_Mag1);
  delay(300);
}

void loop()
{
  time = millis();

  //Serial.println("--------------------------------------"); 

  //BMX055 加速度の読み取り
  BMX055_Accl(Addr_Accl0, force_data0);
  BMX055_Accl(Addr_Accl1, force_data1);
 
  //BMX055 ジャイロの読み取り
  BMX055_Gyro(Addr_Gyro0, force_data0);
  BMX055_Gyro(Addr_Gyro1, force_data1);

  //BMX055 磁気の読み取り
  BMX055_Mag(Addr_Mag0, force_data0);
  BMX055_Mag(Addr_Mag1, force_data1);


    int m = sizeof(force_data0)/sizeof(force_data0[0]);
    int n = sizeof(force_data1)/sizeof(force_data1[0]);
        for(int i = 0; i < m; i++)
    {
        arr[i] = force_data0[i];
    }
            for(int i = 0; i < n; i++)
    {
        arr[9+i] = force_data1[i];
    }
  force_msg.data =  arr;
  force_msg.data_length = 18;
  force_pub.publish(&force_msg);
  while (millis() < time + LOOP_TIME); // enforce constant loop time
  nh.spinOnce();
  // delay(50);
}

//=====================================================================================//
void BMX055_Init(int addr_Accl, int addr_Gyro, int addr_Mag)
{
  //------------------------------------------------------------//
  Wire.beginTransmission(addr_Accl);
  Wire.write(0x0F); // Select PMU_Range register
  Wire.write(0x03);   // Range = +/- 2g
  Wire.endTransmission();
  delay(100);
 //------------------------------------------------------------//
  Wire.beginTransmission(addr_Accl);
  Wire.write(0x10);  // Select PMU_BW register
  Wire.write(0x08);  // Bandwidth = 7.81 Hz
  Wire.endTransmission();
  delay(100);
  //------------------------------------------------------------//
  Wire.beginTransmission(addr_Accl);
  Wire.write(0x11);  // Select PMU_LPW register
  Wire.write(0x00);  // Normal mode, Sleep duration = 0.5ms
  Wire.endTransmission();
  delay(100);
 //------------------------------------------------------------//
  Wire.beginTransmission(addr_Gyro);
  Wire.write(0x0F);  // Select Range register
  Wire.write(0x04);  // Full scale = +/- 125 degree/s
  Wire.endTransmission();
  delay(100);
 //------------------------------------------------------------//
  Wire.beginTransmission(addr_Gyro);
  Wire.write(0x10);  // Select Bandwidth register
  Wire.write(0x07);  // ODR = 100 Hz
  Wire.endTransmission();
  delay(100);
 //------------------------------------------------------------//
  Wire.beginTransmission(addr_Gyro);
  Wire.write(0x11);  // Select LPM1 register
  Wire.write(0x00);  // Normal mode, Sleep duration = 2ms
  Wire.endTransmission();
  delay(100);
 //------------------------------------------------------------//
  Wire.beginTransmission(addr_Mag);
  Wire.write(0x4B);  // Select Mag register
  Wire.write(0x83);  // Soft reset
  Wire.endTransmission();
  delay(100);
  //------------------------------------------------------------//
  Wire.beginTransmission(addr_Mag);
  Wire.write(0x4B);  // Select Mag register
  Wire.write(0x01);  // Soft reset
  Wire.endTransmission();
  delay(100);
  //------------------------------------------------------------//
  Wire.beginTransmission(addr_Mag);
  Wire.write(0x4C);  // Select Mag register
  Wire.write(0x00);  // Normal Mode, ODR = 10 Hz
  Wire.endTransmission();
 //------------------------------------------------------------//
  Wire.beginTransmission(addr_Mag);
  Wire.write(0x4E);  // Select Mag register
  Wire.write(0x84);  // X, Y, Z-Axis enabled
  Wire.endTransmission();
 //------------------------------------------------------------//
  Wire.beginTransmission(addr_Mag);
  Wire.write(0x51);  // Select Mag register
  Wire.write(0x04);  // No. of Repetitions for X-Y Axis = 9
  Wire.endTransmission();
 //------------------------------------------------------------//
  Wire.beginTransmission(addr_Mag);
  Wire.write(0x52);  // Select Mag register
  Wire.write(0x16);  // No. of Repetitions for Z-Axis = 15
  Wire.endTransmission();
}
//=====================================================================================//
void BMX055_Accl(int addr_Accl, float *fdata)
{
  unsigned int data[6];
  for (int i = 0; i < 6; i++)
  {
    Wire.beginTransmission(addr_Accl);
    Wire.write((2 + i));// Select data register
    Wire.endTransmission();
    Wire.requestFrom(addr_Accl, 1);// Request 1 byte of data
    // Read 6 bytes of data
    // xAccl lsb, xAccl msb, yAccl lsb, yAccl msb, zAccl lsb, zAccl msb
    if (Wire.available() == 1)
      data[i] = Wire.read();
  }
  // Convert the data to 12-bits
  xAccl = ((data[1] * 256) + (data[0] & 0xF0)) / 16;
  if (xAccl > 2047)  xAccl -= 4096;
  yAccl = ((data[3] * 256) + (data[2] & 0xF0)) / 16;
  if (yAccl > 2047)  yAccl -= 4096;
  zAccl = ((data[5] * 256) + (data[4] & 0xF0)) / 16;
  if (zAccl > 2047)  zAccl -= 4096;
  xAccl = xAccl * 0.0098; // range = +/-2g
  yAccl = yAccl * 0.0098; // range = +/-2g
  zAccl = zAccl * 0.0098; // range = +/-2g
  fdata[0] = xAccl;
  fdata[1] = yAccl;
  fdata[2] = zAccl;
}
//=====================================================================================//
void BMX055_Gyro(int addr_Gyro, float *fdata)
{
  unsigned int data[6];
  for (int i = 0; i < 6; i++)
  {
    Wire.beginTransmission(addr_Gyro);
    Wire.write((2 + i));    // Select data register
    Wire.endTransmission();
    Wire.requestFrom(addr_Gyro, 1);    // Request 1 byte of data
    // Read 6 bytes of data
    // xGyro lsb, xGyro msb, yGyro lsb, yGyro msb, zGyro lsb, zGyro msb
    if (Wire.available() == 1)
      data[i] = Wire.read();
  }
  // Convert the data
  xGyro = (data[1] * 256) + data[0];
  if (xGyro > 32767)  xGyro -= 65536;
  yGyro = (data[3] * 256) + data[2];
  if (yGyro > 32767)  yGyro -= 65536;
  zGyro = (data[5] * 256) + data[4];
  if (zGyro > 32767)  zGyro -= 65536;

  xGyro = xGyro * 0.0038; //  Full scale = +/- 125 degree/s
  yGyro = yGyro * 0.0038; //  Full scale = +/- 125 degree/s
  zGyro = zGyro * 0.0038; //  Full scale = +/- 125 degree/s

  fdata[3] = xGyro;
  fdata[4] = yGyro;
  fdata[5] = zGyro;
}
//=====================================================================================//
void BMX055_Mag(int addr_Mag, float *fdata)
{
  unsigned int data[8];
  for (int i = 0; i < 8; i++)
  {
    Wire.beginTransmission(addr_Mag);
    Wire.write((0x42 + i));    // Select data register
    Wire.endTransmission();
    Wire.requestFrom(addr_Mag, 1);    // Request 1 byte of data
    // Read 6 bytes of data
    // xMag lsb, xMag msb, yMag lsb, yMag msb, zMag lsb, zMag msb
    if (Wire.available() == 1)
      data[i] = Wire.read();
  }
// Convert the data
  xMag = ((data[1] <<5) | (data[0]>>3));
  if (xMag > 4095)  xMag -= 8192;
  yMag = ((data[3] <<5) | (data[2]>>3));
  if (yMag > 4095)  yMag -= 8192;
  zMag = ((data[5] <<7) | (data[4]>>1));
  if (zMag > 16383)  zMag -= 32768;

  fdata[6] = xMag;
  fdata[7] = yMag;
  fdata[8] = zMag;
}
