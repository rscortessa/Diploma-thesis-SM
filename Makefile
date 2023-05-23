all:DP.x
OBJ= Functions.DP.cpp DP.cpp
L=100
t=100
pp=5000
sites= $(L)
dir="./"

main.x:	$(OBJ) 
	g++ $^ -O3  -o $@

MonteCarlo: main.x
	echo "${dir}DP_L${L}T${t}P${pp}.txt"
	if [ -e "${dir}DP_L${L}T${t}P${pp}S${sites}.txt" -a -e "${dir}DP_L${L}T${t}P${pp}S${sites}data.txt" -a -e "${dir}DP_OP_L${L}T${t}P${pp}S${sites}.txt" ]; then \
		echo "Files already exists";\
	else \
		./main.x $(L) $(t) $(pp) $(sites); \
	fi
graphs: MonteCarlo plot.py
	python3 plot.py $(L) $(t) $(pp) $(sites) 


.PHONY: clean
clean:
	rm -f *.x *.o *.txt *.png *~  
