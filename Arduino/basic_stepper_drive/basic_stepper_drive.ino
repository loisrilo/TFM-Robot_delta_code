int delaylegnth = 100;
int pulso = 2;

void setup() { 
  //establish motor direction toggle pins
  pinMode(12, OUTPUT); //CH A -- HIGH = forwards and LOW = backwards???
  pinMode(13, OUTPUT); //CH B -- HIGH = forwards and LOW = backwards???
  
  //establish motor brake pins
  pinMode(9, OUTPUT); //brake (disable) CH A
  pinMode(8, OUTPUT); //brake (disable) CH B
  
  Serial.begin(115200);
  
}

void loop(){
 
  mover_p(50);
  //Serial.println(pulso);
  delay(2000);
  mover_n(50);
  delay(2000);

}

//fucion para mover el stepper el numero de pasos deseado, direccion positiva:
void mover_p(int x){
  int i=0;
  
  while(i<x){
    
    if(pulso==4){
      digitalWrite(9, LOW);  //ENABLE CH A
      digitalWrite(8, HIGH); //DISABLE CH B

      digitalWrite(12, HIGH);   //Sets direction of CH A
      analogWrite(3, 255);   //Moves CH A
    
      pulso=1;
      Serial.println(pulso);
      i++;
      //Serial.println(i);
      delay(delaylegnth); 
    }
    if(i>=x){break;}
    
    if(pulso==1){
      digitalWrite(9, HIGH);  //DISABLE CH A
      digitalWrite(8, LOW); //ENABLE CH B

      digitalWrite(13, LOW);   //Sets direction of CH B
      analogWrite(11, 255);   //Moves CH B
    
      pulso=2;
      Serial.println(pulso);
      i++;
      //Serial.println(i);
      delay(delaylegnth);
    }
    if(i>=x){break;}
  
    if(pulso==2){
      digitalWrite(9, LOW);  //ENABLE CH A
      digitalWrite(8, HIGH); //DISABLE CH B

      digitalWrite(12, LOW);   //Sets direction of CH A
      analogWrite(3, 255);   //Moves CH A
    
      pulso=3;
      Serial.println(pulso);
      i++;
      //Serial.println(i);
      delay(delaylegnth);
    }
    if(i>=x){break;}
    
    if(pulso==3){
      digitalWrite(9, HIGH);  //DISABLE CH A
      digitalWrite(8, LOW); //ENABLE CH B

      digitalWrite(13, HIGH);   //Sets direction of CH B
      analogWrite(11, 255);   //Moves CH B
    
      pulso=4;
      Serial.println(pulso);
      i++;
      //Serial.println(i);
      delay(delaylegnth);
    }
    if(i>=x){break;}
    
  }
  
}


//fucion para mover el stepper el numero de pasos deseado, direccion negativa:
void mover_n(int x){
  int i=0;
  //Serial.println(pulso);


  while(i<x){
    
    if(pulso==2){
      digitalWrite(9, LOW);  //ENABLE CH A
      digitalWrite(8, HIGH); //DISABLE CH B

      digitalWrite(12, HIGH);   //Sets direction of CH A
      analogWrite(3, 255);   //Moves CH A
    
      pulso=1;
      Serial.println(pulso);
      i++;
      //Serial.println(i);
      delay(delaylegnth); 
    }
    if(i>=x){break;}
    
    if(pulso==3){
      digitalWrite(9, HIGH);  //DISABLE CH A
      digitalWrite(8, LOW); //ENABLE CH B

      digitalWrite(13, LOW);   //Sets direction of CH B
      analogWrite(11, 255);   //Moves CH B
    
      pulso=2;
      Serial.println(pulso);
      i++;
      //Serial.println(i);
      delay(delaylegnth);
    }
    if(i>=x){break;}
  
    if(pulso==4){
      digitalWrite(9, LOW);  //ENABLE CH A
      digitalWrite(8, HIGH); //DISABLE CH B

      digitalWrite(12, LOW);   //Sets direction of CH A
      analogWrite(3, 255);   //Moves CH A
    
      pulso=3;
      Serial.println(pulso);
      i++;
      //Serial.println(i);
      delay(delaylegnth);
    }
    if(i>=x){break;}
    
    if(pulso==1){
      digitalWrite(9, HIGH);  //DISABLE CH A
      digitalWrite(8, LOW); //ENABLE CH B

      digitalWrite(13, HIGH);   //Sets direction of CH B
      analogWrite(11, 255);   //Moves CH B
    
      pulso=4;
      Serial.println(pulso);
      i++;
      //Serial.println(i);
      delay(delaylegnth);
    }
    if(i>=x){break;}
  }
  
}


