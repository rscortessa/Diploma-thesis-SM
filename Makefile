all:DP.x
OBJ= DP.cpp
L=100
t=100
pp=500


main.x:	$(OBJ) 
	g++ $^ -O3  -o $@

graphs: main.x plot.py
	./main.x $(L) $(t) $(pp) 
	python3 plot.py $(L) $(t) $(pp) 

.PHONY:clean
clean:
	rm -f *.x *.o  
