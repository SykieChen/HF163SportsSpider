#!/usr/bin/python
# coding=utf-8

import io
import sys
import pymysql

#连接配置信息
config = {
	'host':'sql.devchen.com',
	'port':3306,
	'user':'root',
	'password':'sykiechen1994',
	'db':'c17_new',
	'charset':'utf8',
	'cursorclass':pymysql.cursors.DictCursor,
}
connection1 = pymysql.connect(**config)
c1 = connection1.cursor()

config = {
	'host':'sql.devchen.com',
	'port':3306,
	'user':'root',
	'password':'sykiechen1994',
	'db':'ori',
	'charset':'utf8',
	'cursorclass':pymysql.cursors.DictCursor,
}
connection2 = pymysql.connect(**config)
c2 = connection1.cursor()
#遍历附表所有球队
sql = 'SELECT name FROM c17_teams'
c1.execute(sql)
teamR=c1.fetchall()
for teamX in teamR:
	teamN=teamX['name']
	sql = 'SELECT id FROM ori.teams WHERE abbr=%s'
	v=(teamN)
	c2.execute(sql, v)
	idR=c2.fetchall()
	if len(idR)!=0 :
		idN=idR[0]['id']
		sql = 'UPDATE c17_new.c17_teams SET id_main=%s WHERE name=%s'
		v=(int(idN), teamN)
		print(teamN, idN)
		try:
			c1.execute(sql,v)
			connection1.commit()
		except:
			print("Write Error.")
			sys.stdout.flush()
			connection1.rollback()
		
	else : print(teamN, 'pass')
	
	
c1.close()
c2.close()
connection1.close()
connection2.close()
