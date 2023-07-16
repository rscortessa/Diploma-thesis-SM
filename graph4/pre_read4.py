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

### The parameters are defined:

arg=sys.argv
print(arg)
L=int(arg[1])
t=int(arg[2])
pp=int(arg[3])
dp=int(arg[4])
N=int(arg[5])
zas=int(arg[6])
allsys=int(arg[7]); system=["Equilibrium","Total\;system"]
sites=L
m=dp/zas*N
AA=os.listdir("./graph4/")
BB=[]
### We look for the files of the runs we have created, the purpose is to make an average.

for x in AA:
    if re.match("DP_L"+str(L)+"T"+str(t)+"P\("+str(pp)+"-"+str(pp+dp)+"\)S[0-9]+N"+str(N)+"Z"+str(zas)+".aux[0-9]+",x):
        BB.append(x)


num=int(m/N)
num_b=len(BB)


pca=[0 for i in range(num)]
err_pca=[0 for i in range(num)]

pca=np.array(pca)    
err_pca=np.array(err_pca)

A=[[0 for i in range(num_b)] for i in range(num)]
B=[[0 for i in range(num_b)] for i in range(num)]
C=[pp+zas*i for i in range(num)]

A=np.array(A)
B=np.array(B)
C=np.array(C)

### All the files are stored:

for ii in range(num_b):
    ## This part of the code creates the image for the percolation:
    File=pd.read_csv("./graph4/"+BB[ii],delim_whitespace=True,header=None)
    A[:,ii]=File[0]
    B[:,ii]=File[1]

### Then the average is made, and the error is computed.

for ii in range(num):
    pca[ii]=np.mean(A[ii,:])
    err_pca[ii]=np.std(A[ii,:])/np.sqrt(num)
    
write_text(np.array([pca,err_pca]),"./graph4/DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(L)+"N"+str(N)+"Z"+str(zas)+".aux")

