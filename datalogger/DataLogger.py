import h5py, time, datetime

import numpy as np

import LeapLogger
dataFileName = str(datetime.datetime.now()) + '.h5'
file = h5py.File(dataFileName,'w')


## Decide on our sampling rate, calculate some useful stuff
logTime = 5.0/60.0 # in minutes
sampleRateHz = 250.0 # in Hz
oneSampleTime = 1.0/sampleRateHz

## Total number of samples
totalSamples = logTime * 60.0 * sampleRateHz


## Get our data recording objects 
leap = LeapLogger.Logger()

leapData = np.zeros((leap.dataPointsPerSample,totalSamples))


def recordSample(sample):
	leapData[:,sample] = leap.listener.record_frame(leapData[:,sample])

currentSample = 0
nextSampleTime = 0

startTime = time.time()
timeOfLastSample = 0 # Collect a sample right away


# Our loop! Record data here
while (currentSample < totalSamples):
	timeSinceLastSample = time.time() - timeOfLastSample
	if (timeSinceLastSample > oneSampleTime):
		recordSample(currentSample)
		timeOfLastSample = time.time()
		currentSample += 1		

file.create_dataset('leap',data = leapData)

file.close()


np.savetxt("foo.csv", leapData, delimiter=",")