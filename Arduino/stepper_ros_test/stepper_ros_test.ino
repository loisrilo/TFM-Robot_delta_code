//ROS:
#include <ros.h>
#include <tfm_delta/pulsos.h>
//adafruit:
#include <stdlib.h>
#include <AccelStepper.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <TimerOne.h>


//ros:
ros::NodeHandle  nh;
tfm_delta::pulsos recibido;
//tfm_delta::pulsos comparacion;
boolean nuevo = 0;
boolean done = 0;

void messageCb( const tfm_delta::pulsos& escuchado){
  if (recibido.p1f != escuchado.p1f | recibido.p2f != escuchado.p2f){
    recibido = escuchado;
    nuevo= 1;
  }
}

ros::Subscriber<tfm_delta::pulsos> sub("trenes_pulsos", &messageCb );
ros::Publisher pub("pulsos_arduino", &recibido);


//adafruit:
boolean control_loop = 0;
int i = 0;
byte p1f = 0;
byte p1b = 0;
byte p2f = 0;
byte p2b = 0;
byte p3f = 0;
byte p3b = 0;
int pos2 = 0;

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
  //ros:
  nh.initNode();
  nh.subscribe(sub);
  nh.advertise(pub);
  //adafruit:
  AFMSbot.begin(); // Start the bottom shield
  AFMStop.begin(); // Start the top shield
  //timer:
  Timer1.initialize(200000); //10ms
  Timer1.attachInterrupt(ISR_Blink);
}

void ISR_Blink(){   
  if (control_loop == 0){
    control_loop = 1;
    //digitalWrite(pin_error,LOW);
  }else {
    // error:
    //digitalWrite(pin_error, HIGH);
//    Serial.print("ERROR: SE HA EXCEDIDO EL TIEMPO DE CICLO");
  }
}

void loop()
{

  if (control_loop == 1) {

    //adafruit:
    if(nuevo==1){
      pub.publish( &recibido);
      
      p1f = recibido.p1f;
      p1b = recibido.p1b;

      p2f = recibido.p2f;
      p2b = recibido.p2b;
      
      p3f = recibido.p3f;
      p3b = recibido.p3b;
      nuevo = 0;
      done = 0;
    }

    if(done == 0){
      if(p1f>>i & 0b1){forwardstep1();}
      if(p1b>>i & 0b1){backwardstep1();}
    
      if(p2f>>i & 0b1){forwardstep2();pos2++;}
      if(p2b>>i & 0b1){backwardstep2();pos2--;}
    
      if(p3f>>i & 0b1){forwardstep3();}
      if(p3b>>i & 0b1){backwardstep3();}  
      
      i++;
      if(i>7){i=0; done = 1;}
    }
    
    if(done == 1){nh.spinOnce();}

    control_loop = 0;
  }
}

