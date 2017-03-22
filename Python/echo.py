#!/usr/bin/env python

# -*- coding: utf-8 -*-
# Copyright 2016 Lois Rilo Antelo (loisriloantelo@gmail.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import rospy
from std_msgs.msg import String

import time


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)


def listener():
    # rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('chatter', String, callback)

    # rospy.spin()


if __name__ == '__main__':
    try:

        rospy.init_node('dual', anonymous=False)
        # rospy.Subscriber('chatter', String, callback)
        pub1 = rospy.Publisher('chatter_dual', String, queue_size=10)
        # hello_str = "soy dual %s" % rospy.get_time()
        rate = rospy.Rate(10)  # 10hz
        while not rospy.is_shutdown():
            rospy.loginfo('here i am')
            str_joan = 'hola' + str(time.time())
            pub1.publish(str_joan)
            rospy.loginfo('again')
            rate.sleep()

    except rospy.ROSInterruptException:
        raise
