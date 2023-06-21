import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as cl
import sys
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import math
arg=sys.argv

# The arguments are received:

pp=[int(arg[i]) for i in range(1,4)]
L=int(arg[4])
t=int(arg[5])
N=int(arg[6])
allsys=int(arg[7])
dp=1
sites=L
m=1

#Labels are created:
system=["Equilibrium","Total\;system"]

# There is created a list to store the eigenvalues:
eigenv=[[] for i in range(3)]
fracvar=[[] for i in range(3)]
## This part of the code creates the image for the percolation:
## We need to iterate over the three probabilities:

for i in range(3):
    filename="./graph6/DP_L"+str(L)+"T"+str(t)+"P("+str(pp[i])+"-"+str(pp[i]+dp)+")S"+str(sites)+".txt"
    print(filename)
    A=pd.read_csv(filename,delim_whitespace=True,header=None)
    scaler=StandardScaler()
    scaler.fit(A)
    scaled_data=scaler.transform(A)
    pca=PCA()
    pca.fit(scaled_data)
    x_pca=pca.transform(scaled_data)
    y=pca.explained_variance_ratio_
    fracvar[i]=y
    sing=pca.singular_values_
    sing=np.array([x**2/np.sum(sing**2) for x in sing])
    eigenv[i]=sing

    
x=[[i for i in range(len(eigenv[j]))] for j in range(3)]
x=np.array(x)

plt.figure(figsize=(8,6))
plt.title(r"$Spectrum\;of\;PCA\;for\;different\;probabilities$"+"\n"
         +"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.yscale("log")
plt.ylim([10**(-6),1])
for i in range(3):
    plt.scatter(x[i],eigenv[i],s=5,label=r"$P="+str(pp[i])+r"\times 10^{-3}$")
    plt.plot(x[i],eigenv[i])
plt.legend()
plt.savefig("./graph6/"+system[allsys]+"Spectrum.png")


plt.figure(figsize=(8,6))
plt.title(r"$Fraction\;of\;Variance\;for\;each\;PCA\;for\;different\;probabilities$"+"\n"
         +"$L="+str(L)+"\;"+"t="+str(t)+"\;"+system[allsys]+"$",fontsize=14)
plt.yscale("log")
plt.ylim([10**(-6),1])
for i in range(3):
    plt.scatter(x[i],fracvar[i],s=5,label=r"$P="+str(pp[i])+r"\times 10^{-3}$")
    plt.plot(x[i],eigenv[i])
plt.legend()
plt.savefig("./graph6/"+system[allsys]+"fracvar.png")


