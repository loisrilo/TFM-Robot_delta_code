#!/usr/bin/env python

import rospy
#from std_msgs.msg import String
from tfm_delta.msg import array_try
from tfm_delta.msg import trayectorias
#from std_msgs.msg import UInt16

a = [0,0,0,0,0,0,0,0,0,0,0,4,146,171,109,189,247,255,239,254]

b = array_try()

#def callback(data):
 #   rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)


def talker():
    rospy.init_node('array_test', anonymous=False)
    pub = rospy.Publisher('array_pub', array_try, queue_size=10)
    rate = rospy.Rate(0.5) # 10hz
    while not rospy.is_shutdown():
        b.arraytry = a
        b.arraytry2 = [1,2,3]
        pub.publish(b)
        # rospy.Subscriber("me_suscribo", String, callback)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass