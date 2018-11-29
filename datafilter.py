import pymysql
import os
import sys

#filepath=sys.argv[1]


db = pymysql.connect(host='localhost', port=3306, user='acer', passwd='acer', db='conndb', charset='utf8')
cursor = db.cursor()
cursor.execute('set names utf8')
print('db connect finish')

sqlcmd="DELETE FROM `conn` WHERE  sip NOT LIKE  '10.%' AND sip NOT LIKE  '192.168.%' AND sip NOT LIKE  '172.%' "
cursor.execute(sqlcmd)
print(sqlcmd)

sqlcmd=" CREATE TABLE conn_copy LIKE conn"
cursor.execute(sqlcmd)
print(sqlcmd)
sqlcmd=" INSERT conn_copy SELECT * FROM conn"
cursor.execute(sqlcmd)
print(sqlcmd)

sqlcmd="create table ipstatus_dip as select dip,sum(byte)as sumbyte,count(distinct sip)as dtsip,count(*) as count from conn group by dip "
cursor.execute(sqlcmd)
print(sqlcmd)

sqlcmd="DELETE FROM `conn` WHERE dip in (SELECT dip FROM  `ipstatus_dip` WHERE count > ( SELECT AVG( count ) FROM  `ipstatus_dip` )) " 
cursor.execute(sqlcmd)
print(sqlcmd)

