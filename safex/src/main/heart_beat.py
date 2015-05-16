import Adafruit_BBIO.GPIO as GPIO
from MySqlClient import CMySqlClient
import datetime
import time

ADC_PATH = '/sys/bus/platform/devices/tiadc/iio:device0/';
adc4 = ADC_PATH + 'in_voltage4_raw';
adc5 = ADC_PATH + 'in_voltage5_raw';
adc6 = ADC_PATH + 'in_voltage6_raw';

class CHeartBeat:
	def __init__(self):
		self.mysql = CMySqlClient.getInstance();
		self.fs_adc4 = open(adc4,'r');
		self.fs_adc5 = open(adc5,'r');
		self.fs_adc6 = open(adc6,'r');
		self.ain4 = 0;
		self.ain5 = 0;
		self.ain6 = 0;
		self.pin_alert = 'P9_22';
		GPIO.setup(self.pin_alert,GPIO.OUT);

	def checkRange(self,_base_v,equ_v,_percent):
		if _base_v == equ_v:
			return True;
		value_high = _base_v * (_percent + 1);
		value_low = _base_v * -(_percent + 1);
		if(equ_v > value_low or equ_v < value_high):
			return True;
		return False;

	def processH1(self):
		value = (self.ain4 * (1+self.ain5))/100;
		lastTime = 0;
		lastValue = 0;
		self.mysql.getData_H1(lastTime,lastValue);
		difference = datetime.datetime.now() - lastTime;
		if(difference > 60 or checkRange(lastValue,value,0.03) == False):
			mysql.addData_H1(value,self.ain5);
		return 0;

	def processH2(self):
		lastTime = 0;
		lastValue = 0;
		self.mysql.getData_H2(lastTime,lastValue);
		difference = datetime.datetime.now() - lastTime;
		if(difference > 60 or checkRange(lastValue,self.ain6,0.03) == False):
			mysql.addData_H2(self.ain6);
		return 0;

	def processH3(self):
		self.mysql.replaceData_H3(self.ain6);
		return 0;

	def execute(self):
		self.ain4 = self.fs_adc4.read();
		self.fs_adc4.seek(0);
		self.ain4 = self.ain4*1000/2275;
		self.ain5 = self.fs_adc5.read();
		self.fs_adc5.seek(0);
		self.ain5 = self.ain5*1000/2275;
		self.ain6 = self.fs_adc6.read();
		self.fs_adc6.seek(0);
		self.ain6 = self.ain6*1000/2275;
		
		if(self.ain4 > 1500):
			GPIO.output(pin_alert,GPIO.HIGH);
		elif ain6 > 1500:
			GPIO.output(pin_alert,GPIO.HIGH);
		else:
			GPIP.output(pin_alert,GPIO.LOW);

		if(mysql.getH1()):
			processH1();
		if(mysql.getH2()):
			processH2();
		if(mysql.getH3()):
			processH3();

		if(mysql.mStop):
			return 1;

		return 0;

