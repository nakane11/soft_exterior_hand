#ifndef BLUETOOTH_HARDWARE_H_
#define BLUETOOTH_HARDWARE_H_

#include <Arduino.h>
#include "BluetoothSerial.h"

class BluetoothHardware {
public:
  BluetoothHardware() {}

  void init()
  {
    SerialBT.begin("esp32-blt");
  }

  void init(char *name)
  {
    SerialBT.begin(name);
  }

  int read(){
    return SerialBT.read();
  }

  void write(const uint8_t* data, int length)
  {
    SerialBT.write(data, length);
  }

  unsigned long time()
  {
    return millis();
  }

protected:
  BluetoothSerial SerialBT;
};

#endif
