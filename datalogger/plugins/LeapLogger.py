################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.			   #
# Leap Motion proprietary and confidential. Not for distribution.			  #
# Use subject to the terms of the Leap Motion SDK Agreement available at	   #
# https://developer.leapmotion.com/sdk_agreement, or another agreement		 #
# between Leap Motion and you, your company or other organization.			 #
################################################################################

import Leap, sys, thread, time, math
import numpy as np
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


gestureDataPoints = 23

metaData = 5
dataPointsPerFinger = 18
handOnlyDataPoints = 16
dataPointsPerHand = handOnlyDataPoints + dataPointsPerFinger * 5
dataPointsPerSample = metaData + dataPointsPerHand * 2 + gestureDataPoints
array =np.zeros((dataPointsPerSample))
gests = np.zeros((gestureDataPoints))

class SampleGetter():
	finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
	state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
	def __init__(self, controller):
		self.controller = controller
		self.controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
		self.controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
		self.controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
		self.controller.enable_gesture(Leap.Gesture.TYPE_SWIPE )
		
	def return_gestures(self):
		controller = self.controller
		frame = controller.frame()
		gests.fill(0)
		for gesture in frame.gestures():
			if gesture.type == Leap.Gesture.TYPE_CIRCLE:
				circle = CircleGesture(gesture)
				gests[0] = 1

				# Determine clock direction using the angle between the pointable and the circle normal
				if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
					gests[1] = 1 # clockwise or counterclockwise

				# Calculate the angle swept since the last frame
				swept_angle = 0
				if circle.state != Leap.Gesture.STATE_START:
					previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
					gests[2] =  (circle.progress - previous_update.progress) * 2 * Leap.PI
					
				gests[3] = circle.progress
				gests[4] = circle.radius

			if gesture.type == Leap.Gesture.TYPE_SWIPE:
				swipe = SwipeGesture(gesture)
				gests[5] = swipe.position.x
				gests[6] = swipe.position.y
				gests[7] = swipe.position.z
				
				gests[8] = swipe.direction.x
				gests[9] = swipe.direction.y
				gests[10] = swipe.direction.z

			if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
				keytap = KeyTapGesture(gesture)
				gests[11] = keytap.position.x
				gests[12] = keytap.position.y
				gests[13] = keytap.position.z
				
				gests[14] = keytap.direction.x
				gests[15] = keytap.direction.y
				gests[16] = keytap.direction.z
			if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
				screentap = ScreenTapGesture(gesture)
				gests[17] = screentap.position.x
				gests[18] = screentap.position.y
				gests[19] = screentap.position.z
				
				gests[20] = screentap.direction.x
				gests[21] = screentap.direction.y
				gests[22] = screentap.direction.z		
		return gests
	def return_frame(self):
		# Get the most recent frame and report some basic information
		frame = self.controller.frame()
		array.fill(0) # Reset the data array
		## Meta data
		array[0] = frame.id
		array[1] = frame.timestamp
		array[2] = len(frame.hands)
		array[3] = len(frame.fingers)
		array[4] = len(frame.tools)
		for hand in frame.hands:
			# Left or right hand?
			hP = metaData if hand.is_left else dataPointsPerHand + metaData
			
			# Not sure what this is
			array[hP] = hand.id 
			
			# Palm position
			array[hP+1] = hand.palm_position[0]
			array[hP+2] = hand.palm_position[1]
			array[hP+3] = hand.palm_position[2]

			# Hand pitch/roll/yaw
			array[hP+4] = hand.direction.pitch * Leap.RAD_TO_DEG
			array[hP+5] = hand.palm_normal.roll * Leap.RAD_TO_DEG
			array[hP+6] = hand.direction.yaw * Leap.RAD_TO_DEG

			# Get arm bone
			arm = hand.arm
			array[hP+7] = arm.direction.x
			array[hP+8] = arm.direction.y
			array[hP+9] = arm.direction.z
			
			array[hP+10] = arm.wrist_position.x
			array[hP+11] = arm.wrist_position.y
			array[hP+12] = arm.wrist_position.z
			
			array[hP+13] = arm.elbow_position.x
			array[hP+14] = arm.elbow_position.y
			array[hP+15] = arm.elbow_position.z

			# Get fingers # Does a hand always have 5 fingers? Lets hope so!
			fN = 0;
			for finger in hand.fingers:
				fP = hP + handOnlyDataPoints + (fN*dataPointsPerFinger)
				fN += 1
				array[fP] = finger.id
				array[fP+1] = finger.length
				array[fP+2] = finger.width
				array[fP+3] = finger.tip_position.x
				array[fP+4] = finger.tip_position.y
				array[fP+5] = finger.tip_position.z
				# Get bones
				for b in range(0, 4):
					bone = finger.bone(b)
					bP = fP + 6 + b * 3
					array[bP] = bone.center.x
					array[bP] = bone.center.y
					array[bP] = bone.center.z
					
		array[-gestureDataPoints:] = self.return_gestures()
		return array

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


class Logger():
	def __init__(self):
			self.controller = Leap.Controller()
			self.listener = SampleGetter(self.controller)
			self.dataPointsPerSample = dataPointsPerSample