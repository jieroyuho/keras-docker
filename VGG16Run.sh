#!/bin/bash

size=10000
targetDir="data"
dir="complete"

while getopts d:s:o: option 
do
case "${option}" 
in
d) targetDir=${OPTARG};;
s) size=${OPTARG};;
o) dir=${OPTARG};;
esac
done


echo $( date +%Y/%m/%d-%H:%M:%S)\ \ \ \ #Begin:

#tar zxvf p1.tgz
#rm unknown*.info.csv

#dir="complete";
dirInput="inputfile";

#shopt -s extglob
#ls !(*info).csv
files=$(ls ${targetDir}/*.csv |grep -vi "info"| tr " " "\n")

mkdir -p ${targetDir}/${dir}
#mkdir -p $dirInput

#mv p1.tgz ./$dirTemp

for file in $files
do

    length=$(wc -l $file | awk '{print $1;}')

    if [ $length -le $size ]
    then
        if [ $length -gt 0 ]
        then 
            echo $( date +%Y/%m/%d-%H:%M:%S)\ \ \ \ #Begin\ \ labelling:\ $file

            python3 VGG16_5485_Label.py $file 

            mv ${file%%.*}.out.csv ${targetDir}/${dir}/$(basename -- ${file%%.*}).complete.csv; 

            #mv ${file} ./${dirInput}/; 

            echo $( date +%Y/%m/%d-%H:%M:%S)\ \ \ \ #Finish\ labelling:\ $file
        else
            echo $( date +%Y/%m/%d-%H:%M:%S)\ \ \ \ #Begin\ \ labelling:\ $file

            cp $file ${targetDir}/${dir}/$(basename -- ${file%%.*}).complete.csv;

            echo $( date +%Y/%m/%d-%H:%M:%S)\ \ \ \ #Finish\ labelling:\ $file
        fi

    else
        echo $( date +%Y/%m/%d-%H:%M:%S)\ \ \ \ #Begin\ \ labelling:\ $file
 
        file_split=${file%%.*}_split
 
        split -a 2 -d -l $size $file $file_split
 
        splitFiles=$(ls ${file_split}* | tr " " "\n")
 
        for sfile in $splitFiles
        do
            echo $( date +%Y/%m/%d-%H:%M:%S)\ \ \ \ #Begin\ \ labelling:\ $sfile
            python3 VGG16_5485_Label.py $sfile 
            echo $( date +%Y/%m/%d-%H:%M:%S)\ \ \ \ #Finish\ \ labelling:\ $sfile
        done
       
        cat ${file_split}*.out.csv >  ${targetDir}/${dir}/$(basename -- ${file%%.*}).complete.csv;
        rm ${file_split}*.out.csv;
        rm ${file%%.*}_split*; 
        #mv ${file} ./${dirInput}/; 
        echo $( date +%Y/%m/%d-%H:%M:%S)\ \ \ \ #Finish\ labelling:\ $file
    fi

done

#mv unknown*.csv ./$dirTemp
#tar zcvf unknown_moeaconn_sip2dipstate_labelled.tgz ./$dir/
echo $( date +%Y/%m/%d-%H:%M:%S)\ \ \ \ #Complete all 
