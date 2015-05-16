import sys
import getopt
import module_io
from module_init import CInit
from module_wd import CWatchDog
from MySqlClient import CMySqlClient
from heart_beat import CHeartBeat
from e_stop import CEmergencyStop
import Adafruit_BBIO.GPIO as GPIO
import time

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
			mysql = CMySqlClient.getInstance();
			mysql.createDataBase();
			return 1;
		elif opt == '-a':
			mysql = CMySqlClient.getInstance();
			mysql.connect('localhost');
			mysql.push();
			return 1;
		elif opt == '-h':
			print help_message;
			return -1;

	return 1;

res = parseOpts(sys.argv[1:]);
wd_o = CWatchDog();
wd_o.init();
init_o = CInit();
heart = CHeartBeat();
e_stop = CEmergencyStop();
while True:
	time.sleep(1);
	res = init_o.execute();
	if(res != 0):
		break;
	res = heart.execute();
	if(res != 0):
		break;
	res = e_stop.execute();
	if(res != 0):
		break;

wd_o.release();
