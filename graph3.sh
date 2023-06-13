#!bin/bash

if [ $# -eq 0 ];then
       L=16
       t=80
       pp=6420
       dp=40
       z=2
       N=200
       else
       L=$1
       t=$( echo "scale=0; (sqrt($L)*$L)" | bc)
       pp=$3
       dp=$4
       z=$5
       N=$6
       allsys=$7
       fi
make "DP_L${L}T${t}P${pp}S${L}.txt"  dp=$dp z=$z  dir="./graph3/" N=$N allsys=$allsys    
python3 ./graph3/graph3.py $L $t $pp $dp $L $N $z $allsys
