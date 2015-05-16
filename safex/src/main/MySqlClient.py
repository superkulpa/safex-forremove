import datetime
import mysql.connector as mdb

class CMySqlClient:

	instance = None;

	def __init__(self):
		self.mTimeStamp = datetime.datetime.now();
		self.mSens1 = True;
		self.mSens2 = True;
		self.mSens3 = False;
		self.mEmail = False;
		self.mShutdown = False;
		self.mStop = False;
		self.mValveH = False;
		self.mValveN = False;
		self.mSaveH = False;
		self.eStop = False;

	def getH1(self):
		return self.mSens1;

	def getH2(self):
		return self.mSens2;

	def getH3(self):
		return self.mSens3;

	def connect(self,_aHost,_aPort,_aUserName,_aPassword):
		self.db = mdb.connect(host=_aHost,port=_aPort,user=_aUserName,password='chemin',database='safex');
		#should do error checking here
		return 0;

	def createDataBase(self):
		dummy = mdb.connect(host='localhost',user='root',password='chemin',port=3306);
		cur = dummy.cursor();
		cur.execute('DROP DATABASE safex');
		cur.execute('CREATE DATABASE safex');
		dummy.close();
		self.db = mdb.connect(host='localhost',user='root',password='chemin',port=3306,database='safex');
		cur = self.db.cursor();
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

	def pull(self):
		cur = self.db.cursor();
		cur.execute('"SELECT time_stamp, sens_1, sens_2, sens_3, e_mail, c_shutdown, c_stop, valve_h, valve_n, save_h, emergency_stop "\
            		"FROM initialize ORDER BY idnr DESC LIMIT 1;"');
		row = cur.fetchone();
		newDateTime = row[0];
		if self.mTimeStamp < newDateTime:
			self.mTimeStamp = newDateTime;
			self.mSens1 = row[1];
			self.mSens2 = row[2];
			self.mSens3 = row[3];
			self.mEmail = row[4];
			self.mShutdown = row[5];
			self.mStop = row[6];
			self.mValveH = row[7];
			self.mValveN = row[8];
			self.mSaveH = row[9];
			self.eStop = row[10];
		return 0;

	def push(self):
		cur = self.db.cursor();
		query = 'INSERT INTO initialize VALUES(NULL, %s,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r);' % (mTimeStamp,mSens1,mSens2,mSens3,mEmail,mShutdown,mStop,mValveH,mValveN,mSaveH,eStop);
		cur.execute(query);
		return 0;

	def getData_H1(self,_lastTime,_lastValue):
		cur = self.db.cursor();
		cur.execute('SELECT time_stamp, value FROM H_1 ORDER BY time_stamp DESC LIMIT 1;');
		row = cur.fetchone();
		_lastTime = row[0];
		_lastValue = row[1];
		return 0;

	def addData_H1(self,_value,_temperature):
		cur = self.db.cursor();
		query = 'INSERT INTO H_1 VALUES(NULL,%s,%d,%d);' % (mTimeStamp,_value,_temperature);
		cur.execute(query);
		return 0;

	def getData_H2(self,_lastTime,_lastValue):
		cur = self.db.cursor();
		cur.execute('SELECT time_stamp, value FROM H_2 ORDER BY time_stamp DESC LIMIT 1;');
		row = cur.fetchone();
		_lastTime = row[0];
		_lastValue = row[1];
		return 0;

	def addData_H2(self,_value):
		cur = self.db.cursor();
		query = 'INSERT INTO H_2 VALUES(NULL,%s,%d);' % (datetime.datetime.now(),_value);
		cur.execute(query);
		return 0;

	def replaceData_H3(self,_value):
		cur = self.db.cursor();
		cur.execute('DELETE * FROM H_3 VALUES;');
		query = 'INSERT INTO H_3 VALUES(NULL,%s,%d)' % (datetime.datetime.now(),_value);
		return 0;

	def setEStop(self,_value):
		if(eStop != _value):
			eStop = _value;
			return push();
		return 0;

	@classmethod
	def getInstance(self):
		if instance is None:
			instance = CMySqlClient();
		return instance;

	def release(self):
		return None;
	