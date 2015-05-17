import time
import logging
#from thread import start_new_thread

LED_PATH = '/sys/class/leds/beaglebone:green:usr0';
WD_Period = 0.2; 
ledTrigger = LED_PATH + '/trigger';
ledBrightness = LED_PATH + '/brightness';

import threading

        
class CWDRuner(threading.Thread):
  def __init__ (self):
      threading.Thread.__init__(self)
      self.loopFlag = True

  def run(self):
    self.removeTrigger();
    isOn = False;
    while self.loopFlag == True:
      fs = open(ledBrightness,'w');
      if isOn == True:
	fs.write('255');
      else:
	fs.write('0');
      fs.close();
      isOn = not isOn;
      time.sleep(WD_Period);

  def removeTrigger(self):
    fs = open(ledTrigger,'w');
    fs.write('none');
    fs.close();        
        
#class CWatchDog:
#  def __init__(self):

thr = CWDRuner()
  
def start():
  logging.debug( "wd: start")
  thr.start()
  return None;

def release():
  logging.debug( "wd: stop")
  thr.loopFlag = False;
  thr.join();
  return None;

loopFlag = True;
