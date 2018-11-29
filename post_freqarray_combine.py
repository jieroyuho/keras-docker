import sys
import os 


#listanswer=list()
#f=open('/var/www/html/freqweb/freqmoear5/dip_unknow.csv')
#for line in f:
#  listanswer.append(line.strip())

#print listanswer
listdip=list()

type=sys.argv[1]
dirname=sys.argv[2]

dictsip2dip=dict()

#listfileid=['30','60','120','240','480','1440','2880','5760']
#listfileid=['1440','2880','5760']
#listfileid=['5760','2880','1440','480','240','120','60','30']

if type=='f':
  listfileid=['30','60','120','240','480']
  listfileid=['30','60']
if type=='c':
  listfileid=['1440','2880','5760','10080','20160']
if type=='a': 
  listfileid=['30','60','120','240','480','1440','2880','5760','10080','20160']
  listfileid=['120','240','480','1440','2880','5760','10080','20160']

#for files in os.listdir(dirname):
for fileid in listfileid:
  files='freqarray'+fileid+'.csv'
  filepath=dirname+files
  timesize=files.replace('freqarray','').replace('.csv','')
  #print timesize
  farray=open(filepath)
  for line in farray:
    listdata=line.strip().split(',')
    dip=listdata[1].strip()
    listdip.append(dip)
    #if dip in listanswer:
    sip2dip=listdata[0]+','+listdata[1]
    listdata=listdata[2:]
    listdata.append(timesize)

    if dictsip2dip.get(sip2dip)== None:
      dictsip2dip[sip2dip]=list()
      dictsip2dip[sip2dip].append(listdata) 
    else:
      dictsip2dip[sip2dip].append(listdata)


#listdip=list(set(listdip))
#print list(set(listdip) & set(listanswer))


dictfreqarray=dict()
listtimerange=list()
for key,data in dictsip2dip.items():
  #print key,data

  maxbef=''
  for listline in data:
    #print listline[0],listline[2]
    if maxbef=='':
      maxvalue=float(listline[0])
      maxdata=listline
    else:
      if float(listline[0])>maxbef:
        maxvalue=float(listline[0]) 
        maxdata=listline
    maxbef=maxvalue    
  #print maxbef,maxdata[2]
  #exit() 
  
  timerange=int(maxdata[1])*int(maxdata[2])/60
  listtimerange.append(timerange)  
  
  dictfreqarray[key]=[maxdata[0],maxdata[1],maxdata[2],timerange]
  #print key,',',maxdata[0],',',maxdata[1],',',maxdata[2],timerange


#######################################level maker 

maxhour=max(listtimerange)
hourl1=maxhour/3
hourl2=hourl1*2

for key,data in dictfreqarray.items():
   #print key,data
   timerange=float(data[3])
   freqrate=float(data[0])
   timesize=data[2]
   
   if freqrate>0.67 and timerange>hourl2:
      level=1
      #print key,',',level,',',freqrate,',',timerange

   if freqrate>0.67 and timerange>hourl1 and timerange<=hourl2:
      level=2
   if timerange>hourl2 and freqrate>0.34 and freqrate<=0.67:
      level=2
   
   if timerange<=hourl1 and  freqrate>0.67:
      level=3
   if freqrate<=0.34 and  timerange>hourl2:
      level=3
   if timerange<=hourl2 and timerange > hourl1 and freqrate>0.34 and freqrate<=0.67:
      level=3
   
   if timerange<=hourl1  and freqrate>0.34 and freqrate<=0.67:
      level=4
   if timerange<=hourl2 and timerange > hourl1 and freqrate<=0.34:
      level=4

   if timerange<=hourl1 and freqrate<=0.34:
      level=5

   timewindow=float(timesize)/60
   
   print(key,',',level,',',freqrate,',',timerange,',',timewindow)

