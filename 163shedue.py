#!/usr/bin/python
# coding=utf-8

import io
import sys
import pymysql
import urllib.parse
import urllib.request
import password
from html.parser import HTMLParser
#处理控制台乱码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')



#UA及Cookie数据
htmlUser_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36'
#htmlCookie = 'JSESSIONID=826307E3B24CA93E7B5CC69611E072C6; CNZZDATA1253891395=584384897-1439197399-http%253A%252F%252Fbjut.fifedu.com%252F%7C1448177798;'
htmlHeaders = {
	'User-Agent' : htmlUser_agent,
	#'cookie': htmlCookie
}



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

def dbwrite(mId163, mRound, mTime, mStatus, mHost, mGuest, mType):
	global mmCounter
	#查对应队伍ID
	sql = "SELECT id FROM c17_teams WHERE name = %s"
	v = (mHost)
	c.execute(sql,v)
	iHost=c.fetchall()
	sql = "SELECT id FROM c17_teams WHERE name = %s"
	v = (mGuest)
	c.execute(sql,v)
	iGuest=c.fetchall()
	print (mId163, mTime, mType, mRound, mStatus, mHost, iHost[0]['id'], mGuest, iGuest[0]['id'])
	sys.stdout.flush()

	sql = "INSERT INTO c17_matches (id_163, time, type, round, status, team_host, team_guest) VALUES (%s,%s,%s,%s,%s,%s,%s)"
	v = (mId163, mTime, mType, mRound, mStatus, iHost[0]['id'], iGuest[0]['id'])
	try:
		c.execute(sql,v)
		connection.commit()
		mmCounter=mmCounter+1
	except:
		print("Write Error.")
		sys.stdout.flush()
		connection.rollback()


#抓取
mmCounter=0

mId163=0
mType=1
mRound=0
mTime=""
mStatus=-1
mHost=""
mGuest=""
flgDiv=False
flgTr=False
flgTd=False
flgRA=False
flgA=False
ctTr=-2
ctTd=0
class htmlPar(HTMLParser):
	def handle_starttag(self, tag, attrs):
		global flgDiv, flgTr, flgRA, flgA, ctTr, ctTd, mId163, flgTd
		if tag == 'div':
			if attrs[0][1] == "leftList4":
				flgDiv=True
		elif tag=='tr':
			if flgDiv==True:
				ctTr=ctTr+1
				#print(ctTr)
				if ctTr%3==0:
					flgTr=True
					#print("flgTr=True")
					#ctTd=0
		elif tag=='td':
			if flgTr==True:
				flgTd=True
				#print("td++")
				ctTd=ctTd+1
				if ctTd==4 or ctTd==6: flgRA=True
		elif tag=='a':
			if flgRA==True: flgA=True
		elif tag=='span' and ctTd==8:
			mId163=int(attrs[1][1][6:-8])
		#if ctTd!=0:
		#	print(tag,"start")

	def handle_endtag(self, tag):
		global flgDiv, flgTr, flgRA, flgA, flgTd, ctTd
		if tag=='div':
			flgDiv=False
		elif tag == 'tr':
			flgTr=False
			#print("TrFalse")
		elif tag == 'a':
			flgA=False
		elif tag == 'td':
			flgRA=False
			flgTd=False
			if ctTd==8 and flgDiv==True:
				#print(mId163, mRound, mTime, mStatus, mHost, mGuest, mType)
				dbwrite(mId163, mRound, mTime, mStatus, mHost, mGuest, mType)
				ctTd=0
		#if ctTd!=0:
		#	print(tag,"end")
	def handle_data(self, data):
		global flgA, ctTd, mId163, mRound, mTime, mStatus, mHost, mGuest, flgTd
		if flgTd==True:
			if ctTd==1:
				mRound=data
				#print(data)
				#mRound=int(data)
			elif ctTd==2:
				mTime=data
			elif ctTd==3:
				if data=='完场': mStatus=2
				elif data=='未开赛': mStatus=0
				else: mStatus=1
			elif ctTd==4 and flgA==True: mHost=data
			elif ctTd==6 and flgA==True: mGuest=data
			#if ctTd!=0:
			#	print (ctTd)
			#	print ("rr")
			#	print (data)



#for league in ['58']:

for league in ['39','51','54','49','68','58']:

	mId163=0
	mType=1
	mRound=0
	mTime=""
	mStatus=-1
	mHost=""
	mGuest=""
	flgDiv=False
	flgTr=False
	flgTd=False
	flgRA=False
	flgA=False
	ctTr=-2
	ctTd=0
	sql = "SELECT id FROM c17_leagues WHERE id_163 = %s"
	v = (league)
	c.execute(sql,v)
	iType=c.fetchall()
	mType=iType[0]['id']
	htmlData = None
	htmlUrl = 'http://goal.sports.163.com/' + league + '/schedule/team/0_0_2015.html'
	htmlReq = urllib.request.Request(htmlUrl, htmlData, htmlHeaders)
	ctTry = 0
	while True:
		try:
			htmlResponse = urllib.request.urlopen(htmlReq, timeout = 3)
		except:
			if ctTry<4:
				ctTry += 1
				print('Error: getStatus. Retrying...', ctTry)
				sys.stdout.flush()
			else:
				print('Error: getStatus. Exiting...')
				sys.stdout.flush()
				sys.exit()
		else:
			break
	htmlOriPage = htmlResponse.read()
	htmlPage = htmlOriPage.decode("UTF8")
	#解析HTML
	iHtmlPar = htmlPar()
	iHtmlPar.feed(htmlPage)

print("Totla: ", mmCounter)
c.close()
connection.close()
