import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as cl
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import sys
import os
import re
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.decomposition import IncrementalPCA

from sklearn.preprocessing import PolynomialFeatures
import math
import gc

def write_text(A,filename):
    if(len(A))>0:
        C=open(filename,"w")
        for ii in range(len(A[0,:])):
            C.write(" ".join(map(str,A[:,ii]))+str("\n"))
            

##The file has to be loaded:

arg=sys.argv # Arguments giving by console.
pp=int(arg[1]) # Initial probability x 10.000.
dp=int(arg[2]) # Change in probability x 10.000.
N=int(arg[3]); print("This is N",N) # Number of repetitions for each probability.
za=int(arg[4]) # Increment in the probability for each cycle x 10.000.
m=math.floor(dp/za)*N; print("This is m",m) # Number of points of rows of the data. 
waw=int(m/N) # Number of points in the p-axis
allsys=int(arg[5])
smooth=int(arg[6])
system=["Equilibrium","Total\;system"]

AA=os.listdir("./")
BB=[]

for x in AA:
    print(x)
    if re.match(str(allsys)+"_L[0-9]+T[0-9]+P\("+str(pp)+"-"+str(pp+dp)+"\)S.aux",x):
        BB.append(x)
        

L=[]
t=[]
sites=[]
print(BB)
for x in BB:
    CC=re.findall(r"[0-9]+",x)
    print(CC)
    L.append(int(CC[1]))
    t.append(int(CC[2]))

L.sort()
t.sort()



# It is proccesed the data for the PCA:
# All the points with different probability need to be examined separately:

# It is created the arrays to store the information

S=[[0 for i in range(waw)] for i in range(len(L))]
P=np.array([pp+za*i for i in range(waw)])
ds=[0 for i in range(len(L))]
Y=[0 for i in range(len(L))]
PI=5800
PF=6600
indexPI=0
indexPF=0
X=np.arange(PI,PF,1)

for ii in range(len(P)):
    if P[ii]<PI:
        indexPI=ii
    if P[ii]<PF:
        indexPF=ii        
for i in range(len(L)):
    files=pd.read_csv(str(allsys)+"_L"+str(L[i])+"T"+str(t[i])+"P("+str(pp)+"-"+str(pp+dp)+")S.aux",delim_whitespace=True,header=None)
    S[i][:]=files[1]
    mymodel=np.poly1d(np.polyfit(P[indexPI:indexPF],S[i][indexPI:indexPF],smooth))
    Y[i]=mymodel(X)
    DY=mymodel.deriv(m=1)
    ds[i]=DY(X)

#It is plotted the entropy:
# We define the points were the derivative is calculated
# These points are approximately in the region 5900-6500


plt.figure(figsize=(8,6))
plt.title(r"$S(p)\; vs \;"+"p$"+"\n"+"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.xlabel(r"$Probability\;p\; \times 10^{3}$",fontsize=14)
plt.ylabel(r"$Entropy\;S(p)$",fontsize=14)
for i in range(len(L)):
    plt.scatter(P,S[i][:],label=r"$L="+str(L[i])+"$")
    plt.plot(P,S[i][:],color="black")
    plt.plot(X,Y[i],color="red")
plt.legend()
plt.savefig("./"+str(allsys)+"_"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"S.pdf")
#write_text(np.array([P,S]),"./"+str(allsys)+"_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"S.aux")






#It is calculated the derivative of the entropy and it is plotted as well:
XX=[]
DS=[[] for i in range(len(L))]
maxis=[]
for ii in range(len(X)):
    if X[ii]>=6200 and X[ii]<=6600:
        XX.append(X[ii])
        for jj in range(len(L)):
            DS[jj].append(ds[jj][ii])

plt.figure(figsize=(8,6))
plt.title(r"$dS/dp\; vs \;"+"p$"+"\n"+"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.xlabel(r"$Probability\;p\; \times 10^{3}$",fontsize=14)
plt.ylabel(r"$dS/dp$",fontsize=14)

for i in range(len(L)):
    plt.scatter(XX,DS[i][:],label=r"$L="+str(L[i])+"$")
    plt.plot(XX,DS[i][:],color="black")
plt.legend()
plt.savefig("./"+str(allsys)+"_"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"DS.pdf")


Linv=[1/l for l in L]
DS=np.array(DS)
for jj in range(len(L)):
    mm=np.where(DS[jj] == DS[jj].max())[0][0]
    maxis.append(XX[mm])

plt.figure(figsize=(8,6))
plt.title(r"$size\;scaling\; vs \;"+"p$"+"\n"+"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.ylabel(r"$Probability\;p\; \times 10^{3}$",fontsize=14)
plt.xlabel(r"$L^{-1}$",fontsize=14)
plt.scatter(Linv,maxis)
plt.savefig("size-scaling.png")
#write_text(np.array([XX,DS]),"./"+str(allsys)+"_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")"+"DS.aux")













