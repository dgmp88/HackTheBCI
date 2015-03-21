import LeapLogger
import numpy as np

l = LeapLogger.Logger()

print l.dataPointsPerSample

data = np.zeros((l.dataPointsPerSample,1000))

while True:
	data[:,0] = l.listener.record_frame(data[:,0])
	print data[:,0]
