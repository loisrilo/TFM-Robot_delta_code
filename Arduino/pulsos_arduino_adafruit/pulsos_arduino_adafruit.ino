//ROS:
#include <ros.h>
#include <tfm_delta/Pulsos.h>
#include <std_msgs/UInt8.h>
#include <tfm_delta/stepper_pos.h>


//adafruit:
#include <stdlib.h>
#include <AccelStepper.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <TimerOne.h>


//ros:
//ros::NodeHandle  nh;
ros::NodeHandle_<ArduinoHardware, 2, 1, 280, 280> nh;

tfm_delta::Pulsos recibido;
tfm_delta::stepper_pos posicion;


boolean nuevo = 0;
boolean done = 0;

void messageCb( const tfm_delta::Pulsos& escuchado){
  if (recibido.id != escuchado.id){
    recibido = escuchado;
    nuevo= 1;
  }
}

ros::Subscriber<tfm_delta::Pulsos> sub("trenes_pulsos", &messageCb );
//ros::Publisher pub("pulsos_arduino", &recibido);
ros::Publisher posicion_stepper("pos_steppers", &posicion);


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


void origen() {
  forwardstep1(); 
  forwardstep2(); 
  forwardstep3(); 
}

void setup()
{ 
  //ros:
  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.subscribe(sub);
  //  nh.advertise(pub);
  nh.advertise(posicion_stepper); 
  //adafruit:
  AFMSbot.begin(); // Start the bottom shield
  AFMStop.begin(); // Start the top shield
  
  origen();
  posicion.stepper1 = 0;
  posicion.stepper2 = 0;
  posicion.stepper3 = 0; 
  
  //timer:
  Timer1.initialize(80000); //10ms
  Timer1.attachInterrupt(ISR_Blink);
}

void ISR_Blink(){   
  if (control_loop == 0){
    control_loop = 1;
    //digitalWrite(pin_error,LOW);
  }
  else {
    // error:
    nh.logwarn("error, se ha excedido el tiempo de ciclo.");
  }
}

void loop()
{

  if (control_loop == 1) {

    //adafruit:
    if(nuevo==1){
      //pub.publish( &recibido);
      

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
      if(p1f>>i & 0b1){
        forwardstep1(); 
        posicion.stepper1++;
      }
      if(p1b>>i & 0b1){
        backwardstep1(); 
        posicion.stepper1--;
      }

      if(p2f>>i & 0b1){
        forwardstep2();
        posicion.stepper2++;
      }
      if(p2b>>i & 0b1){
        backwardstep2();
        posicion.stepper2--;
      }

      if(p3f>>i & 0b1){
        forwardstep3();
        posicion.stepper3++;
      }
      if(p3b>>i & 0b1){
        backwardstep3();
        posicion.stepper3--;
      }  

      i++;
      if(i>7){
        i=0; 
        done = 1;
      }
    }

    posicion.stepper2 = recibido.id;
    
    if(done == 1){
      nh.spinOnce();
      posicion_stepper.publish( &posicion);
    }
    
//    nh.loginfo("hola");

    control_loop = 0;
  }
}


