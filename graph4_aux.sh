#!bin/bash
L=""
for ((i=8; i<=$#;i++)); do
    L+=" ${!i}"
done

pp=$1
dp=$2
z=$3
N=$4
allsys=$5
howmuch=$6
cols=$7
for jj in $(seq 1 1 $howmuch)
do
    make varyl dir=./graph4/ starting=OP_ lnumbers="$L" N=$N pp=$pp dp=$dp z=$z allsys=$allsys -j6
    for i in $L
    do
	python3 ./graph4/read4.py $pp $dp $N $z $i $( echo "scale=0; ((sqrt($i)*$i*50)/(10*sqrt(10)))" | bc) $jj $cols; echo "$i" &
    done    
    rm ./graph4/*.txt
done

for ll in $L
do
    python3 ./graph4/pre_read4.py $ll $( echo "scale=0; ((sqrt($ll)*$ll*50)/(10*sqrt(10)))" | bc) $pp $dp $N $z $allsys
done

for jj in $(seq 1 1 $howmuch)
do
    rm ./graph4/*.aux$jj
done

python3 ./graph4/graph4_aux.py $pp $dp $N $z $allsys

