import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as cl
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import sys
import gc
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.decomposition import IncrementalPCA

import math

def write_text(A,filename):
    if(len(A))>0:
        C=open(filename,"w")
        for ii in range(len(A[0,:])):
            C.write(" ".join(map(str,A[:,ii]))+str("\n"))



arg=sys.argv

L=int(arg[1])
t=int(arg[2])
pp=int(arg[3])
dp=int(arg[4])
sites=int(arg[5])
N=int(arg[6]) #200
print("This is N",N)
za=int(arg[7])
m=math.floor(dp/za)*N
print("This is m",m)

allsys=int(arg[8])
system=["Equilibrium","Total\;system"]
batch_sizes=int(arg[9])
number=int(arg[10])
## This part of the code creates the image for the percolation:


A=pd.read_csv("./graph10/DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(sites)+".txt",delim_whitespace=True,header=None,dtype=np.uint8)
A.info(memory_usage="deep")

scaler=StandardScaler()
scaler.fit(A)
scaled_data=scaler.transform(A)
pca=IncrementalPCA(n_components=1,batch_size=batch_sizes)

pca.fit(scaled_data)
x_pca=np.abs(pca.transform(scaled_data)[:,0])

##First it is required to chose the points in the graph to analyze the distribution
## As a rule of thumb let's consider four points well distributed in the sample:
Npoints=4
NofP=math.floor(dp/za)
Increment=int(NofP/Npoints)
pca_psamples=[ [x for x in np.sort(x_pca[Increment*i*N:(Increment*i+1)*N]) ] for i in range(Npoints)]

def DiaconisRule(A,N):
    A=np.array(A)
    dx=2*(A[int(3/4*len(A))]-A[int(1/4*len(A))])/N**(1/3)
    Nu=(A.max()-A.min())/dx
    return int(Nu)

Nofpoints=[ DiaconisRule(pca_psamples[i][:],N) for i in range(Npoints)]
counts=[0 for i in range(Npoints)]
bins=[0 for i in range(Npoints)]           
for i in range(Npoints):           
           counts[i],bins[i]=np.histogram(pca_psamples[i][:],bins=Nofpoints[i],density=True)
           bins[i]=bins[i][1:len(bins[i])]
           write_text(np.array(bins[i],counts[i]),str(number)"-"+str(i).txt)

