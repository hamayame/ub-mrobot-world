#!/usr/bin/env python 
import rospy 
from geometry_msgs.msg import Twist
from cmvision.msg import Blobs, Blob

#global
move_x = 0.0
move_y = 0.0
blob_pos_x = 0.0
blob_pos_y = 0.0

def callback(data):
	global move_x
	global move_y
	global blob_pos_x
	global blob_pos_y

	if( len( data.blobs ) ):
		for obj in data.blobs:
			if( obj.name == "iCreate" ):
				blob_pos_x = obj.x #blob(x) -> width
				blob_pos_y = obj.y #blob(y) -> height

				#Luas ukuran video kamera bawah quadcopter
				#(WxH) : 640x360

				if( blob_pos_y < 170 ):
					move_y = 0.3
				if( blob_pos_y > 190 ):
					move_y = -0.3
				if( blob_pos_y > 170 and blob_pos_y < 190):
					move_y = 0

				if( blob_pos_x < 310 ):
					move_x = 0.3 
				if( blob_pos_x > 330 ):
					move_x = -0.3
				if( blob_pos_x > 310 and blob_pos_x < 330):
					move_x = 0

def run(): 
	global move_x
	global move_y
	global blob_pos_x
	global blob_pos_y

	pub_cmove = rospy.Publisher("cmd_vel", Twist, queue_size=10 ) 

	rospy.Subscriber('/blobs', Blobs, callback)

	move_copter = Twist()
	move_copter.linear.z = 0
	move_copter.angular.x = 0
	move_copter.angular.y = 0
	move_copter.angular.z = 0

	if( move_x != 0 or move_y != 0 ):
		move_copter.linear.y = move_x
		move_copter.linear.x = move_y
		print("move_x:" + str(move_x) + " move_y:" + str(move_y))
		move_x = 0
		move_y = 0
	else:
		move_copter.linear.x = 0
		move_copter.linear.y = 0

	pub_cmove.publish(move_copter)
	blob_pos_x = 0
	blob_pos_y = 0

if __name__ == '__main__': 
   try: 
       	rospy.init_node('track_follow_blob', anonymous=True) 
       	rate = rospy.Rate(10) # 10hz 
       	while not rospy.is_shutdown():
       	       	run() 
       	       	rospy.sleep(0.07)
   except rospy.ROSInterruptException: 
       pass
