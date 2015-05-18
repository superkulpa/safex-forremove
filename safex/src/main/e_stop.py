import Adafruit_BBIO.GPIO as GPIO
import MySqlClient as mysql
import logging

class CEmergencyStop:
  def __init__(self):
    logging.debug( "CEmergencyStop: init")	  
    self.pin_stop_value = 0;
    self.pin_stop = 'P8_26';
    GPIO.setup(self.pin_stop,GPIO.IN);

  def execute(self):
    logging.debug( "CEmergencyStop: execute")	      
    if GPIO.input(self.pin_stop) == False:
      if self.pin_stop_value == 1:
	mysql.setEStop(True);
	return 1;
      self.pin_stop_value = 1;
    else:
      self.pin_stop_value = 0;
    return 0;
