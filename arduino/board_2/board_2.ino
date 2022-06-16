#include <stdlib.h>
#define fsr_pin A0
#define fsr_pin2 A1
#define fsr_pin3 A2
#define fsr_pin4 A3
#define fsr_pin5 A4
#define fsr_pin6 A5
#define fsr_pin7 A6
#define fsr_pin8 A7
#define fsr_pin9 A8

char serial;

void setup() 
{ 
Serial.begin(9600); // 9600 bps
} 
void loop() 
{

//int fsr_value1 = analogRead(fsr_pin); // 讀取FSR
//int fsr_value2 = analogRead(fsr_pin2); // 讀取FSR
//int fsr_value3 = analogRead(fsr_pin3);
//int fsr_value4 = analogRead(fsr_pin4);
//int fsr_value5 = analogRead(fsr_pin5);
//int fsr_value6 = analogRead(fsr_pin6);
//int fsr_value7 = analogRead(fsr_pin7);
//int fsr_value8 = analogRead(fsr_pin8);
//int fsr_value9 = analogRead(fsr_pin9);

//Serial.print("The 1 sensor value is : ");
//Serial.println(fsr_value1);
//Serial.print("The 2 sensor value is : ");
//Serial.println(fsr_value2);
//Serial.print("The 3 sensor value is : ");
//Serial.println(fsr_value3);
//Serial.print("The 4 sensor value is : ");
//Serial.println(fsr_value4);
//Serial.print("The 5 sensor value is : ");
//Serial.println(fsr_value5);
//Serial.print("The 6 sensor value is : ");
//Serial.println(fsr_value6);
//Serial.print("The 7 sensor value is : ");
//Serial.println(fsr_value7);
//Serial.print("The 8 sensor value is : ");
//Serial.println(fsr_value8);
//Serial.print("The 9 sensor value is : ");
//Serial.println(fsr_value9);

//Serial.println("----------------------------");
//delay(500);

//Connect to python
 if (Serial.available())
 {
  if ('h'==Serial.read())
  {
    int fsr_value = analogRead(fsr_pin); // 讀取FSR
    int fsr_value2 = analogRead(fsr_pin2); // 讀取FSR
    int fsr_value3 = analogRead(fsr_pin3);
    int fsr_value4 = analogRead(fsr_pin4);
    int fsr_value5 = analogRead(fsr_pin5);
    int fsr_value6 = analogRead(fsr_pin6);
    int fsr_value7 = analogRead(fsr_pin7);
    int fsr_value8 = analogRead(fsr_pin8);
    int fsr_value9 = analogRead(fsr_pin9);

       if (fsr_value <200)
      {
       Serial.println(0);
      }
     else 
      {
      Serial.println(fsr_value);
      }
      
      if (fsr_value2 <200)
      {
       Serial.println(0);
      }
     else 
      {
      Serial.println(fsr_value2);
      }

      if (fsr_value3 <200)
      {
       Serial.println(0);
      }
     else 
      {
      Serial.println(fsr_value3);
      }

      if (fsr_value4 <200)
      {
       Serial.println(0);
      }
     else 
      {
      Serial.println(fsr_value4);
      }

      if (fsr_value5 <200)
      {
       Serial.println(0);
      }
     else 
      {
      Serial.println(fsr_value5);
      }

      if (fsr_value6 <200)
      {
       Serial.println(0);
      }
     else 
      {
      Serial.println(fsr_value6);
      }

      if (fsr_value7 <200)
      {
       Serial.println(0);
      }
     else 
      {
      Serial.println(fsr_value7);
      }

      if (fsr_value8 <200)
      {
       Serial.println(0);
      }
     else 
      {
      Serial.println(fsr_value8);
      }

      if (fsr_value9 <200)
      {
       Serial.println(0);
      }
     else 
      {
      Serial.println(fsr_value9);
      }
    
    delay(300);
  }
  else
  {
    Serial.print("None");
    delay(300);
  }
 }
}
