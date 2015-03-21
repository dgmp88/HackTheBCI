import csv
import timeit
import datetime
import numpy as np
import LeapLogger

# Usage: python user.py -p /dev/tty.usbserial-DN00961I --add csv_leap

import plugin_interface as plugintypes

class PluginCSVLeap(plugintypes.IPluginExtended):
	def __init__(self, delim = ",", verbose=False):
		now = datetime.datetime.now()
		self.time_stamp = '%d-%d-%d_%d-%d-%d'%(now.year,now.month,now.day,now.hour,now.minute,now.second)
		self.leap_file_name = 'leap_' + self.time_stamp + '.csv'
		self.bci_file_name = 'bci_' + self.time_stamp + '.csv'

		self.start_time = timeit.default_timer()
		self.delim = delim
		self.verbose = verbose
		self.leaplogger = LeapLogger.Logger()		

	def activate(self):
		pass
		
	def deactivate(self):
		print "Closing"
		return

	def show_help(self):
		print "---"
		
	def write_bci_sample(self, sample, t):
		row = ''
		row += str(t)
		row += self.delim
		row += str(sample.id)
		row += self.delim
		for i in sample.channel_data:
			row += str(i)
			row += self.delim
		for i in sample.aux_data:
			row += str(i)
			row += self.delim
		#remove last comma
		row = row[:-1]
		row += '\n'
		with open(self.bci_file_name, 'a') as f:
			f.write(row)
		
	def write_leap_sample(self,t):
		row = ''
		row += str(t)
		row += self.delim
		for i in self.leaplogger.listener.return_frame():
			row += str(i)
			row += self.delim

		#remove last comma
		row = row[:-1]
		row += '\n'
		with open(self.leap_file_name, 'a') as f:
			f.write(row)


	def __call__(self, sample):
		t = timeit.default_timer() - self.start_time
		self.write_bci_sample(sample,t)
		self.write_leap_sample(t)