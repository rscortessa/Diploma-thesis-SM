#!bin/bash
L=12000
t=10000
pp=6447
sites= 1500 3000 6000 9000 12000
make varys L=$L t=$t pp=$pp dir=./graph2/ starting=OP_ snumbers="1500 3000 6000 9000 12000"
python3 ./graph2/graph2.py $L $t $pp 1500 3000 6000 9000 12000
