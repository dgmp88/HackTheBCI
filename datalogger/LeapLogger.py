################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.			   #
# Leap Motion proprietary and confidential. Not for distribution.			  #
# Use subject to the terms of the Leap Motion SDK Agreement available at	   #
# https://developer.leapmotion.com/sdk_agreement, or another agreement		 #
# between Leap Motion and you, your company or other organization.			 #
################################################################################

import Leap, sys, thread, time, math


class SampleGetter():
	finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
	state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
	def __init__(self, controller):
		self.controller = controller

	def record_frame(self):
		# Get the most recent frame and report some basic information
		frame = self.controller.frame()

		s1 = "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
			  frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

		# Get hands
		for hand in frame.hands:
			handType = "Left hand" if hand.is_left else "Right hand"

			s2 = "  %s, id %d, position: %s" % (
				handType, hand.id, hand.palm_position)

			# Get the hand's normal vector and direction
			normal = hand.palm_normal
			direction = hand.direction

			# Calculate the hand's pitch, roll, and yaw angles
			s3=  "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
				direction.pitch * Leap.RAD_TO_DEG,
				normal.roll * Leap.RAD_TO_DEG,
				direction.yaw * Leap.RAD_TO_DEG)

			# Get arm bone
			arm = hand.arm
			s4 = "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
				arm.direction,
				arm.wrist_position,
				arm.elbow_position)

			# Get fingers
			for finger in hand.fingers:

				s5 =  "	%s finger, id: %d, length: %fmm, width: %fmm" % (
					self.finger_names[finger.type()],
					finger.id,
					finger.length,
					finger.width)

				# Get bones
				for b in range(0, 4):
					bone = finger.bone(b)
					s6 = "	  Bone: %s, start: %s, end: %s, direction: %s" % (
						self.bone_names[bone.type],
						bone.prev_joint,
						bone.next_joint,
						bone.direction)

	def print_frame(self):
		# Get the most recent frame and report some basic information
		frame = self.controller.frame()

		print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
			  frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

		# Get hands
		for hand in frame.hands:
			handType = "Left hand" if hand.is_left else "Right hand"

			print "  %s, id %d, position: %s" % (
				handType, hand.id, hand.palm_position)

			# Get the hand's normal vector and direction
			normal = hand.palm_normal
			direction = hand.direction

			# Calculate the hand's pitch, roll, and yaw angles
			print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
				direction.pitch * Leap.RAD_TO_DEG,
				normal.roll * Leap.RAD_TO_DEG,
				direction.yaw * Leap.RAD_TO_DEG)

			# Get arm bone
			arm = hand.arm
			print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
				arm.direction,
				arm.wrist_position,
				arm.elbow_position)

			# Get fingers
			for finger in hand.fingers:

				print "	%s finger, id: %d, length: %fmm, width: %fmm" % (
					self.finger_names[finger.type()],
					finger.id,
					finger.length,
					finger.width)

				# Get bones
				for b in range(0, 4):
					bone = finger.bone(b)
					print "	  Bone: %s, start: %s, end: %s, direction: %s" % (
						self.bone_names[bone.type],
						bone.prev_joint,
						bone.next_joint,
						bone.direction)


def main():
	# Create a sample listener and controller
	controller = Leap.Controller()
	listener = SampleGetter(controller)
	startTime = time.time()
	s = 0
	i = 0

	# Keep this process running until Enter is pressed
	print "Press Enter to quit..."
	try:
		while True:
			listener.record_frame()
			i+=1
			#listener.print_frame()
			tSecs = math.floor(time.time()-startTime)
			if (tSecs > s):
				print '%i, %1.4f' % (tSecs, i/(time.time()-startTime))
				s = math.floor(time.time() - startTime)
				print i
			
			
	except KeyboardInterrupt:
		pass
	finally:
		pass

if __name__ == "__main__":
	main()
