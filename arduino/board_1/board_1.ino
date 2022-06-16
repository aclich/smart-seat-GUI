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
#define fsr_pin10 A9
#define fsr_pin11 A10
#define fsr_pin12 A11
#define fsr_pin13 A12
#define fsr_pin14 A13
#define fsr_pin15 A14
#define fsr_pin16 A15
//int fsr_pin3 = 8;
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
//int fsr_value10 = analogRead(fsr_pin10);
//int fsr_value11 = analogRead(fsr_pin11);
//int fsr_value12 = analogRead(fsr_pin12);
//int fsr_value13 = analogRead(fsr_pin13);
//int fsr_value14 = analogRead(fsr_pin14);
//int fsr_value15 = analogRead(fsr_pin15);
//int fsr_value16 = analogRead(fsr_pin16);
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
//Serial.print("The 10 sensor value is : ");
//Serial.println(fsr_value10);
//Serial.print("The 11 sensor value is : ");
//Serial.println(fsr_value11);
//Serial.print("The 12 sensor value is : ");
//Serial.println(fsr_value12);
//Serial.print("The 13 sensor value is : ");
//Serial.println(fsr_value13);
//Serial.print("The 14 sensor value is : ");
//Serial.println(fsr_value14);
//Serial.print("The 15 sensor value is : ");
//Serial.println(fsr_value15);
//Serial.print("The 16 sensor value is : ");
//Serial.println(fsr_value16);
//Serial.println("----------------------------");
//delay(500);

//Connect to python
 if (Serial.available())
 {
  if ('s'==Serial.read())
  {
    int fsr_value = analogRead(fsr_pin); // 讀取FSR
    int fsr_value2 = analogRead(fsr_pin2);
    int fsr_value3 = analogRead(fsr_pin3);
    int fsr_value4 = analogRead(fsr_pin4);
    int fsr_value5 = analogRead(fsr_pin5);
    int fsr_value6 = analogRead(fsr_pin6);
    int fsr_value7 = analogRead(fsr_pin7);
    int fsr_value8 = analogRead(fsr_pin8);
    int fsr_value9 = analogRead(fsr_pin9);
    int fsr_value10 = analogRead(fsr_pin10);
    int fsr_value11 = analogRead(fsr_pin11);
    int fsr_value12 = analogRead(fsr_pin12);
    int fsr_value13 = analogRead(fsr_pin13);
    int fsr_value14 = analogRead(fsr_pin14);
    int fsr_value15 = analogRead(fsr_pin15);
    int fsr_value16 = analogRead(fsr_pin16);
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

      if (fsr_value10 <200)
      {
       Serial.println(0);
      }
     else 
      {
      Serial.println(fsr_value10);
      }

      if (fsr_value11 <200)
      {
       Serial.println(0);
      }
     else 
      {
      Serial.println(fsr_value11);
      }

      if (fsr_value12 <200)
      {
       Serial.println(0);
      }
     else 
      {
      Serial.println(fsr_value12);
      }

      if (fsr_value13 <200)
      {
       Serial.println(0);
      }
     else 
      {
      Serial.println(fsr_value13);
      }

      if (fsr_value14 <200)
      {
       Serial.println(0);
      }
     else 
      {
      Serial.println(fsr_value14);
      }

      if (fsr_value15 <200)
      {
       Serial.println(0);
      }
     else 
      {
      Serial.println(fsr_value15);
      }

      if (fsr_value16 <200)
      {
       Serial.println(0);
      }
     else 
      {
      Serial.println(fsr_value16);
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
