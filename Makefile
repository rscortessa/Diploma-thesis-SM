L=10
t= $(shell echo "scale=0; (sqrt($L)*$L)*50/(10*sqrt(10))" | bc)
pp=5000
dp=40
sites=$L
dir=./
N=200
p1=6425
p2=6447
p3=6460
z=2
allsys=1

%.x:%.cpp 
	@$(CXX) $(CXXFLAGS) -o $@ $< Functions.DP.cpp

DP_OP_L%.txt: DP.x
	if [ -e ${dir}$@ -a -e ${dir}${subst .txt,data.txt,${subst DP_OP,DP,$@}} ]; then \
		echo "Files already exists";\
	else \
		./DP.x $(subst S, ,$(subst .txt, ,$(subst P, ,$(subst T, ,$(subst DP_OP_L, ,$@))))) $(dp) $(N) $(dir); \
	fi

DP_L%.txt: PCA.x
	if [ -e ${dir}$@ ]; then \
		echo "Files already exists";\
	else \
		./PCA.x $(subst S, ,$(subst .txt, ,$(subst P, ,$(subst T, ,$(subst DP_L, ,$@))))) $(dp) $(N) $(dir) $(z) $(allsys); \
	fi

starting=_OP_
pnumbers= 5000 6000 7000 
pvalues=$(addprefix p_,$(pnumbers))
varyp:$(pvalues)
$(pvalues):
	$(MAKE) DP$(starting)L$(L)T$(t)P$(@:p_%=%)S$(sites).txt

lnumbers= 16 20 24 28 32 36
lvalues=$(addprefix l_,$(lnumbers))
varyl:$(lvalues)
$(lvalues):
	$(MAKE) DP_L$(@:l_%=%)T$(shell echo "scale=0; (sqrt($(@:l_%=%))*$(@:l_%=%))*50/(10*sqrt(10))" | bc)P$(pp)S$(@:l_%=%).txt 


starting=_OP_
snumbers= 100 200 300
svalues=$(addprefix s_,$(snumbers))

varys:$(svalues)
$(svalues):
	$(MAKE) DP$(starting)L$(L)T$(t)P$(pp)S$(@:s_%=%).txt 




graphs: DP_OP_L$(L)T$(t)P$(pp)S$(sites).txt plot.py
	python3 plot.py $(L) $(t) $(pp) $(sites) 


graph3: DP_L$(L)T$(t)P$(pp)S$(sites).txt
	python3 ./graph3/graph3.py $(L) $(t) $(pp) $(dp) $(L) $(N)

figure3:
	make graph3 dir=./graph3/



.PHONY: clean
clean:
	rm -f *.x *.o *.txt *.png *~  
