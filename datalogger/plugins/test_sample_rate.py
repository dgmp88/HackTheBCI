import sample_rate, time

sR = sample_rate.PluginSampleRate()
sR.activate()

while True:
	sR.__call__(0)
	time.sleep(2)
