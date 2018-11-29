import numpy as np
import sys

fpicpath=sys.argv[1]
finfopath=sys.argv[2]
hour=0.5

fpic=open(fpicpath)
finfo=open(finfopath)

listpic=list()
for line in fpic:
  label=line.split(',')[1800].strip()
  listpic.append(label)


listinfo=list()
for line in finfo:
  listinfo.append(line.strip())

dictinfo=dict()
for pic,info in zip(listpic,listinfo):
  if dictinfo.get(info)== None:
    dictinfo[info]=list()
    dictinfo[info].append(pic)
  else:
    dictinfo[info].append(pic)

for key,data in dictinfo.items():
  nppic=np.array(data).astype(float)
  timelen=len(data)
  freqcount=np.sum(nppic)
  freqrate=freqcount/timelen
  #if timelen==0:
  sip2dip=key.replace('p2_hms','').replace('to',',').replace('_','.')
  #if freqrate>0.8 and timelen >600:
  print(sip2dip,',',freqrate,',',timelen)
  #print key,data
