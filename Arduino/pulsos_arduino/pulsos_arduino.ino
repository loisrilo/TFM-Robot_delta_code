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


//Pines drivers:
int en1 = 2;
int pul1 = 3;
int dir1 = 4;
int en2 = 5;
int dir2 = 6;
int pul2 = 7;
int en3 = 8;
int pul3 = 9;
int dir3 = 10;

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


//driver:
boolean control_loop = 0;
int i = 0;
byte p1f = 0;
byte p1b = 0;
byte p2f = 0;
byte p2b = 0;
byte p3f = 0;
byte p3b = 0;
int pos2 = 0;


int ancho_pulso = 500;
int post_pulso = 500;

void adelante1(){
  digitalWrite(4,1);
  digitalWrite(3,!digitalRead(3));
  delayMicroseconds(ancho_pulso);
  digitalWrite(3,!digitalRead(3));
  delayMicroseconds(post_pulso);
}

void atras1(){
  digitalWrite(dir1,0);
  digitalWrite(3,!digitalRead(3));
  delayMicroseconds(ancho_pulso);
  digitalWrite(3,!digitalRead(3));
  delayMicroseconds(post_pulso); 
}

void adelante2(){
  digitalWrite(en2,1);
  digitalWrite(dir2,1);
  digitalWrite(pul2,!digitalRead(pul2));
  delayMicroseconds(ancho_pulso);
  digitalWrite(pul2,!digitalRead(pul2));
  delayMicroseconds(post_pulso);
}

void atras2(){
  digitalWrite(en2,1);
  digitalWrite(dir2,0);
  digitalWrite(pul2,!digitalRead(pul2));
  delayMicroseconds(ancho_pulso);
  digitalWrite(pul2,!digitalRead(pul2));
  delayMicroseconds(post_pulso);
}

void adelante3(){
  digitalWrite(dir3,1);
  digitalWrite(pul3,!digitalRead(pul3));
  delayMicroseconds(ancho_pulso);
  digitalWrite(pul3,!digitalRead(pul3));
  delayMicroseconds(post_pulso);
}

void atras3(){
  digitalWrite(dir3,0);
  digitalWrite(pul3,!digitalRead(pul3));
  delayMicroseconds(ancho_pulso);
  digitalWrite(pul3,!digitalRead(pul3));
  delayMicroseconds(post_pulso); 
}


//void origen() {
//  forwardstep1(); 
//  forwardstep2(); 
//  forwardstep3(); 
//}

void setup()
{ 
  //ros:
  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.subscribe(sub);
  //  nh.advertise(pub);
  nh.advertise(posicion_stepper); 
  //driver:
  pinMode(en1,OUTPUT);
  pinMode(pul1,OUTPUT);
  pinMode(dir1,OUTPUT);
  pinMode(en2,OUTPUT);
  pinMode(pul2,OUTPUT);
  pinMode(dir2,OUTPUT);
  pinMode(en3,OUTPUT);
  pinMode(pul3,OUTPUT);
  pinMode(dir3,OUTPUT);
  
  
//  origen();
  posicion.stepper1 = 0;
  posicion.stepper2 = 0;
  posicion.stepper3 = 0; 
  
  //timer:
  Timer1.initialize(16000); //16ms
  Timer1.attachInterrupt(ISR_Blink);
}

void ISR_Blink(){   
  if (control_loop == 0){
    control_loop = 1;
  }
  else {
    // error:
    nh.logwarn("error, se ha excedido el tiempo de ciclo.");
  }
}

void loop()
{

  if (control_loop == 1) {

    //driver:
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
        adelante1(); 
        posicion.stepper1++;
      }
      if(p1b>>i & 0b1){
        atras1(); 
        posicion.stepper1--;
      }

      if(p2f>>i & 0b1){
        adelante2();
        posicion.stepper2++;
      }
      if(p2b>>i & 0b1){
        atras2();
        posicion.stepper2--;
      }

      if(p3f>>i & 0b1){
        adelante3();
        posicion.stepper3++;
      }
      if(p3b>>i & 0b1){
        atras3();
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


