import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as cl
import sys
import os
import re
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.interpolate import splev,splrep
from sklearn.preprocessing import PolynomialFeatures



def LinearR2(col_1, col_2):
    col_1 = sm.add_constant(col_1)
    model = sm.OLS(col_2, col_1)
    results = model.fit()
    COEF = [results.params[0], results.bse[0], results.params[1], results.bse[1],results.rsquared]
    COEF =  np.array(COEF)
    return COEF

def write_text(A,filename):
    if(len(A))>0:
        C=open(filename,"w")
        for ii in range(len(A[0,:])):
            C.write(" ".join(map(str,A[:,ii]))+str("\n"))



arg=sys.argv
pp=int(arg[1])
dp=int(arg[2])
zas=int(arg[3])
N=int(arg[4])
allsys=int(arg[5]); system=["Steady\;state","Entire\;evolution"]
ww=int(arg[6])
PI=int(arg[7])
PF=int(arg[8])
m=dp/zas*N
AA=os.listdir("./")
BB=[]

for x in AA:
    if re.match("DP_L[0-9]+T[0-9]+P\("+str(pp)+"-"+str(pp+dp)+"\)S[0-9]+N"+str(N)+"Z"+str(zas)+".aux",x):
        BB.append(x)

L=[]
t=[]
sites=[]
print(BB)
for x in BB:
    CC=re.findall(r"[0-9]+",x)
    print(CC)
    L.append(int(CC[0]))
    t.append(int(CC[1]))
    sites.append(int(CC[4]))

L.sort()
t.sort()
sites.sort()

pca_L=[0.0 for i in range(len(L))]
pca_L=np.array(pca_L)    
num=int(m/N)
num_l=len(L)
A=[[0.0 for i in range(num_l)] for i in range(num)]
B=[[0.0 for i in range(num_l)] for i in range(num)]
C=[pp+zas*i for i in range(num)]
A=np.array(A)
B=np.array(B)
C=np.array(C)

for ii in range(len(L)):
    ## This part of the code creates the image for the percolation:
    File=pd.read_csv("./DP_L"+str(L[ii])+"T"+str(t[ii])+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(sites[ii])+"N"+str(N)+"Z"+str(zas)+".aux",dtype=float,delim_whitespace=True,header=None)
    A[:,ii]=File[0]
    B[:,ii]=File[1]
    #Principal Components
    #N is the number of repetitions
    #int(m/N) is the number of points with different probability

plt.figure(figsize=(8,6))
plt.title(r"$ \langle |P_2| \rangle \; vs \;"+"p$"+"\n $for \;different\; sizes\; (L)\; "+system[allsys]+"$",fontsize=18)
plt.xlabel(r"$Probability\;p\;$",fontsize=18)
plt.ylabel(r"$\langle |P_2| \rangle$",fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
for l in range(num_l):
    plt.errorbar(C/10000,A[:,l],yerr=B[:,l],label=r"$L="+str(L[l])+"$")
    plt.plot(C/10000,A[:,l],color="black") 
plt.axvline(x=0.6447, color="b",label="$p_c$")
plt.legend(fontsize=18)
plt.savefig("./"+str(allsys)+"_"+str(pp)+"P"+str(dp)+"DP"+str(N)+"N"+"PC2.png")

###Regression for the calculation of the minimum:

minis=[0.0 for i in range(len(L))]


plt.figure(figsize=(8,6))
plt.title(r"$\langle |P_2| \rangle\; vs \;"+"p$"+"\n $for different sizes (L) "+system[allsys]+"$",fontsize=18)
plt.xlabel(r"$Probability\;p$",fontsize=18)
plt.ylabel(r"$\langle |P_2| \rangle $",fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
#PI=5000
#PF=7000
for i in range(len(L)):
    X=[]
    Y=[]
    for ii in range(len(C)):
        if C[ii]>=PI and C[ii]<=PF:
            X.append(C[ii])
            Y.append(A[ii,i])
    sp1=splrep(X,Y)
    X=np.linspace(PI,PF,2000)
    Y=splev(X,sp1)
    fitting=np.polyfit(X,Y,ww)
    mymodel=np.poly1d(fitting)
    X=np.arange(PI,PF,1)
    Y=mymodel(X)
    jj=np.where(Y == Y.min())[0][0]
    minis[i]=X[jj]
    plt.plot(X/10000,Y)
    plt.errorbar(C/10000,A[:,i],yerr=B[:,i],label=r"$\;L="+str(L[i])+"$")
    plt.plot(C/10000,A[:,i],color="black") 
    plt.plot()

plt.axvline(x=0.6447, color="b",label="$p_c$")
plt.legend(fontsize=18)
plt.savefig("./"+str(allsys)+"_"+str(pp)+"P"+str(dp)+"DP"+str(N)+"N"+"PCaux.png")


if len(L)>3:
    Linv=[1/l for l in L]
    Linv.reverse()
    minis.reverse()
    Linv=np.array(Linv)
    zet=np.array(minis)
    minis=np.array(minis)

    ##Polynomial fit
    sp1=splrep(Linv,zet)
    X=np.linspace(min(Linv),max(Linv),200)
    Y=splev(X,sp1)
    fitting,cov=np.polyfit(X,Y,2,full=False,cov=True)
    mymodel=np.poly1d(fitting)
    ## Examine values
    print(fitting)
    print(cov)
    ## Fitting
    X=np.linspace(0,max(Linv),200)
    Y=mymodel(X)
    ## Fitting
    print(mymodel)
    Yo=mymodel([0])[0]
    dyo=np.sqrt(cov[2][2])

    ## Linear fit
    pc=6447.0
    x=np.array(Linv).reshape((-1,1))
    Result=LinearR2(x,zet)
    plt.figure(figsize=(8,6))
    plt.title(r"$Finite\;size\;scaling\;of\;the\;minimum\;of\;\langle| P_2| \rangle\;$",fontsize=14)
    plt.xlabel(r"$1/L$",fontsize=14)
    plt.ylabel(r"$p^*$",fontsize=14)
    plt.xlim([0.0001,max(Linv)+0.001])
    plt.scatter(Linv,minis/10000,color="red")
    #plt.plot(x,(Result[0]+x*Result[2])/10000,label=r"$p_c^* \approx("+str(round(Result[0],3))+"\pm"+str(round(Result[1],5))+r")\times 10^{-3}$")
    plt.plot(X,Y/10000,label=r"$p_c \approx("+str(round(Yo,3))+"\pm"+str(round(dyo,3))+r")\times 10^{-3}$")
    plt.axhline(y=0.6447,color="black",label="$p_c$")
    #plt.xscale("log")
    plt.yscale("log")
    plt.legend()
    plt.savefig("./"+str(allsys)+"_"+str(pp)+"P"+str(dp)+"DP"+str(N)+"N"+"REGmin.pdf")

    write_text(np.array([Linv,zet]),"./Qtiplot"+".aux")



