#!/bin/bash

#=== Start Maria DB ===
service mysql start

#=== Create Table ===

DB_NAME="conndb"
DB_USER="acer"
DB_PASS="acer"

SQL1="DROP DATABASE IF EXISTS ${DB_NAME};"
SQL2="CREATE DATABASE IF NOT EXISTS ${DB_NAME};"
SQL3="CREATE USER '${DB_USER}'@'%' IDENTIFIED BY '${DB_PASS}';"
SQL4="GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'%';"
SQL5="FLUSH PRIVILEGES;"
SQL6="source ./freq.sql"

mysql -e "${SQL1}${SQL2}${SQL3}${SQL4}${SQL5}"
mysql -e "${SQL6}"

#=== Run the Datafilter ===

grep -v ':' /data/${fName}  > conn.v1.csv 
grep -vE '(^[0-9]*,[0-9.]*,[0-9]*,(10.|172.31.|172.16.|172.23.|172.24.|172.69.|224.|239.)[0-9.]*,[0-9]*,[0-9]*$)' conn.v1.csv  > conn.v2.csv  
grep -vE '(^[0-9]*,[0-9.]*,[0-9]*,(210.69.)[0-9.]*,[0-9]*,[0-9]*$)|(:)' conn.v2.csv  > conn.v3.csv  

mv conn.v3.csv conn.csv
rm -f conn.v*

#=== Filter the White list ===

python3 datafilter.py

#=== Excute DB to produce csv

mkdir data

python3 makedatasetunknown.inday.py 30 &
python3 makedatasetunknown.inday.py 60 &
python3 makedatasetunknown.inday.py 120 &
python3 makedatasetunknown.inday.py 240 &
python3 makedatasetunknown.inday.py 480 &
python3 makedatasetunknown.py 1440 &
python3 makedatasetunknown.py 2880 &
python3 makedatasetunknown.py 5760 &
python3 makedatasetunknown.py 10080 &
python3 makedatasetunknown.py 20160 &

#SERVICE=makedatasetunknown.py

waitstatus=1

while [ $waitstatus -eq 1 ]
do

echo $waitstatus
ps -aux | grep -v grep | grep makedatasetunknown.py > /dev/null
result=$?
echo "exit code: ${result}"
if [ "${result}" -eq "0" ] ; then
    echo "`date`: $SERVICE service running, everything is fine"
    waitstatus=1
else
    echo "`date`: $SERVICE is not running"
    waitstatus=0
fi

sleep 10

done


#=== Feed in VGG16 ===

sh ./VGG16Run.sh


#=== Combine ===

projectpath='data'
tagpath=$projectpath/complete/


mkdir $projectpath/freqarrayf
mkdir $projectpath/freqarrayc
mkdir $projectpath/freqarray

cp $projectpath/*.info.csv $tagpath/

python3 post_freqarray.py $tagpath/unknown_conn_sip2dipstate30.complete.csv $tagpath/unknown_conn_sip2dipstate30.info.csv > $projectpath/freqarrayf/freqarray30.csv
python3 post_freqarray.py $tagpath/unknown_conn_sip2dipstate60.complete.csv $tagpath/unknown_conn_sip2dipstate60.info.csv > $projectpath/freqarrayf/freqarray60.csv
python3 post_freqarray.py $tagpath/unknown_conn_sip2dipstate120.complete.csv $tagpath/unknown_conn_sip2dipstate120.info.csv > $projectpath/freqarrayf/freqarray120.csv
python3 post_freqarray.py $tagpath/unknown_conn_sip2dipstate240.complete.csv $tagpath/unknown_conn_sip2dipstate240.info.csv > $projectpath/freqarrayf/freqarray240.csv
python3 post_freqarray.py $tagpath/unknown_conn_sip2dipstate480.complete.csv $tagpath/unknown_conn_sip2dipstate480.info.csv > $projectpath/freqarrayf/freqarray480.csv

python3 post_freqarray.py $tagpath/unknown_conn_sip2dipstate1440.complete.csv $tagpath/unknown_conn_sip2dipstate1440.info.csv > $projectpath/freqarrayc/freqarray1440.csv
python3 post_freqarray.py $tagpath/unknown_conn_sip2dipstate2880.complete.csv $tagpath/unknown_conn_sip2dipstate2880.info.csv > $projectpath/freqarrayc/freqarray2880.csv
python3 post_freqarray.py $tagpath/unknown_conn_sip2dipstate5760.complete.csv $tagpath/unknown_conn_sip2dipstate5760.info.csv > $projectpath/freqarrayc/freqarray5760.csv
python3 post_freqarray.py $tagpath/unknown_conn_sip2dipstate10080.complete.csv $tagpath/unknown_conn_sip2dipstate10080.info.csv > $projectpath/freqarrayc/freqarray10080.csv
python3 post_freqarray.py $tagpath/unknown_conn_sip2dipstate20160.complete.csv $tagpath/unknown_conn_sip2dipstate20160.info.csv > $projectpath/freqarrayc/freqarray20160.csv

echo 'python post_freqarray finsih'

python3 post_freqarray_combine.py f $projectpath/freqarrayf/ > freqarrayf.csv
python3 post_freqarray_combine.py c $projectpath/freqarrayc/ > freqarrayc.csv
cp $projectpath/freqarrayf/* $projectpath/freqarray/
cp $projectpath/freqarrayc/* $projectpath/freqarray/
python3 post_freqarray_combine.py a $projectpath/freqarray/ > /data/${fName}.freqarray.csv
echo 'python post_freqarray_combine finsih'

echo 'freqarray level status'
cat /data/${fName}.freqarray.csv |cut -d ',' -f 3 |sort |uniq -c
echo 'freqarray level 1 timewindows'
grep ', 1 ,' /data/${fName}.freqarray.csv |cut -d ',' -f 6 |sort |uniq -c



