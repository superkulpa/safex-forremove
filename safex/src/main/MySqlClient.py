import datetime
import mysql.connector as mdb
import logging

class CControlData:
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

data=CControlData()

def getValveH1():
  return data.mValveH

def getValveN1():
  return data.mValveN

def getMStop():
  return data.mStop
  
def getH1():
  return data.mSens1;

def getH2():
  return data.mSens2;

def getH3():
  return data.mSens3;

def connect():
  logging.debug( "mysql: connect")
  if(data.db is None):
    data.db = mdb.connect(host="localhost",port=3306,user="root",password='chemin',database='safex');
  #should do error checking here
  return data.db;

def createDataBase():
  logging.debug( "mysql: createDataBase")
  dummy = mdb.connect(host='localhost',user='root',password='chemin',port=3306);
  cur = dummy.cursor();
  cur.execute('DROP DATABASE safex');
  cur.execute('CREATE DATABASE safex');
  dummy.close();
  
  data.db = mdb.connect(host='localhost',user='root',password='chemin',port=3306,database='safex');
  cur = db.cursor();
  cur.execute("CREATE TABLE initialize(idnr INTEGER AUTO_INCREMENT PRIMARY KEY"\
	  ", time_stamp DATETIME"\
	  ", sens_1 BOOL NOT NULL DEFAULT 1, sens_2 BOOL NOT NULL DEFAULT 1, sens_3 BOOL NOT NULL DEFAULT 0"\
	  ", e_mail BOOL NOT NULL DEFAULT 0, c_shutdown BOOL NOT NULL DEFAULT 0, c_stop BOOL NOT NULL DEFAULT 0"\
	  ", valve_h BOOL NOT NULL DEFAULT 0, valve_n BOOL NOT NULL DEFAULT 0, save_h BOOL NOT NULL DEFAULT 1"\
	  ", emergency_stop BOOL DEFAULT 0"\
	  ");");
  res = push();
  if res != 0:
    return res;
  cur.execute("CREATE TABLE H_1(idnr INTEGER AUTO_INCREMENT PRIMARY KEY, time_stamp DATETIME"\
	  ", value INTEGER, temperature INTEGER);");
  res = addData_H1(0,0);
  if res != 0:
    return res;

  cur.execute("CREATE TABLE H_2(idnr INTEGER AUTO_INCREMENT PRIMARY KEY, time_stamp DATETIME"\
	  ", value INTEGER);");
  res = addData_H2(0);
  if res != 0:
    return res;

  cur.execute("CREATE TABLE H_3(idnr INTEGER AUTO_INCREMENT PRIMARY KEY, time_stamp DATETIME"\
	  ", value INTEGER);");
  res = addData_H3(0);
  if res != 0:
    return res;

  return 0;

def pull():
  logging.debug( "mysql: pull")	  
  cur = data.db.cursor();
  cur.execute("SELECT *"\
    "FROM initialize ORDER BY idnr DESC LIMIT 1;");
  row = cur.fetchone();
  newDateTime = row[1];
  if data.mTimeStamp < newDateTime:
    data.mTimeStamp = newDateTime;
    data.mSens1 = row[2];
    data.mSens2 = row[3];
    data.mSens3 = row[4];
    data.mEmail = row[5];
    data.mShutdown = row[6];
    data.mStop = row[7];
    data.mValveH = row[8];
    data.mValveN = row[9];
    data.mSaveH = row[10];
    data.eStop = row[11];
    print( "mysql: pull", row)	     
  return 0;

def push():
  logging.debug( "mysql: push")  
  cur = data.db.cursor();
  query = 'INSERT INTO initialize VALUES(NULL, NOW(),%r,%r,%r,%r,%r,%r,%r,%r,%r,%r);'\
    % (data.mSens1,data.mSens2,data.mSens3,data.mEmail,data.mShutdown,data.mStop,data.mValveH,data.mValveN,data.mSaveH,data.eStop);
  cur.execute(query);
  return 0;

def getData_H1():
  logging.debug( "mysql: getData_H1")
  cur = data.db.cursor();
  cur.execute('SELECT time_stamp, value FROM H_1 ORDER BY time_stamp DESC LIMIT 1;');
  row = cur.fetchone();
  return row[0], row[1];

def addData_H1(_value,_temperature):
  logging.debug( "mysql: addData_H1: %d, %d", _value, _temperature)  
  cur = data.db.cursor();
  query = 'INSERT INTO H_1 VALUES(NULL, NOW(), %d, %d);' % (_value, _temperature);
  cur.execute(query);
  return 0;

def getData_H2():
  logging.debug( "mysql: getData_H2")    
  cur = data.db.cursor();
  cur.execute('SELECT time_stamp, value FROM H_2 ORDER BY time_stamp DESC LIMIT 1;');
  row = cur.fetchone();
  return row[0], row[1];

def addData_H2(_value):
  logging.debug( "mysql: addData_H2: %d", _value)   
  cur = data.db.cursor();
  query = 'INSERT INTO H_2 VALUES(NULL, NOW(), %d);' % (_value);
  cur.execute(query);
  return 0;

def replaceData_H3(_value):
  logging.debug( "mysql: replaceData_H3")    
  cur = data.db.cursor();
  cur.execute('DELETE * FROM H_3 VALUES;');
  query = 'INSERT INTO H_3 VALUES(NULL, NOW(), %d)' % (_value);
  return 0;

def setEStop(_value):
  logging.debug( "mysql: setEStop %d", _value)  
  if(data.eStop != _value):
    data.eStop = _value;
    return push();
  return 0;

