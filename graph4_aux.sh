#!bin/bash
L="$1 $2 $3 $4"
pp=$5
dp=$6
N=$8
z=$7
allsys=$9
make varyl dir=./graph4/ starting=OP_ lnumbers="$1 $2 $3 $4" N=$N pp=$pp dp=$dp z=$z allsys=$9 -j6
for i in $L
do
    echo "$i"
    python3 ./graph4/read4.py $pp $dp $N $z $i $( echo "scale=0; ((sqrt($i)*$i*50)/(10*sqrt(10)))" | bc)
done    
python3 ./graph4/graph4_aux.py $pp $dp $N $z $allsys


