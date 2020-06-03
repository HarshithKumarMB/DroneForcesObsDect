#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
from std_msgs.msg import String
import math as m
def callback(data):
	global n
	count_r = 0
	count_l = 0
	global msg
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	for i in data.ranges:
		if(i<7 and i>3):
			ind = data.ranges.index(i)
			rospy.loginfo(ind)
			if(ind<540 and ind>240):
				count_r+=1
			if(ind>540 and ind<840):
				count_l+=1
		else:
			pass
		if(count_l>300 and count_r>300): 
			rospy.loginfo("for a large wall")
			msg.linear.z = msg.linear.x
			
			
		elif(count_l>0 and count_r==0):
			rospy.loginfo("for an obstacle in left only")
			msg.linear.y = -2*msg.linear.x*m.sin(0.00436*ind)
			
			
		elif(count_r>0 and count_l==0): 
			rospy.loginfo("for an obstacle in right only")
			msg.linear.y = 2*msg.linear.x*m.sin(0.00436*ind)
			
			
		elif(count_r > count_l): #for obstacle stretching both sides
			if(data.ranges[ind-1] <= 30):
				rospy.loginfo("for finding the right most point of the obstacle")
				msg.linear.y = -2*msg.linear.x*m.cos(0.00436*(540 - ind - 0.174))
				
				
		elif(count_r < count_l): #for obstacle stretching both sides
			if(data.ranges[ind+1] <= 30): 
				rospy.loginfo("for finding the left most point of the obstacle")
				msg.linear.y = 2*msg.linear.x*m.cos(0.00436*(ind - 540 + 0.174))

		elif(abs(count_l - count_r) < 200 and count_r < 100 and count_l < 100 and data.ranges[540]<30): 
			rospy.loginfo("for obstacle in front and by default moves 30 degree in left")
			msg.linear.y = (2*msg.linear.x*m.cos(0.785)
			
	pub.publish(msg)	
		
				
def listener():
	global msg
	msg = Twist()
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("/scan", LaserScan, callback)
	rospy.spin()
if __name__ == '__main__':
	listener()


