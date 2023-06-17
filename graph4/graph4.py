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
N=int(arg[3])
zas=int(arg[4])
allsys=int(arg[5]); system=["Equilibrium","Total\;system"]

m=dp/zas*N
A=os.listdir("./graph4/")
B=[]

for x in A:
    print(x)
    if re.match("DP_L[0-9]+T[0-9]+P\("+str(pp)+"-"+str(pp+dp)+"\)S[0-9]+.txt",x):
        B.append(x)
print(B)





L=[]
t=[]
sites=[]
for x in B:
    C=re.findall(r"[0-9]+",x)
    L.append(int(C[0]))
    t.append(int(C[1]))
    sites.append(int(C[4]))

print(L)
L.sort()
t.sort()
sites.sort()
print(L)
pca_L=[0 for i in range(len(L))]
for ii in range(len(L)):
    ## This part of the code creates the image for the percolation:
    File=pd.read_csv("./graph4/DP_L"+str(L[ii])+"T"+str(t[ii])+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(sites[ii])+".txt",delim_whitespace=True,header=None)
    scaler=StandardScaler()
    scaler.fit(File)
    scaled_data=scaler.transform(File)
    pca=PCA()
    pca.fit(scaled_data)
    x_pca=pca.transform(scaled_data)
    pca_L[ii]=x_pca[:,0]
    #Principal Components
    #N is the number of repetitions
    #int(m/N) is the number of points with different probability

pca_L=np.array(pca_L)    
num=int(m/N)
num_l=len(L)
A=[[0 for i in range(num_l)] for i in range(num)]
B=[[0 for i in range(num_l)] for i in range(num)]
C=[pp+zas*i for i in range(num)]
for l in range(num_l):
    for j in range(num):
        D=np.array([np.abs(f) for f in pca_L[l,N*j:N*(j+1)]])
        A[j][l]=np.mean(D)
        B[j][l]=np.std(D)/np.sqrt(N)
A=np.array(A)
B=np.array(B)
C=np.array(C)
print(A,B,C)




plt.figure(figsize=(8,6))
plt.title(r"$|PC_1|\; vs \;"+"p$"+"\n $for \;different\; sizes\; (L) "+system[allsys]+"$",fontsize=14)
plt.xlabel(r"$Probability\;p\; \times 10^{3}$",fontsize=14)
plt.ylabel(r"$|PC_1|$",fontsize=14)
plt.yscale("log")
for l in range(num_l):
    plt.errorbar(C,A[:,l],yerr=B[:,l],label=r"$|PC_1\;L="+str(L[l])+"|$")
    plt.plot(C,A[:,l],color="black") 

plt.legend()
plt.savefig("./graph4/"+str(allsys)+"_"+str(pp)+"P"+str(dp)+"DP"+str(N)+"N"+"PC1.pdf")

###Regression for the calculation of the minimum:

minis=[ C[A[:,x].argmin()]  for x in range(len(L))]
Linv=[1/l for l in L]

x=np.array(Linv).reshape((-1,1))
zet=np.array(minis)
Result=LinearR2(x,zet)
plt.figure(figsize=(8,6))
plt.xlabel(r"$1/L$",fontsize=14)
plt.ylabel(r"$|P_{c}|$",fontsize=14)
plt.scatter(Linv,minis)
#plt.plot(x,Result[0]+x*Result[2],label=r"$\P_c \approx"+str(round(Result[2],3))+"\pm"+str(round(Result[3],5))+"$")
plt.legend()
plt.savefig("./graph4/"+str(allsys)+"_"+str(pp)+"P"+str(dp)+"DP"+str(N)+"N"+"REGmin.pdf")




