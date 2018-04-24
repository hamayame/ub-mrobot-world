#!/usr/bin/env python 
import subprocess

import takeoff	#import 'takeoff.py' dari folder yg sama
import move_irobot_create
import follow_blob

import rospy 
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_msgs.msg import Empty 

if __name__ == '__main__': 
	try: 
		rospy.init_node('move_follow_robot', anonymous=True) 
		rate = rospy.Rate(1) # 1hz / 1s

		init_fly = False # variable lock yg digunakan untuk takeoff quadcopter diawal program berjalan

		subprocess.call(["source devel/setup.bash && rosrun world-proj follow_blob.py"])
		rospy.sleep(1.0)

		while not rospy.is_shutdown():
#			follow_blob.run()
			if( init_fly == False ):
				takeoff.run()
				print("takeoff!")
				start_follow.communicate()
				print("follow!")
				init_fly = True
			move_irobot_create.run()
#			run() 
	except rospy.ROSInterruptException: 
		pass
