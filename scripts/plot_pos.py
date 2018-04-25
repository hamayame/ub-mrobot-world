#!/usr/bin/env python 
import follow_blob

import rospy 
from geometry_msgs.msg import Pose, Vector3
from ardrone_autonomy.msg import Navdata

from gazebo_msgs.srv import GetModelState

#constant
#sesuai dokumentasi ardrone_autonomy (http://docs.ros.org/indigo/api/ardrone_autonomy/html/msg/Navdata.html)
TIME = 1 #seconds
POS = 1000 #(position) milimeters -> meters

#sesuai webpage (https://www.unitconverters.net/typography/centimeter-to-pixel-x.htm)
PIXEL = (0.0264583333 / 100)  #centimeters -> meters

#sesuai webpage (http://www.endmemo.com/sconvert/m_s2g.php)
ACC_GRAVITY = 0.101972 #g

#global
qc_vx = 0 #velocity
qc_vy = 0
qc_vz = 0
qc_atx = 0.0 #acceleration time
qc_aty = 0.0
qc_atz = 0.0
pos_x = 0
pos_y = 0
pos_z = 0
qc_pos = Pose()

found = False
data_found = 1
blob_pos_x = 0.0
blob_pos_y = 0.0
blob_avg_x = 0.0
blob_avg_y = 0.0

irobot_avg_vx = 0.0
irobot_avg_vy = 0.0

def position_drone(velocity):
	return velocity*TIME/POS

def velocity(position, time):
	return position/time

def get_model_pos_on_world(name, link):
	model_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
	resp_model_state = model_state(name, link)
	qc_pos = resp_model_state.pose

def callback(data):
	global qc_vx
	global qc_vy
	global qc_vz
	global qc_atx
	global qc_aty
	global qc_atz

	qc_vx = data.vx
	qc_vy = data.vy
	qc_vz = data.vz

	qc_atx = qc_vx / (data.ax * ACC_GRAVITY)
	qc_aty = qc_vy / (data.ay * ACC_GRAVITY)
	qc_atz = qc_vz / (data.az * ACC_GRAVITY)

def run():
	global qc_vx
	global qc_vy
	global qc_vz
	global qc_atx
	global qc_aty
	global qc_atz
	global pos_x
	global pos_y
	global pos_z
	global found
	global data_found
	global blob_pos_x
	global blob_pos_y
	global blob_avg_x
	global blob_avg_y
	global irobot_avg_vx
	global irobot_avg_vy

	found, blob_pos_x, blob_pos_y = follow_blob.position()	

	rospy.Subscriber('/ardrone/navdata', Navdata, callback)
	
	pos_x += position_drone(qc_vx)
	pos_y += position_drone(qc_vy)
	pos_z += position_drone(qc_vz)

	qc_pos.position.x = pos_x
	qc_pos.position.y = pos_y
	qc_pos.position.z = pos_z

	irobot_pos = Pose()
	irobot_pos.position.z = 0

	irobot_pos_abs = Pose()
	irobot_pos_abs.position.z = 0

	irobot_vec = Vector3()
	irobot_vec.z = 0

	irobot_avg_vec = Vector3()
	irobot_avg_vec.z = 0

	if( found == True ):
		blob_pos_x = ((blob_pos_x - 320) * PIXEL) 
		blob_pos_y = (-(blob_pos_y - 180) * PIXEL) 

		irobot_pos.position.x = blob_pos_x
		irobot_pos.position.y = blob_pos_y

		irobot_pos_abs.position.x = pos_x + blob_pos_x
		irobot_pos_abs.position.y = pos_y + blob_pos_y

		blob_avg_x += abs(irobot_pos.position.x)
		blob_avg_y += abs(irobot_pos.position.x)

		irobot_vec.x = velocity((blob_avg_x / data_found), qc_atx)
		irobot_vec.y = velocity((blob_avg_y / data_found), qc_aty)

		irobot_avg_vx += (irobot_vec.x / data_found)
		irobot_avg_vy += (irobot_vec.y / data_found)

		irobot_avg_vec.x = irobot_avg_vx
		irobot_avg_vec.y = irobot_avg_vy

		data_found += 1
	else:
		irobot_pos.position.x = 0
		irobot_pos.position.y = 0

		irobot_vec.x = 0
		irobot_vec.y = 0
		irobot_vec.z = 0

	pub_qc_pose = rospy.Publisher('drone_pos', Pose, queue_size=10)
	pub_qc_pose.publish(qc_pos)

	pub_irobot_pose = rospy.Publisher('robot_pos_relative', Pose, queue_size=10)
	pub_irobot_pose.publish(irobot_pos)

	pub_irobot_pose_abs = rospy.Publisher('robot_pos_absolute', Pose, queue_size=10)
	pub_irobot_pose.publish(irobot_pos_abs)

	pub_irobot_vec = rospy.Publisher('robot_vector', Vector3, queue_size=10)
	pub_irobot_vec.publish(irobot_vec)

	pub_irobot_avg_vec = rospy.Publisher('robot_avg_vector', Vector3, queue_size=10)
	pub_irobot_avg_vec.publish(irobot_avg_vec)

	print("pos_x:" + str(pos_x) + " pos_y:" + str(pos_y) + " pos_z:" + str(pos_z))
	print("pos_x_abs:" + str(irobot_pos_abs.position.x) + " pos_y_abs:" + str(irobot_pos_abs.position.y) + " pos_z_abs:" + str(irobot_pos_abs.position.z))
	print("pos_x_robot:" + str(blob_pos_x) + " pos_y_robot:" + str(blob_pos_y) + " pos_z_robot:0")
	print("vec_x_robot:" + str(irobot_vec.x) + " vec_y_robot:" + str(irobot_vec.y) + " vec_z_robot:" + str(irobot_vec.z))
	print("avec_x_robot:" + str(irobot_avg_vec.x) + " avec_y_robot:" + str(irobot_avg_vec.y) + " avec_z_robot:" + str(irobot_avg_vec.z))
	print("==============")

if __name__ == '__main__': 

   model_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
   rospy.wait_for_service("/gazebo/get_model_state")

   try: 
       	rospy.init_node('node_drone_pos', anonymous=True) 
       	rate = rospy.Rate(10) # 10hz 

	resp_model_state = model_state(model_name="quadrotor")
	qc_pos = resp_model_state.pose	
	
	pos_x = qc_pos.position.x
	pos_y = qc_pos.position.y
	pos_z = qc_pos.position.z

       	while not rospy.is_shutdown():
      	       	run() 
       	       	rate.sleep()
   except rospy.ROSInterruptException: 
       pass
