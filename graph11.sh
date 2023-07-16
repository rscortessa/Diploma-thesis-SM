#!bin/bash

L=$1
t=$2
pp=$3
dp=$4
z=$5
N=$6
allsys=$7
batch=$8
howmuch=$9

for jj in $(seq 1 1 $howmuch)
do
    make "DP_L${L}T${t}P${pp}S${L}.txt"  dp=$dp z=$z  dir="./graph11/" N=$N allsys=$allsys ; python3 ./graph11/read11.py $pp $dp $N $z $L $t $jj $batch; echo "$i" &
done
python3 ./graph11/graph11.py $L $t $pp $dp $L $N $z $allsys $howmuch
