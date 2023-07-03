import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as cl
import statsmodels.api as sm
import sys
import math
import os
import re



def write_text(A,filename):
    if(len(A))>0:
        C=open(filename,"w")
        for ii in range(len(A[0,:])):
            C.write(" ".join(map(str,A[:,ii]))+str("\n"))
            
def LinearR2(col_1, col_2):
    col_1 = sm.add_constant(col_1)
    model = sm.OLS(col_2, col_1)
    results = model.fit()
    COEF = [results.params[0], results.bse[0], results.params[1], results.bse[1],results.rsquared]
    COEF =  np.array(COEF)
    return COEF

##The file has to be loaded:

arg=sys.argv # Arguments giving by console.
pp=int(arg[1]) # Initial probability x 10.000.
dp=int(arg[2]) # Change in probability x 10.000.
N=int(arg[3])
allsys=int(arg[4])
system=["Equilibrium","Total\;system"]

AA=os.listdir("./graph8/")
BB=[]
L=[]
t=[]

for x in AA:
    if re.match(str(allsys)+"_L[0-9]+T[0-9]+P\("+str(pp)+"-"+str(pp+dp)+"\)DS.aux",x):
        BB.append(x)
print("files:",BB)

for file in BB:
    aux=re.findall(r"[0-9]+",file)
    L.append(int(aux[1]))
    t.append(int(aux[2]))

L.sort()
t.sort()

Linv=[1/l for l in L]
Pc=np.array([0 for l in L])

plt.figure(figsize=(8,6))
plt.title(r"$DS(p)$",fontsize=14)
plt.xlabel(r"$p$",fontsize=14)
plt.ylabel(r"$DS$",fontsize=14)


for ii in range(len(L)):
    A=pd.read_csv("./graph8/"+str(allsys)+"_L"+str(L[ii])+"T"+str(t[ii])+"P("+str(pp)+"-"+str(pp+dp)+")DS.aux",delim_whitespace=True,header=None)
    jj=np.where(A[1] == A[1].max())[0][0]
    Pc[ii]=A[0][jj]
    plt.scatter(A[0],A[1],label="L="+str(L[ii]))

plt.legend()    
plt.savefig("./graph8/"+str(allsys)+"_"+str(pp)+"P"+str(dp)+"DP"+str(N)+"N"+"DS.pdf")

x=np.array(Linv).reshape((-1,1))
Result=LinearR2(x,Pc)



plt.figure(figsize=(8,6))
plt.title(r"$Finite\;size\;scaling\;of\;the\;minimum\;of\;\langle P_1 \rangle\;$",fontsize=14)
plt.xlabel(r"$1/L$",fontsize=14)
plt.ylabel(r"$p_{c}$",fontsize=14)
#plt.xscale("log")
plt.xlim([min(Linv)-0.001,max(Linv)+0.001])
plt.scatter(Linv,Pc)
plt.plot(x,Result[0]+x*Result[2],label=r"$p_c \approx"+str(round(Result[0],3))+"\pm"+str(round(Result[1],5))+"$")
plt.legend()
plt.savefig("./graph8/"+str(allsys)+"_"+str(pp)+"P"+str(dp)+"DP"+str(N)+"N"+"REGmin.pdf")
