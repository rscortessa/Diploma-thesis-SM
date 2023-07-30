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
    make varyl dir=./graph12/ starting=_ lnumbers="$L" N=$N pp=$pp dp=$dp z=$z allsys=$allsys -j4    
    for i in $L
    do
	python3 ./graph12/read12.py $pp $dp $N $z $i $( echo "$(perl -E "say $i**(1.58)" | awk -F'.' '{print $1}')" | bc) $jj $cols ; echo "$i" & 
    done    
    #rm ./graph4/*.txt
done
wait
for ll in $L
do
    python3 ./graph12/pre_read12.py $ll $( echo "$(perl -E "say $ll**(1.58)" | awk -F'.' '{print $1}')" | bc) $pp $dp $N $z $allsys
done

for jj in $(seq 1 1 $howmuch)
do
    rm ./graph12/*.aux$jj
done

python3 ./graph12/graph12_aux.py $pp $dp $N $z $allsys

