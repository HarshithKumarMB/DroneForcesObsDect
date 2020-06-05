#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
from std_msgs.msg import String
import math as m
def callback(data):
	global error
	integ_p = 0
	error_p = 0
	#msg.linear.z = 2 * abs(error) + 0.5*(error)
	count_r = 0
	count_l = 0
	count_f = 0
	kp = 1
	ki = 0.001
	kd = 0.7
	global msg
	msg.linear.x = 0.1
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	for i in data.ranges: #accessing every lelement in the list of distances
		
		if(i<15 and i>3):
			ind = data.ranges.index(i) 
			
			if(ind>165 and ind<195): 
				count_r+=1
			if(ind>885 and ind<915):  
				count_l+=1
			if(ind>525 and ind<555):
				count_f+=1
			error = 2/i
			integ = integ_p + error
			der = error - error_p
		else:
			pass
		
	if(count_l>0 and count_r>0 and count_f>0): #large wall
		msg.linear.z = msg.linear.x*0.707
		#msg.linear.x = 0
		#msg.linear.y = 0
			
			
	elif(count_l>0 and count_r==0 and count_f==0):# obs in left only
		#msg.linear.y = -2*msg.linear.x*m.sin(0.00436*ind)
		msg.linear.y = -((kp*error) + (ki*integ) + (kd*der))
		msg.linear.z = 0
			
			
	elif(count_r>0 and count_l==0 and count_f==0):#obs in right only
		#msg.linear.y = 2*msg.linear.x*m.sin(0.00436*ind)
		msg.linear.y = (kp*error)+(ki*integ)+(kd*der)
		msg.linear.z = 0
			
			
	elif(count_r > count_l and (count_l > 0 and count_f > 0)):#obs more right
		if(data.ranges[ind-1] <= 30):
			#msg.linear.y = -2*msg.linear.x*m.cos(0.00436*(540 - ind - 0.174))
			msg.linear.y = -((kp*error) + (ki*integ) + (kd*der))	
			msg.linear.z = 0
				
				
	elif(count_r < count_l and (count_r > 0 and count_f > 0)):#obs more left 
		if(data.ranges[ind+1] <= 30): 
			
			#msg.linear.y = 2*msg.linear.x*m.cos(0.00436*(ind - 540 + 0.174))
			msg.linear.y = ((kp*error) + (ki*integ) + (kd*der))
			msg.linear.z = 0

	elif(count_f>0 and count_r == 0 and count_l == 0):#obs in front
		
		#msg.linear.y = 2*msg.linear.x*m.cos(0.785)
		msg.linear.y = ((kp*error) + (ki*integ) + (kd*der))		
		msg.linear.z = 0


	error_p = error
	integ_p = integ

	
	pub.publish(msg)	
		

				
def listener():
	global msg
	global error_prior
	global integral_prior
	
	msg = Twist()
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("/scan", LaserScan, callback)
	rospy.spin()
	
	rospy.spin()

if __name__ == '__main__':
	listener()


