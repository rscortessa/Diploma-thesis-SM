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
make varyl dir=./graph8/ starting=_ lnumbers="$L" N=$N pp=$pp dp=$dp z=$z allsys=$allsys -j6
for i in $L
do
    python3 ./graph8/compute_ds.py $i $( echo "scale=0; ((sqrt($i)*$i*50)/(10*sqrt(10)))" | bc) $pp $dp $i $N $z $allsys  $smooth; echo "$i" &
done    

python3 ./graph8/size_scaling_ds.py $pp $dp $N $allsys
