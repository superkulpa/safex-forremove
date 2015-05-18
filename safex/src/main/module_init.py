import Adafruit_BBIO.GPIO as GPIO
import MySqlClient as mysql
import logging

class CInit:
  def __init__(self):
    logging.debug( "CInit: init")
    self.pin_vH = 'P9_11';
    GPIO.setup(self.pin_vH,GPIO.OUT);
    GPIO.output(self.pin_vH,GPIO.LOW);

    self.pin_vN = 'P9_12';
    GPIO.setup(self.pin_vN,GPIO.OUT);
    GPIO.output(self.pin_vN,GPIO.LOW);

    self.pin_gc = 'P9_24';
    GPIO.setup(self.pin_gc,GPIO.OUT);
    GPIO.output(self.pin_gc,GPIO.LOW);

    res = mysql.push();
    if(res != 0):
      return;

  def __del__(self):
    logging.debug( "CInit: del")
    GPIO.output(self.pin_vH,GPIO.LOW);
    GPIO.output(self.pin_vN,GPIO.LOW);
    GPIO.output(self.pin_gc,GPIO.HIGH);
    

  def execute(self):
    logging.debug( "CInit: execute")
    #pull data from mysql server, programm read last data, that has been written
    mysql.pull()

    GPIO.output(self.pin_vH, GPIO.HIGH if mysql.getValveH1() else GPIO.LOW);
    GPIO.output(self.pin_vN, GPIO.HIGH if mysql.getValveN1() else GPIO.LOW);
    return 0;

	