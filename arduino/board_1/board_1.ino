#include <stdlib.h>

#define PressureThres 200
#define SensorCount 16
#define BoardName "B1"

byte pins[SensorCount] = {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15};
String sensor_id[SensorCount] = {"0", "1", "2", "3", "5", "6", "7", "8", "10", "11", "12", "13", "15", "16", "17", "18"};
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
    if ('s' == s_in)
    {
      if (mode == 1) {
        mode_1();
      }
      else if (mode == 2) {
        mode_2();
      }
      else if (mode == 3) {
        mode_3();
      }
    }
    else if ('w' == s_in) {
      Serial.println(BoardName);
    }
    else if ('m' == s_in){
      Serial.print("Board mode=");
      Serial.println(mode);
    }
    else if ('1' <= s_in <= '3') {
      mode = s_in - '0'; // convert single Char to Int
      Serial.print("Set board mode=");
      Serial.println(s_in);
    }
  }
}
