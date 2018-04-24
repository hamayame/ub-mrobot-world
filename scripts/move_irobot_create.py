#!/usr/bin/env python 
import rospy 
from geometry_msgs.msg import Twist
from std_msgs.msg import String 
from std_msgs.msg import Empty 

def run(): 
	pub_move = rospy.Publisher("cmd_vel_create", Twist, queue_size=1 ) 

	move_to_front = Twist()
	move_to_front.linear.x = 1
	move_to_front.linear.y = 0
	move_to_front.linear.z = 0
	move_to_front.angular.x = 0
	move_to_front.angular.y = 0
	move_to_front.angular.z = 0

	move_to_back = Twist()
	move_to_back.linear.x = -1
	move_to_back.linear.y = 0
	move_to_back.linear.z = 0
	move_to_back.angular.x = 0
	move_to_back.angular.y = 0
	move_to_back.angular.z = 0

	rospy.sleep(1.0)
	pub_move.publish(move_to_back) 
	rospy.loginfo("iCreate move Back!")
	rospy.sleep(5.0)
	pub_move.publish(move_to_front)
	rospy.loginfo("iCreate move Front!")
	rospy.sleep(5.0)


if __name__ == '__main__': 
   try: 
	rospy.init_node('move_irobot_create', anonymous=True) 
	rate = rospy.Rate(0.1) # 0.1hz / 10s
       	while not rospy.is_shutdown():
       	       	run() 
   except rospy.ROSInterruptException: 
       pass
