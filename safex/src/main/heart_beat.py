import Adafruit_BBIO.GPIO as GPIO
import MySqlClient as mysql
import datetime
import time
import logging

ADC_PATH = '/sys/bus/platform/devices/tiadc/iio:device0/';
adc4 = ADC_PATH + 'in_voltage4_raw';
adc5 = ADC_PATH + 'in_voltage5_raw';
adc6 = ADC_PATH + 'in_voltage6_raw';

class CHeartBeat:
  def __init__(self):
    logging.debug( "mysql: CHeartBeat")
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
    logging.debug( "mysql: processH1")
    value = (self.ain4 * (1+self.ain5))/100;
    lastTime, lastValue = mysql.getData_H1();
    difference = datetime.datetime.now() - lastTime;
    if(difference > datetime.timedelta(seconds=60) or self.checkRange(lastValue, value, 0.03) == False):
      mysql.addData_H1(value, self.ain5);
    return 0;

  def processH2(self):
    logging.debug( "mysql: processH2")
    lastTime,lastValue = mysql.getData_H2();
    difference = datetime.datetime.now() - lastTime;
    if(difference > datetime.timedelta(seconds=60) or self.checkRange(lastValue,self.ain6,0.03) == False):
      mysql.addData_H2(self.ain6);
    return 0;

  def processH3(self):
    logging.debug( "mysql: processH3")
    mysql.replaceData_H3(self.ain6);
    return 0;

  def execute(self):
    logging.debug( "mysql: execute")
    self.ain4 = float(self.fs_adc4.read());
    self.fs_adc4.seek(0);
    self.ain4 = self.ain4*1000/2275;
    self.ain5 = float(self.fs_adc5.read());
    self.fs_adc5.seek(0);
    self.ain5 = self.ain5*1000/2275;
    self.ain6 = float(self.fs_adc6.read());
    self.fs_adc6.seek(0);
    self.ain6 = self.ain6*1000/2275;
    
    if(self.ain4 > 1500):
      GPIO.output(self.pin_alert,GPIO.HIGH);
    elif self.ain6 > 1500:
      GPIO.output(self.pin_alert,GPIO.HIGH);
    else:
      GPIO.output(self.pin_alert,GPIO.LOW);

    if(mysql.getH1()):
      self.processH1();
    if(mysql.getH2()):
      self.processH2();
    if(mysql.getH3()):
      self.processH3();

    if(mysql.getMStop()):
      return 1;

    return 0;

