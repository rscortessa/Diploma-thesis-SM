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
smooth=$6
cols=$7
make varyl dir=./graph9/ starting=_ lnumbers="$L" N=$N pp=$pp dp=$dp z=$z allsys=$allsys -j6
for i in $L
do
    python3 ./graph9/compute_id.py $i $( echo "$(perl -E "say $i**(1.58)" | awk -F'.' '{print $1}')" | bc) $pp $dp $i $N $z $allsys  $smooth; echo "$i" &
done    

#python3 ./graph9/size_scaling_id.py $pp $dp $N $allsys
