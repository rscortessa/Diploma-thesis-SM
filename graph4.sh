#!bin/bash
L="$1 $2 $3 $4"
pp=$5
dp=$6
N=$8
z=$7
allsys=$9
make varyl dir=./graph4/ starting=OP_ lnumbers="$1 $2 $3 $4" N=$N pp=$pp dp=$dp z=$z allsys=$9
python3 ./graph4/graph4.py $pp $dp $N $z $allsys


