import pymysql
import time
import numpy as np
from sklearn import preprocessing
import sys



mysqlid='root'
mysqlkey='acer'
database='iscxbotnet'
database='freqmoear5'
mysqlurl='127.0.0.1'


#labelvalue=0
#startendlenmin=30
readmodel='model.pkl'

labelvalue=1
startendlenmin=30
startendlenmin=60
startendlenmin=120
startendlenmin=480
startendlenmin=1440
startendlenmin=2880

startendlenmin=int(sys.argv[1])

readmodel=''

#database='freqmoear5'
#projectname='moeaconn' #table=projectname , table_index=projectname_sip2dipstate
#path_iplist='/var/www/html/freqweb/freqmoear5/dip_unknow.csv'

database='iscxbotnet'
projectname='iscxp1testbyte'
path_iplist='/var/www/html/freqweb/iscx/nowhitelistip'

database='freqmoear6'
projectname='moeaconn' #table=projectname , table_index=projectname_sip2dipstate
path_iplist='/var/www/html/freqweb/freqmoear6/dip_unknow.csv'

database='freqmoear7'
projectname='conn' #table=projectname , table_index=projectname_sip2dipstate
path_iplist='/var/www/html/freqweb/freqmoear7/dip_unknow.csv'


path_iplist=''

##########################

def listreduce(times,listsumsbyte):
 #listsumsbyte - group by timeslot
 timeslot=times
 listtimeslot=list()
 listsumsbytenew=list()
 i=0
 for point in listsumsbyte:
  listtimeslot.append(point)
  i=i+1
  if i==timeslot:
    #print len(listtimeslot),listtimeslot
    nptimeslot=np.array(listtimeslot)
    nptimeslotsum=np.sum(nptimeslot)
    #print nptimeslotsum
    listsumsbytenew.append(nptimeslotsum)
    i=0
    listtimeslot=list()

 return listsumsbytenew

def createtable(tablename):
 sql='CREATE TABLE IF NOT EXISTS `'+tablename+'`(`point` int(20) NOT NULL) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'
 #sql='CREATE TABLE IF NOT EXISTS `'+tablename+'`(`time` datetime DEFAULT NULL, `point` int(20) NOT NULL) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'
 cursor.execute(sql)

def inserttotable(tablename,listname):
 cursor.execute('TRUNCATE '+tablename)
 for point in listname:
   sql="INSERT INTO `"+tablename+"` (`point`) VALUES ('"+str(point)+"')"
   cursor.execute(sql)

def createinserttable(tablename,listname):
  #createtable(tablename)
  #inserttotable(tablename,listname)
  return 1

def zerofillfromtable_copy(sql):
 beforet=0
 listsumsbyte=list()

 cursor.execute(sql)
 result = cursor.fetchall()
 for record in result:
   datetimestring=str(record[0]).strip()
   sumsbyte=record[1]
   try:
    nowt=time.mktime(time.strptime(datetimestring,'%Y-%m-%d %H:%M:%S'))
   except:
    nowt=time.mktime(time.strptime(datetimestring,'%Y-%b-%d_%H:%M:%S'))
    

   if beforet==0:
     beforet=nowt
   else:
     gap=int(nowt-beforet)
     if gap>1:
       for i in range(1,gap,+1):
         addt=beforet+i
         s=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(addt))
         #print s,0
         listsumsbyte.append(0)

   #print datetimestring,sumsbyte
   listsumsbyte.append(sumsbyte)
   beforet=nowt

 return listsumsbyte
 #print len(listsumsbyte)

def zerofillfromtable(sql,sip):
 beforet=0
 listsumsbyte=list()

 poweroffsec=0

 cursor.execute(sql)
 result = cursor.fetchall()
 for record in result:
   datetimestring=str(record[0]).strip()
   sumsbyte=record[1]
   try:
    nowt=time.mktime(time.strptime(datetimestring,'%Y-%m-%d %H:%M:%S'))
   except:
    nowt=time.mktime(time.strptime(datetimestring,'%Y-%b-%d_%H:%M:%S'))


   if beforet==0:
     beforet=nowt
     startt=nowt
   else:
     gap=int(nowt-beforet)
     if gap>1:
       for i in range(1,gap,+1):
         addt=beforet+i

         #checking if power on
         #s=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(addt))
         s=time.strftime('%Y-%m-%d %H:%M', time.localtime(addt))
         s=s[:-1]
         #print s
         if checksippoweron(s,sip):
           listsumsbyte.append(0)
         else:
           poweroffsec=poweroffsec+1
           #print 'power off',s

   #print datetimestring,sumsbyte
   listsumsbyte.append(sumsbyte)
   beforet=nowt

 print('time range:',startt,nowt,'=',int(nowt-startt))
 print('poweron len:',len(listsumsbyte))
 print('poweroff len:',poweroffsec)

 return listsumsbyte
 #print len(listsumsbyte)

