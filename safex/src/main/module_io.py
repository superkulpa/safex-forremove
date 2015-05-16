import re
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO

ADC.setup();

def prepareFor(_optarg):
	pin = -1;
	if _optarg is None:
		#log "invalid arg" error
		return -1;
	optarg = _optarg;
# 	regexp = "(AIN[0-8])|([P][9,8]_([0-3][0-9])|(4[0-6]))";
	if re.match(optarg):
		if optarg[0] == 'P':
			pin = optarg;
		elif optarg[0] == 'A':
			return -2;

	if pin == 0:
		#log "invalid arg" error
		return -1;
	return pin;

def readAnalog(optarg):
	ain = ADC.read(optarg);
	return ain;


def read_input(optarg):
	pin = prepareFor(optarg);
	if pin == -1:
		return -1;
	if pin == -2:
		return readAnalog(optarg);
	GPIO.setup(pin,GPIO.IN);
	return GPIO.input(pin);

def write_output(optarg,value):
	pin = prepareFor(optarg);
	if pin == -1:
		return -1;
	if value is None:
		#log "invalid arg" error
		return -1;
	GPIO.setup(pin,GPIO.OUT);
	GPIO.output(pin,value);
	return value;

