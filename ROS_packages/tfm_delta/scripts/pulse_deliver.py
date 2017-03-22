#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from tfm_delta.msg import Pulsos
from std_msgs.msg import UInt16
from tfm_delta.msg import trayectorias

from time import sleep

# sinusoide 180:
#tra_f = [63,255,255,255,255,127,223,190,247,119,109,173,106,170,148,146,68,33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#tra_b = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,34,36,146,149,85,90,219,109,221,239,191,127,191,255,251,255,255,225]

# sinusoide 90:
tra_f = [63,255,255,191,119,109,106,146,68,0,0,0,0,0,0,0,0,0,0,0]
tra_b = [0,0,0,0,0,0,0,0,0,0,0,4,146,171,109,189,247,255,239,254]

# aproximacion y circulo:
cir_f1 = [0,0]
cir_b1 = [0,0]
cir_f2 = [0,0]
cir_b2 = [0,0]
cir_f3 = [0,0]
cir_b3 = [0,0]

# recibe trayectorias:
trayec = trayectorias()


pulso_test = Pulsos()
def nopulses():
    pulso_test.id = int(0)
    pulso_test.p1f = int(0)
    pulso_test.p1b = int(0)
    pulso_test.p2f = int(0)
    pulso_test.p2b = int(0)
    pulso_test.p3f = int(0)
    pulso_test.p3b = int(0)


def callback(data):
    global trayec
    trayec = data
    cir_f1 = data.f1
    cir_b1 = data.b1
    cir_f2 = data.f2
    cir_b2 = data.b2
    cir_f3 = data.f3
    cir_b3 = data.b3
    rospy.loginfo('recibido')


def recibir_trayectoria():
    while recibido == 0:
        rospy.Subscriber("trayectorias", trayectorias, callback)


def talker():
    rospy.init_node('generador_pulsos', anonymous=False)
    rospy.Subscriber("trayectorias", trayectorias, callback)
    rospy.loginfo('estoy aqui')
    pub = rospy.Publisher('trenes_pulsos', Pulsos, queue_size=10)
    pub2 = rospy.Publisher('num_pulso', UInt16, queue_size=10)
    rate = rospy.Rate(15.625/2) # 10hz
    i = 0
    sleep(5)
    while not rospy.is_shutdown():
        pulso_test.id = i
        # pulso_test.p1f = cir_f1[i-1]
        # pulso_test.p1b = cir_b1[i-1]
        # pulso_test.p2f = cir_f2[i-1]
        # pulso_test.p2b = cir_b2[i-1]
        # pulso_test.p3f = cir_f3[i-1]
        # pulso_test.p3b = cir_b3[i-1]
        pulso_test.p1f = trayec.f1[i-1]
        pulso_test.p1b = trayec.b1[i-1]
        pulso_test.p2f = trayec.f2[i-1]
        pulso_test.p2b = trayec.b2[i-1]
        pulso_test.p3f = trayec.f3[i-1]
        pulso_test.p3b = trayec.b3[i-1]
        if i < len(trayec.f1): # len(tra_f) para sinusoide   (aantes cir_f1) trayec.f1
            rospy.loginfo(i)
            i += 1
        # if i >= len(tra_f):
        #     nopulses()
        #     rospy.loginfo('trayectoria finalizada')
        pub.publish(pulso_test)
        if i >= len(trayec.f1): # len(tra_f) para sinusoide   (aantes cir_f1) trayec.f1
            nopulses()
            rospy.loginfo('trayectoria finalizada')
        pub2.publish(i)
        rate.sleep()


if __name__ == '__main__':
    try:
        #rospy.init_node('generador_pulsos', anonymous=False)
        #recibir_trayectoria()
        #if recibido:
        #nopulses()
        talker()
    except rospy.ROSInterruptException:
        pass