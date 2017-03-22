// Shows how to run three Steppers at once with varying speeds
//
// Requires the Adafruit_Motorshield v2 library 
//   https://github.com/adafruit/Adafruit_Motor_Shield_V2_Library
// And AccelStepper with AFMotor support 
//   https://github.com/adafruit/AccelStepper

// This tutorial is for Adafruit Motorshield v2 only!
// Will not work with v1 shields
#include <stdlib.h>
#include <AccelStepper.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <TimerOne.h>

boolean control_loop = 0;
int i = 0;
byte p1f = 0;
byte p1b = 0;
byte p2f = 0;
byte p2b = 0;
byte p3f = 0;
byte p3b = 255;
int pos2 = 0;

//pruebas trayectorias:
int j = 0;
byte tra_f[40] = {63,255,255,255,255,127,223,190,247,119,109,173,106,170,148,146,68,33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
byte tra_b[40] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,34,36,146,149,85,90,219,109,221,239,191,127,191,255,251,255,255,224};


Adafruit_MotorShield AFMSbot(0x61); // Rightmost jumper closed
Adafruit_MotorShield AFMStop(0x60); // Default address, no jumpers

// Connect two steppers with 200 steps per revolution (1.8 degree)
// to the top shield
Adafruit_StepperMotor *myStepper1 = AFMStop.getStepper(200, 1);
Adafruit_StepperMotor *myStepper2 = AFMStop.getStepper(200, 2);

// Connect one stepper with 200 steps per revolution (1.8 degree)
// to the bottom shield
Adafruit_StepperMotor *myStepper3 = AFMSbot.getStepper(200, 2);

// you can change these to DOUBLE or INTERLEAVE or MICROSTEP!
// wrappers for the first motor!
void forwardstep1() {  
  myStepper1->onestep(FORWARD, SINGLE);
}
void backwardstep1() {  
  myStepper1->onestep(BACKWARD, SINGLE);
}
// wrappers for the second motor!
void forwardstep2() {  
  myStepper2->onestep(FORWARD, SINGLE);
}
void backwardstep2() {  
  myStepper2->onestep(BACKWARD, SINGLE);
}
// wrappers for the third motor!
void forwardstep3() {  
  myStepper3->onestep(FORWARD, SINGLE);
  //INTERLEAVE
}
void backwardstep3() {  
  myStepper3->onestep(BACKWARD, SINGLE);
}

// Now we'll wrap the 3 steppers in an AccelStepper object
AccelStepper stepper1(forwardstep1, backwardstep1);
AccelStepper stepper2(forwardstep2, backwardstep2);
AccelStepper stepper3(forwardstep3, backwardstep3);

void setup()
{ 
  AFMSbot.begin(); // Start the bottom shield
  AFMStop.begin(); // Start the top shield
  
  Timer1.initialize(20000); //10ms
  Timer1.attachInterrupt(ISR_Blink);
  
  Serial.begin(115200);
   
}

void ISR_Blink(){   
  if (control_loop == 0){
    control_loop = 1;
    //digitalWrite(pin_error,LOW);
  }else {
    // error:
    //digitalWrite(pin_error, HIGH);
    Serial.print("ERROR: SE HA EXCEDIDO EL TIEMPO DE CICLO");
  }
}

void loop()
{
  if (control_loop == 1) {
    
    if(j<40){
      p1f = tra_f[j];
      p1b = tra_b[j];
    }
    else{
      p1f = 0;
      p1b = 0;
    }
    
    if(j<40){
      p2f = tra_f[j];
      p2b = tra_b[j];
    }
    else{
      p2f = 0;
      p2b = 0;
    }
      
    p3f = 0;
    p3b = 16;
//PROBLEMA CON SPEED() Y SETSPEED()...
//    stepper1.setSpeed(1.0);
//    if(ristra>>i & 0b1){Serial.println("True");}
//    else{Serial.println("False");}
//    if(0b11000000>>i & 0b1){forwardstep1();}
//    if(0b11000000>>i & 0b1){backwardstep1();}
    
    if(p1f>>i & 0b1){forwardstep1();}
    if(p1b>>i & 0b1){backwardstep1();}
    
    if(p2f>>i & 0b1){forwardstep2();pos2++;}
    if(p2b>>i & 0b1){backwardstep2();pos2--;}
    
    if(p3f>>i & 0b1){forwardstep3();}
    if(p3b>>i & 0b1){backwardstep3();}    
    
    i++;
    if(i>7){i=0;j++;}
    if(j>40){Serial.println("HE ACABADO TIO!");}
    Serial.println(pos2);
//    Serial.println(0b1001>>0);
//    
    
    

//    Serial.println(0b00001001);

    control_loop = 0;
  }

}
