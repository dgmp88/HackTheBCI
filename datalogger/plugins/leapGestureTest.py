import LeapLogger
import numpy as np

l = LeapLogger.Logger()

print l.dataPointsPerSample

data = np.zeros((l.dataPointsPerSample,1000))

lastData = None

while True:
	data = l.listener.return_frame()[-23:]
	
	if (lastData == None):
		lastData = data.copy()
		lastData.fill(1)

	if not np.all(lastData==data):
		print data
		
	lastData = data.copy()