def checksippoweron(s,sip):
  iptable='sip_'+sip.replace('.','_')
  sql='select * from '+iptable+' where hm10 ="'+s+'" limit 1'
  #print sql
  cursor.execute(sql)
  result = cursor.fetchone()
  if result:
    return 1
  else:
    return 0


class collectseg:
 def __init__(self):
   self.listsegall=list()

 def listcut_copy(self,range,listsumsbyteall):
  pic=range
  reductionrate=range/1800
  valuestart=0
  valueend=pic
  valuemax=len(listsumsbyteall)
  while valueend<=valuemax:
    #print valuestart,valueend
    listseg=listsumsbyteall[valuestart:valueend]
    npseg=np.array(listseg)
    valuesum=int(np.sum(npseg))
    print('total len:',valuemax,'start:',valuestart,'valuesum:',valuesum)
    if valuesum>0:
      listseg=self.reduction_pooling(listseg,reductionrate)
      listseg.append(self.label)
      self.listsegall.append(listseg)
    print('total listseg:',len(self.listsegall))
    valuestart=valueend
    valueend=valuestart+pic

 def listcut(self,npsegip):
   for listseg in npsegip:  
      self.listsegall.append(listseg)

 def iplistcut(self,range,listsumsbyteall):
  list0cut=0
  listsegip=list()
  pic=range
  reductionrate=int(range/1800)
  valuestart=0
  valueend=pic
  valuemax=len(listsumsbyteall)
  while valueend<=valuemax:
    #print valuestart,valueend,pic
    listseg=listsumsbyteall[valuestart:valueend]
    npseg=np.array(listseg)
    valuesum=np.sum(npseg)
    #print 'total len:',valuemax,'now:',valuestart,'valuesum:',valuesum
    if valuesum>0:
      #listseg.append(self.label)
      #self.listsegall.append(listseg)

      #min_max_scaler = preprocessing.MinMaxScaler()
      #listseg=self.reduction_pooling(listseg,reductionrate)
      #listseg = min_max_scaler.fit_transform(listseg)

      listseg=self.reduction_pooling(listseg,reductionrate)
      listseg=np.array(listseg)
      listseg=listseg.reshape(-1, 1)
      min_max_scaler = preprocessing.MinMaxScaler()
      listseg = min_max_scaler.fit_transform(listseg)
    else:
      listseg=self.reduction_pooling(listseg,reductionrate)
      listseg=np.array(listseg)
      listseg=listseg.reshape(-1, 1)
      list0cut=list0cut+1
    listseg=np.ravel(listseg)
    print('listseg len:',len(listseg))
    listsegip.append(listseg)
    valuestart=valueend
    valueend=valuestart+pic
  npsegip=np.array(listsegip)

  print('all seg:',len(listsegip))
  print('valuesum=0 seg',list0cut)

  return npsegip

 def iplistcut_copy(self,range,listsumsbyteall):
  listsegip=list()
  pic=range
  reductionrate=range/1800
  valuestart=0
  valueend=pic
  valuemax=len(listsumsbyteall)
  while valueend<=valuemax:
    #print valuestart,valueend
    listseg=listsumsbyteall[valuestart:valueend]
    npseg=np.array(listseg)
    valuesum=np.sum(npseg)
    #print 'total len:',valuemax,'now:',valuestart,'valuesum:',valuesum
    if valuesum>0:
      #listseg.append(self.label)
      #self.listsegall.append(listseg)

      min_max_scaler = preprocessing.MinMaxScaler()
      listseg=self.reduction_pooling(listseg,reductionrate)
      listseg = min_max_scaler.fit_transform(listseg)
      listsegip.append(listseg)
    valuestart=valueend
    valueend=valuestart+pic
  npsegip=np.array(listsegip)
  return npsegip



 def show(self):
  print(len(self.listsegall))

 def getnpdataset(self):
  dataset=np.array(self.listsegall)
  return dataset
 
 def reduction_pooling(self,listseg,reductionrate):
   newlistseg=list()
   n=reductionrate
   lenlistseg=int(len(listseg))
   for i in range(0,lenlistseg,+n):
     newlistseg.append( max(listseg[i:i+n]) )
   #print len(listseg)
   #print len(newlistseg)
   return newlistseg



    




