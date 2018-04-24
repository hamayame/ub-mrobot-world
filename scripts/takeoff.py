#!/usr/bin/env python 
import rospy 
from std_msgs.msg import String 
from std_msgs.msg import Empty 

def run(): 
   pub = rospy.Publisher("ardrone/takeoff", Empty, queue_size=10 ) 
   rospy.sleep(1.0)
   pub.publish(Empty())


if __name__ == '__main__': 
   try: 
       	rospy.init_node('takeoff', anonymous=True) 
       	rate = rospy.Rate(10) # 10hz 
       	while not rospy.is_shutdown():
       	       	run() 
       	       	rate.sleep()
   except rospy.ROSInterruptException: 
       pass
