import csv_leap

x = csv_leap.PluginCSVLeap()
class Sample:
	pass
	
sample = Sample()
sample.id = 1
sample.channel_data =  10
sample.channel_data = [1,2,3,4]
sample.aux_data = [1,2,3,5]

for i in xrange(10): 
	x.__call__(sample)