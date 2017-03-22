#include <ros.h>
#include <std_msgs/UInt8.h>
#include <std_msgs/UInt16.h>
#include <tfm_delta/pulsos.h>

ros::NodeHandle  nh;

byte a = 0;

void messageCb( const std_msgs::UInt8& numero){
  a = numero.data;
}

void fun (const std_msgs::UInt16& numero){
  //
}

void funcion (const tfm_delta::pulsos& numero){
  //
}

ros::Subscriber<std_msgs::UInt8> sub("integer", &messageCb );
ros::Subscriber<std_msgs::UInt16> subs("otro", &fun );
ros::Subscriber<tfm_delta::pulsos> sub3("another", &funcion);

std_msgs::UInt8 number;
ros::Publisher tomalo("lois", &number);

void setup()
{ 
  nh.initNode();
  nh.subscribe(sub);
  nh.subscribe(subs);
  nh.subscribe(sub3);
  nh.advertise(tomalo);
}

void loop()
{
  number.data = a;
  tomalo.publish( &number);
  nh.spinOnce();
  delay(100);
}

