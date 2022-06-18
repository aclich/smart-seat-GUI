#include <stdlib.h>

#define PressureThres 200
#define SensorCount 9
#define BoardName "B2"

byte pins[SensorCount] = {A0, A1, A2, A3, A4, A5, A6, A7, A8};
String sensor_id[SensorCount] = {"4", "9", "14", "19", "20", "21", "22", "23", "24"};

int mode = 1;

int get_value(byte pin){
  int value = analogRead(pin);
  return value > PressureThres ? value : 0;
  }

void mode_1(){
  for (int i = 0 ; i<SensorCount; i++){
      Serial.println(get_value(pins[i]));
    }
}

void mode_2(){
  String str = "{";
      for (int i = 0; i < SensorCount; i++){
        str += i == 0 ? String(" ") : String(", ");
        str += "\"" + sensor_id[i] + "\":" + String(get_value(pins[i]));
      } 
      Serial.println(str+" }");
  }

void mode_3(){
  String str = "[";
      for (int i = 0; i < SensorCount; i++){
        str += i == 0 ? "" : ", ";
        str += String(get_value(pins[i]));
      } 
      Serial.println(str+"]");
  }

void setup()
{
  Serial.begin(9600); // 9600 bps
}


void loop()
{
  if (Serial.available())
  {
    char s_in = Serial.read();
    switch (s_in)
    {
    case 's':
      switch (mode)
      {
      case 1:
        mode_1();
        break;
      case 2:
        mode_2();
        break;
      case 3:
        mode_3();
        break;
      default:
        break;
      }
      break;
    case 'w':
      Serial.println(BoardName);
      break;
    case 'm':
      Serial.print("Board mode=");
      Serial.println(mode);
      break;
    case '1': case '2': case '3':
      mode = s_in - '0'; //convert single Char to Int
      Serial.print("Set board mode=");
      Serial.println(s_in);
      break;
    default:
      break;
    }
  }
}
