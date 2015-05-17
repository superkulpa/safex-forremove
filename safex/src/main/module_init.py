import Adafruit_BBIO.GPIO as GPIO
from MySqlClient import CMySqlClient

class CInit:
	def __init__(self):
		self.pin_vH = 'P9_11';
		GPIO.setup(self.pin_vH,GPIO.OUT);
		GPIO.output(self.pin_vH,GPIO.LOW);

		self.pin_vN = 'P9_12';
		GPIO.setup(self.pin_vN,GPIO.OUT);
		GPIO.output(self.pin_vN,GPIO.LOW);

		self.pin_gc = 'P9_24';
		GPIO.setup(self.pin_gc,GPIO.OUT);
		GPIO.output(self.pin_gc,GPIO.LOW);

		mysql = CMySqlClient.getInstance();
		res = 0;
		if(mysql.isConnected() == False):
			res = mysql.connect('localhost');
			if(res != 0):
				return;
		res = mysql.push();
		if(res != 0):
			return;

	def __del__(self):
		GPIO.output(self.pin_vH,GPIO.LOW);
		GPIO.output(self.pin_vN,GPIO.LOW);
		GPIO.output(self.pin_gc,GPIO.HIGH);

	def execute(self):
		mysql = CMySqlClient.getInstance();
		GPIO.output(pin_vH,GPIO.HIGH if mysql.mValveH else GPIO.LOW);
		GPIO.output(pin_vN,GPIO.HIGH if mysql.mValveN else GPIO.LOW);
		return 0;

	