#################################


#db = MySQLdb.connect(host=mysqlurl, user=mysqlid, passwd=mysqlkey, db=database)
db = pymysql.connect(host='localhost', port=3306, user='acer', passwd='acer', db='conndb', charset='utf8')
cursor = db.cursor()
cursor.execute('set names utf8')


#####################################################
#####################################################make dataset
#####################################################

picrange=1800
#picrange=18000
picrange=startendlenmin*60
cs=collectseg()

cs.label=labelvalue

#####################freqyes

#white dip
listanswer=list()
no_listanswer=0
if path_iplist!='':
  f=open(path_iplist)
  for line in f:
    listanswer.append(line.strip())
else:
  no_listanswer=1

listtable=list()

"""
###########################sip####################################################
sql='SELECT * FROM  `testipbadv2_ipstate` WHERE StartEndLenMin >30 and sbytesum>0'
#sql='SELECT * FROM  `testipgood_ipstate` WHERE StartEndLenMin >30 and sbytesum>0'
cursor.execute(sql)
result = cursor.fetchall()
for record in result:
  ip=record[0]
  iptable='p_hms'+ip.replace('.','_')
  listtable.append(iptable)

  sql="CREATE TABLE IF NOT EXISTS "+iptable+" AS \
   SELECT STR_TO_DATE(ts,'%Y-%M-%d_%H:%i:%s')AS hms1,SUM(  `orig_ip_bytes` ) AS sumsbyte FROM  `testipbad` WHERE  `id.orig_h` =  '"+ip+"' GROUP BY hms1"
  print sql
  cursor.execute(sql)
"""

##########################sip to dip#################################################
if labelvalue==0:
  datatable='testipgood'
else:
  datatable='testipbad'
datatable=projectname

datatype='sip2dipstate'
datatableindex=datatable+'_'+datatype
startendlensec=startendlenmin*60
print('read table index',datatableindex)

#create datatableindex
sql='create table if not exists '+datatableindex+' as SELECT sip,dip,MAX(timestamp) - MIN(timestamp)as timedistance ,sum(byte)as sumbyte FROM  `'+datatable+'`  GROUP BY `sip` ,`dip` '
cursor.execute(sql)

#sql='SELECT `id.orig_h`,`id.resp_h` FROM  `'+datatableindex+'` WHERE StartEndLenMin >30 and sbytesum>0'
#sql='SELECT `id.orig_h`,`id.resp_h` FROM   `'+datatableindex+'` WHERE StartEndLenMin >'+str(startendlenmin)+' and sbytesum>0'
sql=' SELECT sip,dip FROM  `'+datatableindex+'` WHERE (sip LIKE  "172.%" OR sip LIKE  "10.%" OR sip LIKE  "192.168.%" ) AND (dip not LIKE  "172.%" and dip not LIKE "10.%" and dip not LIKE  "192.168.%" ) AND timedistance > '+str(startendlensec)
sql=' SELECT sip,dip FROM  `'+datatableindex+'` WHERE timedistance >= '+str(startendlensec)+' and sumbyte!=0'
print(sql)

listsip=list()

cursor.execute(sql)
result = cursor.fetchall()
for record in result:
 ip=record[0].strip()
 dip=record[1].strip()
 if dip in listanswer or no_listanswer==1:

  iptable='p2_hms'+ip.replace('.','_')+'to'+dip.replace('.','_')
  listtable.append(iptable)

  #sql="DROP TABLE "+iptable
  #try:
  # cursor.execute(sql)
  #except:
  # 1

  sql="CREATE TABLE IF NOT EXISTS  "+iptable+" AS \
    SELECT FROM_UNIXTIME(trim(timestamp),'%Y-%m-%d %H:%i:%s')AS hms1,SUM(`byte`) AS sumsbyte FROM  `"+datatable+"` WHERE  `sip` =  '"+ip+"' and `dip` =  '"+dip+"'  GROUP BY hms1 "
  #SELECT STR_TO_DATE(ts,'%Y-%M-%d_%H:%i:%s')AS hms1,SUM(  `orig_ip_bytes` ) AS sumsbyte FROM  `"+datatable+"` WHERE  `id.orig_h` =  '"+ip+"' and `id.resp_h` =  '"+dip+"'  GROUP BY hms1"
  print(sql)
  cursor.execute(sql)

  listsip.append(ip)  


