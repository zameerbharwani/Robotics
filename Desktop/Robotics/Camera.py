#!/usr/bin/env python
import Joy
import rospy

class GimbalController:

	def __init__(self):

		self.init_camera=rospy.init_node("Gimbal", anonymous=True)
		self.sub_camera=rosy.Subscriber("Xbox",Joy,self.callback) #receives Xbox commands by subscribing to Joy topic
		self.pub_camera= rospy.Publisher("Gimbal Camera", Frame, queue_size=20) #xbox publishes to the camera
		self.pan=0
		self.tilt=0
		self.ID = 600 # CAN id


	def callback(self):

		if joy.buttons[10]==1:
			self.tilt+=10

		if self.tilt >60:
			self.tilt = 60
	
		if self.tilt < -60:
			self.tilt = -60	

		if self.pan < -180:
			self.pan = -180	

		if self.pan > 180:
			self.pan=180

		elif joy.buttons[11]==1:
			self.tilt-=10	
		
		elif joy.buttons[12]==1:
			self.pan+=10

		elif joy.buttons[13]==1: 
			self.pan-=10

		self.sendAngle()


# Convert angles to CAN frame msg type
	def angleToFrame(self):
		frame = Frame()
		frame.ID = self._id
		frame.is_rtr = False
		frame.is_extended = False
		frame.is_error = False
		frame.dlc = 8
		data = bytearray(struct.pack('i', self.pan))
		data.extend(bytearray(struct.pack('i', self.tilt)))
		frame.data = str(data)
		return frame

	# Publish angles to SocketCAN
	def sendAngle(self):
		canFrame = self.angleToFrame()
		self.pub_camera.publish(canFrame)


if __name__ == '__main__':
	controller = GimbalController()
	rospy.spin()




		