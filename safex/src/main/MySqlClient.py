import datetime
import mysql.connector as mdb
import logging

mTimeStamp = datetime.datetime.now();
mSens1 = True;
mSens2 = True;
mSens3 = False;
mEmail = False;
mShutdown = False;
mStop = False;
mValveH = False;
mValveN = False;
mSaveH = False;
eStop = False;
db = None

def getH1():
  return mSens1;

def getH2():
  return mSens2;

def getH3():
  return mSens3;

def connect():
  logging.debug( "mysql: connect")
  db = mdb.connect(host="localhost",port=3306,user="root",password='chemin',database='safex');
  print db
  #should do error checking here
  return 0;

def createDataBase():
  logging.debug( "mysql: createDataBase")
  dummy = mdb.connect(host='localhost',user='root',password='chemin',port=3306);
  cur = dummy.cursor();
  cur.execute('DROP DATABASE safex');
  cur.execute('CREATE DATABASE safex');
  dummy.close();
  db = mdb.connect(host='localhost',user='root',password='chemin',port=3306,database='safex');
  cur = db.cursor();
  cur.execute('"CREATE TABLE initialize(idnr INTEGER AUTO_INCREMENT PRIMARY KEY"\
	  ", time_stamp DATETIME"\
	  ", sens_1 BOOL NOT NULL DEFAULT 1, sens_2 BOOL NOT NULL DEFAULT 1, sens_3 BOOL NOT NULL DEFAULT 0"\
	  ", e_mail BOOL NOT NULL DEFAULT 0, c_shutdown BOOL NOT NULL DEFAULT 0, c_stop BOOL NOT NULL DEFAULT 0"\
	  ", valve_h BOOL NOT NULL DEFAULT 0, valve_n BOOL NOT NULL DEFAULT 0, save_h BOOL NOT NULL DEFAULT 1"\
	  ", emergency_stop BOOL DEFAULT 0"\
	  ");"');
  res = push();
  if res != 0:
	  return res;
  cur.execute('"CREATE TABLE H_1(idnr INTEGER AUTO_INCREMENT PRIMARY KEY, time_stamp DATETIME"\
	  ", value INTEGER, temperature INTEGER);"');
  res = addData_H1(0,0);
  if res != 0:
	  return res;

  cur.execute('"CREATE TABLE H_2(idnr INTEGER AUTO_INCREMENT PRIMARY KEY, time_stamp DATETIME"\
	  ", value INTEGER);"');
  res = addData_H2(0);
  if res != 0:
	  return res;

  cur.execute('"CREATE TABLE H_3(idnr INTEGER AUTO_INCREMENT PRIMARY KEY, time_stamp DATETIME"\
	  ", value INTEGER);"');
  res = addData_H3(0);
  if res != 0:
	  return res;

  return 0;

def pull():
  logging.debug( "mysql: pull", db)	  
  cur = db.cursor();
  cur.execute('"SELECT time_stamp, sens_1, sens_2, sens_3, e_mail, c_shutdown, c_stop, valve_h, valve_n, save_h, emergency_stop "\
	  "FROM initialize ORDER BY idnr DESC LIMIT 1;"');
  row = cur.fetchone();
  newDateTime = row[0];
  if mTimeStamp < newDateTime:
    mTimeStamp = newDateTime;
    mSens1 = row[1];
    mSens2 = row[2];
    mSens3 = row[3];
    mEmail = row[4];
    mShutdown = row[5];
    mStop = row[6];
    mValveH = row[7];
    mValveN = row[8];
    mSaveH = row[9];
    eStop = row[10];
  return 0;

def push():
  logging.debug( "mysql: push")  
  cur = db.cursor();
  query = 'INSERT INTO initialize VALUES(NULL, %s,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r);' % (mTimeStamp,mSens1,mSens2,mSens3,mEmail,mShutdown,mStop,mValveH,mValveN,mSaveH,eStop);
  cur.execute(query);
  return 0;

def getData_H1(_lastTime,_lastValue):
  logging.debug( "mysql: getData_H1", db)
  cur = db.cursor();
  cur.execute('SELECT time_stamp, value FROM H_1 ORDER BY time_stamp DESC LIMIT 1;');
  row = cur.fetchone();
  _lastTime = row[0];
  _lastValue = row[1];
  return 0;

def addData_H1(_value,_temperature):
  logging.debug( "mysql: addData_H1")  
  cur = db.cursor();
  query = 'INSERT INTO H_1 VALUES(NULL,%s,%d,%d);' % (mTimeStamp,_value,_temperature);
  cur.execute(query);

  return 0;

def getData_H2(_lastTime,_lastValue):
  logging.debug( "mysql: getData_H2")    
  cur = db.cursor();
  cur.execute('SELECT time_stamp, value FROM H_2 ORDER BY time_stamp DESC LIMIT 1;');
  row = cur.fetchone();
  _lastTime = row[0];
  _lastValue = row[1];

  return 0;

def addData_H2(_value):
  logging.debug( "mysql: addData_H2")   
  cur = db.cursor();
  query = 'INSERT INTO H_2 VALUES(NULL,%s,%d);' % (datetime.datetime.now(),_value);
  cur.execute(query);
 
  return 0;

def replaceData_H3(_value):
  logging.debug( "mysql: replaceData_H3")    
  cur = db.cursor();
  cur.execute('DELETE * FROM H_3 VALUES;');
  query = 'INSERT INTO H_3 VALUES(NULL,%s,%d)' % (datetime.datetime.now(),_value);

  return 0;

def setEStop(_value):
  logging.debug( "mysql: setEStop")  
  if(eStop != _value):
    eStop = _value;
    return push();
  return 0;