listsip= list(set(listsip))
for sip in listsip:
  iptable='sip_'+sip.replace('.','_')

  #sql="DROP TABLE "+iptable
  #cursor.execute(sql)
  
  sql="CREATE TABLE IF NOT EXISTS  "+iptable+" AS \
    SELECT SUBSTRING(FROM_UNIXTIME(TRIM(TIMESTAMP),'%Y-%m-%d %H:%i'),1,CHAR_LENGTH(FROM_UNIXTIME(TRIM(TIMESTAMP),'%Y-%m-%d %H:%i')) -1 ) AS hm10, SUM(`byte`) AS sumsbyte FROM  `"+datatable+"` WHERE  `sip` =  '"+sip+"'  GROUP BY hm10 "
  print(sql)
  cursor.execute(sql)


###
#listtable=['p_hms192_168_106_141']
#listtable=['p_hms158_65_110_241']
#listtable=['p2_hms172_16_2_113to209_85_135_104']
#listtable=['p2_hms158_65_110_2to224_0_0_9']
#listtable=['p2_hms10_1_2_100to172_31_1_76']
#listtable=['p2_hms172_31_1_16to127_0_0_1']
#listtable=['p2_hms172_31_1_199to210_61_248_234']
#listtable=['p2_hms172_31_1_199to210_61_248_234','p2_hms172_31_1_12to23_56_24_60']

print('listtable:',len(listtable))
finfo=open('data/unknown_'+datatableindex+str(startendlenmin)+'.info.csv','w')
datasavefile='data/unknown_'+datatableindex+str(startendlenmin)+'.csv'
fdata=open(datasavefile,'a')

dictiptraffic=dict()
for table in listtable:
 print(table)
 sql="select hms1,sumsbyte from "+table
 #tablenew='f0_'+table

 sip=table.split('t')[0].replace('p2_hms','')
 listsumsbyte=zerofillfromtable(sql,sip)
 npipseg=cs.iplistcut(picrange,listsumsbyte)

 dictiptraffic[table]=npipseg
 
 np.savetxt(fdata,npipseg, delimiter=',',fmt='%10.5f')

 print(len(npipseg)) 
 for i in range(0,len(npipseg), +1):
   finfo.write(table+'\n')

 #cs.listcut(npipseg)

#cs.show()

#datasavefile='unknown_'+datatableindex+str(startendlenmin)+'.csv'
#dataset=cs.getnpdataset()
#np.savetxt(datasavefile,dataset, delimiter=',',fmt='%10.5f')


if readmodel!='':
   print('#######################################################')
   print('################predict################################')
   print('#######################################################')
  
   datasavefile_predict='predict_'+datatableindex+str(startendlenmin)+'.csv'
   datasavefile_predictinfo='predict_'+datatableindex+str(startendlenmin)+'info.csv'
   f=open(datasavefile_predictinfo,'w')

   #ml analysis
   from sklearn.externals import joblib
   model = joblib.load(readmodel)

   if datatype=='sip2dipstate':
     f.write('sip,dip,timelen,freqrate,label\n')

   i=0
   for tablename,nptraffic in dictiptraffic.items():
      print(tablename,nptraffic.shape)
      #try:
      listresult=model.predict(nptraffic)
      timelen=len(listresult)
      freqlen=sum(listresult)
      freqrate=freqlen/timelen
      
      if 'p2_hms' in tablename:
        sipdip=tablename.replace('p2_hms','').replace('to',',').replace('_','.').split(',')
        sip=sipdip[0]
        dip=sipdip[1]
        data=sip+','+dip+','+str(timelen)+','+str(freqrate)+',0\n'
      if 'p_hms' in tablename:
        sip=tablename.replace('p_hms','').replace('_','.')
        data=sip+','+str(timelen)+','+str(freqrate)+'\n'
      f.write(data)

      ipnptrafficlabel=np.column_stack((nptraffic,listresult)) 
      #print ipnptrafficlabel.shape

      if i==0:
        nptrafficlabel=ipnptrafficlabel
      else:
        nptrafficlabel=np.row_stack((nptrafficlabel,ipnptrafficlabel))
      i=i+1

      #except:
      #print 'error'
   
   print('ready for writting file from numpy data:',nptrafficlabel.shape)
   np.savetxt(datasavefile_predict,nptrafficlabel, delimiter=',',fmt='%10.5f')


   exit()
   f=open('predictresult_badip')
   for line in f:
    listdata=line.strip().split(',')
    print(listdata)

