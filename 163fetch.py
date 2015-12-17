#!/usr/bin/python34
# coding=utf-8
import io
import sys
#import urllib.parse
#import urllib.request
import xml.sax
import pymysql
import time
import password

#连接数据库
config = {
	'host':'localhost',
	'port':3306,
	'user':password.dbUsr,
	'password':password.dbPass,
	'db':'sports',
	'charset':'utf8',
	'cursorclass':pymysql.cursors.DictCursor,
}
connection = pymysql.connect(**config)
c = connection.cursor()

def dbWrite(cID, mHost, mGuest):
	print("[INFO] Updating sub DB...",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
	sql = "UPDATE c17_matches SET status=2, score_host=%s, score_guest=%s WHERE id_163=%s"
	v = (mHost, mGuest, cID)
	try:
		c.execute(sql,v)
		connection.commit()
		print("[INFO] Success.")
	except:
		print("[ERRO] Write Error.")
		sys.stdout.flush()
		connection.rollback()
	return

def findMain(tHost, tGuest, mTime, sHost, sGuest):
	print("[INFO] Updating main DB...", sHost, sGuest, mTime, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
	sql = "SELECT id_main FROM c17_teams WHERE id=%s"
	v = (tHost)
	c.execute(sql,v)
	cHost = c.fetchall()
	mainHost = cHost[0]['id_main']

	sql = "SELECT id_main FROM c17_teams WHERE id=%s"
	v = (tGuest)
	c.execute(sql,v)
	cGuest = c.fetchall()
	mainGuest = cGuest[0]['id_main']
	if mainHost == None :
		print("[WARN] Not found in main DB: ", sHost, sGuest, mainHost, mainGuest, mTime)
		return
	sql = "UPDATE matches SET home_curt_score=%s, away_curt_score=%s, status='after', updated_at=NOW() WHERE home_curt_id=%s AND away_curt_id=%s AND begin_time=%s"
	v = (sHost, sGuest, mainHost, mainGuest, mTime)
	#print(sql % v)

	try:
		c.execute(sql,v)
		connection.commit()
		print("[INFO] Success.")
	except:
		print("[ERRO] Write Error.")
		sys.stdout.flush()
		connection.rollback()

	return




#抓网易比赛结果
def cResult(cType, cID):
	mStatus = 0
	mHost = 0
	mGuest = 0
	class cPar(xml.sax.ContentHandler) :
		def startElement(self, tag, attributes):
			nonlocal mStatus , mHost , mGuest
			if tag == "Result":
				#print ("Status: ", attributes["matchPeriod"])
				if attributes["matchPeriod"] == '完场': mStatus = 2
			elif tag == "Team":
				if attributes["side"] == "1":
					#print ("**********Host Team**********")
					#print ("Name: ", attributes["team"])
					#print ("Score: ", attributes["score"])
					mHost = int(attributes["score"])
				else:
					#print ("**********Guest Team**********")
					#print ("Name: ", attributes["team"])
					#print ("Score: ", attributes["score"])
					mGuest = int(attributes["score"])

			'''
			elif tag == "Stat":
				print ("Goal:")
				print ("\tPeriod: ", attributes["period"])
				print ("\tTime: ", attributes["time"])
				print ("\tPlayer: ", attributes["player"])
				print ("\tPosition: ", attributes["position"])
				print ("\tType: ", attributes["type"])
			elif tag== "Card":
				print ("Card:")
				print ("\tColor: ", attributes["cardType"])
				print ("\tPeriod: ", attributes["period"])
				print ("\tTime: ", attributes["time"])
				print ("\tPlayer: ", attributes["player"])
				print ("\tReason: ", attributes["Reason"])
			elif tag=="Substitution":
				print ("Substitution:")
				print ("\tPeriod: ", attributes["period"])
				print ("\tTime: ", attributes["time"])
				print ("\tPosition: ", attributes["substitutePosition"])
				print ("\tOff: ", attributes["subOffName"])
				print ("\tOn: ", attributes["subOnName"])
			'''

	parser = xml.sax.make_parser()
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)
	Handler = cPar()
	parser.setContentHandler(Handler)
	url = "http://goal.sports.163.com/" + str(cType) + "/match/general/2015/" + str(cID) + ".xml"

	'''
	if cType == '39':
		chType = "英超"
	elif cType == '51':
		chType = "意甲"
	elif cType == '54':
		chType = "西甲"
	elif cType == '49':
		chType = "德甲"
	elif cType == '68':
		chType = "法甲"
	elif cType == '58':
		chType = "欧冠"
	else:
		print ('Unknown Type!')
		return
	print ("*****************", chType, "*******************")
	'''
	parser.parse(url)
	return mStatus, mHost, mGuest


#处理控制台乱码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')


#轮询数据库所有
sql = 'SELECT id_163, type, time, team_host, team_guest FROM c17_matches WHERE status!=2 AND DATE(NOW())-DATE(time)>=0'
#sql = 'SELECT id_163, type, time, team_host, team_guest FROM c17_matches WHERE
#round=1 AND type=1'
c.execute(sql)
idR = c.fetchall()
for idX in idR:
	cID = int(idX['id_163'])
	mType = int(idX['type'])
	sql = "SELECT id_163 FROM c17_leagues WHERE id = %s"
	v = (mType)
	c.execute(sql,v)
	rType = c.fetchall()
	cType = int(rType[0]['id_163'])
	mStatus, mHost, mGuest = cResult(cType,cID)
	#print("[QERY] ", cType,cID,mStatus, mHost, mGuest, idX['time'])
	sys.stdout.flush()
	if mStatus == 2 :
		dbWrite(cID, mHost, mGuest)
		#print (idX['team_host'], idX['team_guest'], idX['time'], mHost, mGuest)
		findMain(idX['team_host'], idX['team_guest'], idX['time'], mHost, mGuest)







c.close()
connection.close()
#print("*Loop Finished* ", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
