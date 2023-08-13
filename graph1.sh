#!bin/bash
L=$1
#t=$( echo "scale=0; (sqrt($L)*$L)" | bc)
t=$5
p="$2 $3 $4"
make varyp dir=./graph1/ starting=_OP_ pnumbers="$2 $3 $4" L=$L t=$t N=1000
python3 ./graph1/graph1.py $L $t $p 


