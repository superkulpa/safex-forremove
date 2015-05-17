import time
from thread import start_new_thread

LED_PATH = '/sys/class/leds/beaglebone:green:usr0';
WD_Period = 1000*200;
ledTrigger = LED_PATH + '/trigger';
ledBrightness = LED_PATH + '/brightness';
instance = None;

def removeTrigger():
	fs = open(ledTrigger,'w');
	fs.write('none');
	fs.close();

class CWatchDog:

	def __init__(self):
		self.loopFlag = True;

	def run(self):
		removeTrigger();
		fs = open(ledBrightness,'w');
		isOn = False;
		if isOn == True:
			fs.write('255');
		else:
			fs.write('0');
		isOn = not isOn;
		time.sleep(WD_Period/1000000.0);
		while self.loopFlag == True:
			if isOn == True:
				fs.write('255');
			else:
				fs.write('0');
			isOn = not isOn;
			time.sleep(WD_Period/1000000.0);
		fs.close();

	def init(self):
		#if instance is None:
		instance = CWatchDog();
		start_new_thread(instance.run,());
		return instance;

	def release(self):
		self.loopFlag = False;
		return None;
