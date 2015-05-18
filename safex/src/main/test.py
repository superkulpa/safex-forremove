import sys
import getopt
import logging
import datetime

class TestClass:
  mTimeStamp = datetime.datetime.now()
  flag=True

tc = TestClass()

def testDateTime():
  #global tc
  tc.flag=False
  print tc.mTimeStamp
  

try:
  logging.basicConfig(level=logging.DEBUG)
#filename='safex.log'
  print tc.flag
  testDateTime()
  print tc.flag
  
  
except BaseException, e:
  print "exception", e
 
