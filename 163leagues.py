#!/usr/bin/python
# coding=utf-8

import io
import sys
import pymysql
import password

#连接配置信息
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

try:
	with connection.cursor() as cursor:
		sql = "INSERT INTO c17_leagues (name, id_163) VALUES ('英超',39)"
		cursor.execute(sql)
		sql = "INSERT INTO c17_leagues (name, id_163) VALUES ('意甲',51)"
		cursor.execute(sql)
		sql = "INSERT INTO c17_leagues (name, id_163) VALUES ('西甲',54)"
		cursor.execute(sql)
		sql = "INSERT INTO c17_leagues (name, id_163) VALUES ('德甲',49)"
		cursor.execute(sql)
		sql = "INSERT INTO c17_leagues (name, id_163) VALUES ('法甲',68)"
		cursor.execute(sql)
		sql = "INSERT INTO c17_leagues (name, id_163) VALUES ('欧冠',58)"
		cursor.execute(sql)
	connection.commit()
finally:
	connection.close();
