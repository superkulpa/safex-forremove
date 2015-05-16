import Adafruit_BBIO.GPIO as GPIO
from MySqlClient import CMySqlClient

class CEmergencyStop:
	def __init__(self):
		self.mysql = CMySqlClient.getInstance();
		self.pin_stop = 'P8_26';
		GPIO.setup(self.pin_stop,GPIO.IN);
		self.pin_stop_value = 0;

	def execute(self):
		if GPIO.input(pin_stop):
			if pin_stop_value == 1:
				mysql.setEStop(True);
				return 1;
			pin_stop_value = 1;
		else:
			pin_stop_value = 0;
		return 0;
