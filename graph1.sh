#!bin/bash
rm *.x
make main.x
s=12000
y=10000
for ss in 6425 6447 6460
do
    make MonteCarlo L=$s t=$y pp=$ss dir="./graph1/" &
    
done
wait
for ss in 6425 6447 6460
do
    mv "./DP_L"$s"T"$y"P"$ss".txt" "./graph1/."
    mv "./DP_L"$s"T"$y"P"$ss"data.txt" "./graph1/."
    mv "./DP_OP_L"$s"T"$y"P"$ss".txt" "./graph1/."
done
wait

python3 ./graph1/graph1.py $s $y 6425 6447 6460
