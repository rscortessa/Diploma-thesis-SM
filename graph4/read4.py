import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as cl
import sys
import os
import re
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import IncrementalPCA
import tracemalloc

def write_text(A,filename):
    if(len(A))>0:
        C=open(filename,"w")
        for ii in range(len(A[0,:])):
            C.write(" ".join(map(str,A[:,ii]))+str("\n"))

arg=sys.argv
pp=int(arg[1])
dp=int(arg[2])
N=int(arg[3])
zas=int(arg[4])
L=int(arg[5])
t=int(arg[6])
howmuch=int(arg[7])
portion=int(arg[8])

read_portion=int(m*portion/100)
r_portion=(portion/100*N)

entire_set=True

if portion==100:
    entire_set=True
else:
    entire_set=False

m=dp/zas*N
num=int(m/N)

###Length of the file: m*N

filename="./graph4/DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(L)+".txt"





A=[[0 for i in range(num)],[0 for i in range(num)]]
pca_L=np.array([])
pca=IncrementalPCA(n_components=1)

if entire_set==True:
    files=pd.read_csv(filename,delim_whitespace=True,header=None,dtype=np.uint8)
    scaler=StandardScaler()
    scaler.fit(files)
    scaled_data=scaler.transform(files)
    pca=PCA(n_components=1)
    pca.fit(scaled_data)
    x_pca=pca.transform(scaled_data)

else:
    tracemalloc.start()
    with pd.read_csv(filename,delim_whitespace=True,header=None,dtype=np.uint8,chunksize=read_portion) as reader:
        for chunk in reader:
            print(chunk,sys.getsizeof(chunk))
            pca.partial_fit(chunk)    
    print("PCA",sys.getsizeof(pca))

    with pd.read_csv(filename,delim_whitespace=True,header=None,dtype=np.uint8,chunksize=read_portion) as reader:
        for chunk in reader:
            x_pca=pca.transform(chunk)
            x_pca=np.abs(x_pca[:,0])
            pca_L=np.concatenate((pca_L,x_pca),axis=0)
    print(tracemalloc.get_traced_memory())
    tracemalloc.stop()

    
for j in range(num):
        A[0][j]=np.mean(pca_L[N*j:N*(j+1)])
        A[1][j]=np.std(pca_L[N*j:N*(j+1)])/np.sqrt(N*1.0)

write_text(np.array(A),"./graph4/DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(L)+"N"+str(N)+"Z"+str(zas)+".aux"+str(howmuch))
