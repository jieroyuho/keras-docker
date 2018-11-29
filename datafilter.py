import pymysql
import os
import sys

#filepath=sys.argv[1]


db = pymysql.connect(host='localhost', port=3306, user='acer', passwd='acer', db='conndb', charset='utf8')
cursor = db.cursor()
cursor.execute('set names utf8')
print('db connect finish')

sqlcmd='TRUNCATE conn'
cursor.execute(sqlcmd)
print(sqlcmd)

#cmd="grep  -vn '.*,.*,.*,10.|172.31.|172.16.|172.23.|172.24.|210.69.|224.|:' "+filepath+" | cut -d ':' -f 2 > conn.csv"
#os.system(cmd)
#print(cmd)

cmd="mysqlimport -u root --local --fields-terminated-by=, --password=acer conndb conn.csv" 
os.system(cmd)
print(cmd)


sqlcmd="create table ipstatus_dip as select dip,sum(byte)as sumbyte,count(distinct sip)as dtsip,count(*) as count from conn group by dip "
cursor.execute(sqlcmd)
print(sqlcmd)

sqlcmd="DELETE FROM `conn` WHERE dip in (SELECT dip FROM  `ipstatus_dip` WHERE count > ( SELECT AVG( count ) FROM  `ipstatus_dip` )) " 
cursor.execute(sqlcmd)
print(sqlcmd)

