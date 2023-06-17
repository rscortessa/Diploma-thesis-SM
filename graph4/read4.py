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
m=dp/zas*N
num=int(m/N)

filename="./graph4/DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(L)+".txt"

File=pd.read_csv(filename,delim_whitespace=True,header=None,dtype=bool)
scaler=StandardScaler()
scaler.fit(File)
scaled_data=scaler.transform(File)
pca=PCA()
pca.fit(scaled_data)
x_pca=pca.transform(scaled_data)
pca_L=x_pca[:,0]
print()
A=[[0 for i in range(num)],[0 for i in range(num)]]

for j in range(num):
        D=np.array([np.abs(f) for f in pca_L[N*j:N*(j+1)]])
        A[0][j]=np.mean(D)
        A[1][j]=np.std(D)/np.sqrt(N)

write_text(np.array(A),"./graph4/DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(L)+"N"+str(N)+"Z"+str(zas)+".aux")
