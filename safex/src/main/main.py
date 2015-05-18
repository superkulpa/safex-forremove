import sys, os
import getopt
import module_io
from module_init import CInit
import module_wd as wd
import MySqlClient as mysql
from heart_beat import CHeartBeat

from e_stop import CEmergencyStop
import Adafruit_BBIO.GPIO as GPIO
import time
import logging
import traceback


help_message = 'the safex:\n\
    -i : io mode, read input data from GPIOs, AIN, ex: -i P8_12, -i AIN0\n\
    -o : io mode, write ouput data to GPIOsex: -o P8_12 1, write value 1 to port P8_12\n';

def parseOpts(argv):
  opts, args = getopt.getopt(argv,'act:i:o:h');
  for opt, arg in opts:
    if opt == '-i':
      print module_io.read_input(arg);
      return 1;
    elif opt == '-o':
      print module_io.write_output(arg, GPIO.HIGH);
      return 1;
    elif opt == '-c':
      mysql.createDataBase();
      return 1;
    elif opt == '-a':
      mysql.connect();
      mysql.push();
      return 1;
    elif opt == '-h':
      print help_message;
      return -1;

  return 1;

try:
  logging.basicConfig(level=logging.DEBUG)
#filename='safex.log'

  res = parseOpts(sys.argv[1:]);
  lifecycles=0
  res = mysql.connect();
  if (res is None):
    print "Can't connect to sql, exit"
    raise BaseException
  
  wd.start();
  init_o = CInit();
  heart = CHeartBeat();
  e_stop = CEmergencyStop();
  
  while True:
    res = init_o.execute();
    if(res != 0):
      break;
    res = heart.execute();
    if(res != 0):
      break;
    res = e_stop.execute();
    if(res != 0):
      break;
    #limit lifecycles
    lifecycles += 1
    if lifecycles>30:
      break
    time.sleep(1);
    
except BaseException as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(e, exc_type, fname, exc_tb.tb_lineno)
 
wd.release();
#  traceback.print_stack()