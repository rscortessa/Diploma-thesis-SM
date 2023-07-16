#!bin/bash
L=$4
t=$( echo "$(perl -E "say $L**(1.7)" | awk -F'.' '{print $1}')" | bc)
N=$5
allsys=$6
make varyp dp=1 z=1  dir="./graph6/" N=$N allsys=$allsys pnumbers="$1 $2 $3" L=$L t=$t starting=_    
wait
python3 ./graph6/graph6.py $1 $2 $3 $L $t $N $allsys
