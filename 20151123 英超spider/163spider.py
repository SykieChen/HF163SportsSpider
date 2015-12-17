#!/usr/bin/python

# coding=utf-8
import io
import sys
#import urllib.parse
#import urllib.request
import xml.sax

#抓网易比赛结果
#测试版，直接输出
def cResult(cType, cID):
	class cPar(xml.sax.ContentHandler) :
		def startElement(self, tag, attributes):
			if tag == "Result":
				print ("Status: ", attributes["matchPeriod"])
			elif tag == "Team":
				if attributes["side"]=="1":
					print ("**********Host Team**********")
					print ("Name: ", attributes["team"])
					print ("Score: ", attributes["score"])
				else:
					print ("**********Guest Team**********")
					print ("Name: ", attributes["team"])
					print ("Score: ", attributes["score"])
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
			
			
	parser = xml.sax.make_parser()
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)
	Handler = cPar()
	parser.setContentHandler(Handler)
	url = "http://goal.sports.163.com/" + cType + "/match/general/2015/" + cID + ".xml"

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
	parser.parse(url)


#处理控制台乱码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')


cResult('39','1547079')
#cResult('58','1574857')
#cResult('51','1568952')
			