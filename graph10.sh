#!bin/bash

L=$1
t=$2
pp=$3
dp=$4
z=$5
N=$6
allsys=$7
batch=$8
make "DP_L${L}T${t}P${pp}S${L}.txt"  dp=$dp z=$z  dir="./graph10/" N=$N allsys=$allsys    
python3 ./graph10/graph10.py $L $t $pp $dp $L $N $z $allsys $batch $9
