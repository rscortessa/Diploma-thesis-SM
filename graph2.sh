#!bin/bash
rm *.x
make main.x

L=12000
t=10000
pp=6447

site1=6000
site2=3000
site3=12000
for ss in $site1 $site2 $site3
do
    make MonteCarlo L=$L t=$t pp=$pp sites=$ss dir="./graph2/" &
    
done
wait
for ss in $site1 $site2 $site3
do
    mv "./DP_L"$L"T"$t"P"$pp"S"$ss".txt" "./graph2/."
    mv "./DP_L"$L"T"$t"P"$pp"S"$ss"data.txt" "./graph2/."
    mv "./DP_OP_L"$L"T"$t"P"$pp"S"$ss".txt" "./graph2/."
done
wait

python3 ./graph2/graph2.py $L $t $pp $site1 $site2 $site3
