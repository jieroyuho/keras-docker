#!/bin/bash

#Start Maria DB
#service mysql restart

#Create Table 

DB_NAME="conndb"
DB_USER="acer"
DB_PASS="acer"

SQL1="DROP DATABASE IF EXISTS ${DB_NAME};"
SQL2="CREATE DATABASE IF NOT EXISTS ${DB_NAME};"
SQL3="CREATE USER '${DB_USER}'@'%' IDENTIFIED BY '${DB_PASS}';"
SQL4="GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'%';"
SQL5="FLUSH PRIVILEGES;"
SQL6="source /root/freq.sql"

mysql -e "${SQL1}${SQL2}${SQL3}${SQL4}${SQL5}"
mysql -e "${SQL6}"


