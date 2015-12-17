# coding=utf-8
import io
import sys
import urllib.parse
import urllib.request
#import json
from html.parser import HTMLParser

#抓取比赛状态比分
def cStatus(cID):
	flgStatusSpan = False
	flgScoreSpan = False
	retStatus = -1
	scoreA = 0
	scoreB = 0
	class htmlPar(HTMLParser):
		def handle_starttag(self, tag, attrs):
			nonlocal flgStatusSpan, flgScoreSpan
			if tag == 'span':
				for name,value in attrs:
					if value=='c_mathstat':
						flgStatusSpan = True
					elif value=='c_score':
						flgScoreSpan = True
						
		def handle_endtag(self, tag):
			nonlocal flgStatusSpan, flgScoreSpan
			if tag=='span':
				flgStatusSpan = False
				flgScoreSpan = False
		
		def handle_data(self, data):
			nonlocal flgStatusSpan, flgScoreSpan, retStatus, scoreA, scoreB
			if flgStatusSpan == True:
				#print (data[18:20])
				if data[18:20] == '完场':
					retStatus = 1
				else:
					retStatus = 0
			elif flgScoreSpan == True:
				if retStatus == 1:
					#print(data[1:2])
					scoreA = int(data[1:2])
					scoreB = int(data[3:4])
				
	
	htmlData = None
	htmlUrl = 'http://goal.sports.163.com/39/match/stat/2015/' + cID + '.html'
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
	return retStatus, scoreA, scoreB

	
	
#处理控制台乱码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')



#UA及Cookie数据
htmlUser_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36'
htmlCookie = 'JSESSIONID=826307E3B24CA93E7B5CC69611E072C6; CNZZDATA1253891395=584384897-1439197399-http%253A%252F%252Fbjut.fifedu.com%252F%7C1448177798;'
htmlHeaders = {
	'User-Agent' : htmlUser_agent,
	'cookie': htmlCookie
}

print(cStatus('1546923'))
print(cStatus('1574857'))
	
