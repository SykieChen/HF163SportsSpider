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

#抓取
flgOption = False
flgTeam = False
teamId = 0
class htmlPar(HTMLParser):
	def handle_starttag(self, tag, attrs):
		global flgOption, flgTeam, teamId
		if tag == 'select':
			for name,value in attrs:
				if value=='teamOfficialId':
					flgTeam = True
		elif tag == 'option':
			if flgTeam == True:
				#print(attrs[0][1])
				if attrs[0][1] != "0":
					flgOption = True
					print (attrs[0][1])
					teamId = int(attrs[0][1])

	def handle_endtag(self, tag):
		global flgOption, flgTeam
		if tag=='select':
			flgTeam = False
		elif tag == 'option':
			flgOption = False

	def handle_data(self, data):
		global flgOption, teamId
		if flgOption == True:
			print (data)
			sys.stdout.flush()
			sql = "INSERT INTO c17_teams (name, id_163) VALUES (%s,%s)"
			v = (data,int(teamId))
			#print (sql,v)
			ctTry = 0
			try:
				c.execute(sql,v)
				connection.commit()
			except:
				print("Repeat record, ignore.")
				sys.stdout.flush()


for league in ['39','51','54','49','68','58']:
	htmlData = None
	htmlUrl = 'http://goal.sports.163.com/' + league + '/schedule.html'
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


c.close()
connection.close()
