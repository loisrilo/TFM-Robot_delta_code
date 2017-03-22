#include <TimerOne.h>

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

int i = 0;
int j = 0;

boolean control_loop = 0;

//pruebas trayectorias:
int k = 0;
byte tra_f[40] = {63,255,255,255,255,127,223,190,247,119,109,173,106,170,148,146,68,33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
byte tra_b[40] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,34,36,146,149,85,90,219,109,221,239,191,127,191,255,251,255,255,225};
byte p1f = 0;
byte p1b = 0;


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

void setup() { 
  pinMode(en1,OUTPUT);
  pinMode(pul1,OUTPUT);
  pinMode(dir1,OUTPUT);
  pinMode(en2,OUTPUT);
  pinMode(pul2,OUTPUT);
  pinMode(dir2,OUTPUT);
  pinMode(en3,OUTPUT);
  pinMode(pul3,OUTPUT);
  pinMode(dir3,OUTPUT);
  
  Timer1.initialize(3000); //1500 motor
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

void loop(){
  if (control_loop == 1) {
    
    if(j<40){
        p1f = tra_f[j];
        p1b = tra_b[j];
      }
      else{
        p1f = 0;
        p1b = 0;
      }
    
      if(p1f>>i & 0b1){adelante1();}
      if(p1b>>i & 0b1){atras1();}
      
      if(p1f>>i & 0b1){adelante2();}
      if(p1b>>i & 0b1){atras2();}
      
      if(p1f>>i & 0b1){adelante3();}
      if(p1b>>i & 0b1){atras3();}
    
      i++;
      if(i>7){i=0;j++;}
      if(j>40){Serial.println("HE ACABADO TIO!");}
    
    control_loop = 0;
  }
    
    //FIRST TRIAL:
//  if(i<200){
//    adelante1();
//    i++;
//  }
//  if(i>=200){
//    if(j<200){
//      atras1();
//      j++;
//    }
//  }
}
