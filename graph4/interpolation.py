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




arg=sys.argv
pp=int(arg[1])
dp=int(arg[2])
N=int(arg[4])
zas=int(arg[3])
allsys=int(arg[5]); system=["Equilibrium","Total\;system"]
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
for x in BB:
    CC=re.findall(r"[0-9]+",x)
    L.append(int(CC[0]))
    t.append(int(CC[1]))
    sites.append(int(CC[4]))

L.sort()
t.sort()
sites.sort()

pca_L=[0 for i in range(len(L))]
pca_L=np.array(pca_L)    
num=int(m/N)
num_l=len(L)
A=[[0 for i in range(num_l)] for i in range(num)]
B=[[0 for i in range(num_l)] for i in range(num)]
C=[pp+zas*i for i in range(num)]
A=np.array(A)
B=np.array(B)
C=np.array(C)

for ii in range(len(L)):
    ## This part of the code creates the image for the percolation:
    File=pd.read_csv("./DP_L"+str(L[ii])+"T"+str(t[ii])+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(sites[ii])+"N"+str(N)+"Z"+str(zas)+".aux",delim_whitespace=True,header=None)
    print(A[ii,:])
    A[:,ii]=File[0]
    B[:,ii]=File[1]
    #Principal Components
    #N is the number of repetitions
    #int(m/N) is the number of points with different probability

plt.figure(figsize=(8,6))
plt.title(r"$|PC_1|\; vs \;"+"p$"+"\n $for different sizes (L) "+system[allsys]+"$",fontsize=14)
plt.xlabel(r"$Probability\;p\; \times 10^{3}$",fontsize=14)
plt.ylabel(r"$|PC_1|$",fontsize=14)
plt.yscale("log")
for l in range(num_l):
    plt.errorbar(C,A[:,l],yerr=B[:,l],label=r"$|PC_1\;L="+str(L[l])+"|$")
    plt.plot(C,A[:,l],color="black") 

plt.legend()
plt.savefig("./"+str(allsys)+"_"+str(pp)+"P"+str(dp)+"DP"+str(N)+"N"+"PC1.pdf")

###Regression for the calculation of the minimum:

minis=[0 for i in range(len(L))]


plt.figure(figsize=(8,6))
plt.title(r"$|PC_1|\; vs \;"+"p$"+"\n $for different sizes (L) "+system[allsys]+"$",fontsize=14)
plt.xlabel(r"$Probability\;p\; \times 10^{3}$",fontsize=14)
plt.ylabel(r"$|PC_1|$",fontsize=14)
plt.yscale("log")

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
    mymodel=np.poly1d(np.polyfit(X,Y,ww))
    X=np.arange(PI,PF,1)
    Y=mymodel(X)
    jj=np.where(Y == Y.min())[0][0]
    minis[i]=X[jj]
    plt.plot(X,Y)
    plt.errorbar(C,A[:,i],yerr=B[:,i],label=r"$|PC_1\;L="+str(L[i])+"|$")
    plt.plot(C,A[:,i],color="black") 
    plt.plot()

plt.axvline(x=6447, color="b",label="P_c")
plt.legend()
plt.savefig("./"+str(allsys)+"_"+str(pp)+"P"+str(dp)+"DP"+str(N)+"N"+"PCaux.pdf")

Linv=[1/l for l in L]







x=np.array(Linv).reshape((-1,1))
zet=np.array(minis)
Result=LinearR2(x,zet)
plt.figure(figsize=(8,6))
plt.xlabel(r"$1/L$",fontsize=14)
plt.ylabel(r"$|P_{c}|$",fontsize=14)
plt.scatter(Linv,minis)
plt.plot(x,Result[0]+x*Result[2],label=r"$P_c \approx"+str(round(Result[0],3))+"\pm"+str(round(Result[1],5))+"$")
plt.legend()
plt.savefig("./"+str(allsys)+"_"+str(pp)+"P"+str(dp)+"DP"+str(N)+"N"+"REGmin.pdf")




