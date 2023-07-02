#!bin/bash
L=$1
t=$( echo "scale=0; (sqrt($L)*$L)" | bc)
make varyp dir=./graph7/ starting=_OP_ pnumbers="$2 $3 $4 $5 $6 $7 $8 $9" L=$L t=$t N=1000
python3 ./graph7/graph7.py $L $t $2 $3 $4 $5 $6 $7 $8 $9


