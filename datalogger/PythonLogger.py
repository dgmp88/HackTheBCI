#!/usr/bin/env python2.7
import argparse # new in Python2.7
import open_bci_v3 as bci
import os
import time
import string
import atexit
import threading

from yapsy.PluginManager import PluginManager

import logging
logging.basicConfig(level=logging.CRITICAL) # DEBUG for dev

# Load the plugins from the plugin directory.
manager = PluginManager()
manager.setPluginPlaces(["plugins"])
manager.collectPlugins()

if __name__ == '__main__':
# Namespace(add=None, baud=115200, daisy=False, filtering=True, info=None, list=False, port='/dev/tty.usbserial-DN00961I')

	class Args:
		pass
	args = Args()

	args.daisy = False
	args.filtering = True
	args.baud=115200
	args.port='/dev/tty.usbserial-DN00961I'
	args.list = False
	args.info = None
	args.add = None
	
	board = bci.OpenBCIBoard(port=args.port, daisy=args.daisy, filter_data=args.filtering)

	print board.getNbEEGChannels(), "EEG channels and", board.getNbAUXChannels(), "AUX channels at", board.getSampleRate(), "Hz."


	s = 'sv'
	# Tell the board to enable or not daisy module
	if board.daisy:
		s = s + 'C'
	else:
		s = s + 'c'
	# d: Channels settings back to default  
	s = s + 'd'

	while(s != "/exit"):
		#Send char and wait for registers to set
		if (not s): pass

		elif("help" in s): print "View command map at: \
http://docs.openbci.com/software/01-OpenBCI_SDK.\n\
For user interface: read README or view \
https://github.com/OpenBCI/OpenBCI_Python"

		elif board.streaming and s != "/stop":
			print "Error: the board is currently streaming data, please type '/stop' before issuing new commands."
		else:
		  	flush = False # read silently incoming packet if set (used when stream is stopped)
			if('/' == s[0]):
				s = s[1:]
				rec = False # current command is recognized or fot

				if("T:" in s):
					lapse = int(s[string.find(s,"T:")+2:])
					rec = True
				elif("t:" in s):
					lapse = int(s[string.find(s,"t:")+2:])
					rec = True
				else:
					lapse = -1

				if("start" in s): 
					if(fun != None):
						# start streaming in a separate thread so we could always send commands in here
						boardThread = threading.Thread(target=board.start_streaming, args=(fun, lapse))
						boardThread.daemon = True # will stop on exit
						boardThread.start()
					else:
						print "No function loaded"
					rec = True
				elif('test' in s):
					test = int(s[string.find(s,"test")+4:])
					board.test_signal(test)
					rec = True
				elif('stop' in s):
					board.stop()
					rec = True
					flush = True
				if rec == False:
					print("Command not recognized...")
				
			elif s:
				for c in s:
					board.ser.write(c)
					time.sleep(0.100)

			line = ''
			time.sleep(0.1) #Wait to see if the board has anything to report
			while board.ser.inWaiting():
				c = board.ser.read()
				line += c
				time.sleep(0.001)	
				if (c == '\n') and not flush:
					print('%\t'+line[:-1])
					line = ''
			if not flush:
				print(line)

		#Take user input
		s = raw_input('--> ');
