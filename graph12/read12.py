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
from sklearn.decomposition import PCA

import tracemalloc
import math

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

def PCA_txt_(L,t,pp,dp,sites,diry,entire_set,centralized,read_portion,allpc):
    filename="."+diry+"DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(sites)+".txt"

    ## Check what procedure has to be followed, in order to be the more effective.
    ##########################################
    if allpc==True:
        if entire_set==True:
            pca=PCA()
        else:
            pca=IncrementalPCA()
    else:
        if entire_set==True:
            pca=PCA(n_components=2)
        else:
            pca=IncrementalPCA(n_components=2)
    ##########################################
    
    if entire_set==True:
        files=pd.read_csv(filename,delim_whitespace=True,header=None,dtype=np.uint8)
        if centralized==False:
            vary=np.array(files.std())
        scaler=StandardScaler()
        scaler.fit(files)
        scaled_data=scaler.transform(files)
        pca.fit(scaled_data)
        if centralized==False:
            pca_L=np.dot(files,np.multiply(pca.components_.T,vary))
        else:
            pca_L=pca.transform(scaled_data)
    else:
        with pd.read_csv(filename,delim_whitespace=True,header=None,dtype=np.uint8,chunksize=read_portion) as reader:
            for chunk in reader:
                print(chunk,sys.getsizeof(chunk))
                pca.partial_fit(chunk)    
            print("PCA",sys.getsizeof(pca))
        pca_L=np.array([])
        with pd.read_csv(filename,delim_whitespace=True,header=None,dtype=np.uint8,chunksize=read_portion) as reader:
            for chunk in reader:
                if centralized==False:
                    x_pca=np.dot(chunk,pca.components_.T)
                else:
                    x_pca=pca.transform(chunk)
                try:
                    pca_L=np.concatenate((pca_L,x_pca),axis=0)
                except:
                    pca_L=x_pca
    return pca,pca_L




def write_text(A,filename):
    if(len(A))>0:
        C=open(filename,"w")
        for ii in range(len(A[0,:])):
            C.write(" ".join(map(str,A[:,ii]))+str("\n"))

arg=sys.argv
print(arg)
pp=int(arg[1])
dp=int(arg[2])
N=int(arg[3])
zas=int(arg[4])
L=int(arg[5])
t=int(arg[6])
howmuch=int(arg[7])
portion=int(arg[8])
m=math.floor(dp/zas)*N
read_portion=int(m*portion/100)
r_portion=(portion/100*N)

entire_set=True
centralized=True
sites=L
num=math.floor(dp/zas)

if portion==100:
    entire_set=True
else:
    entire_set=False


pca,pca_L=PCA_txt_(L,t,pp,dp,sites,"/graph12/",entire_set,centralized,read_portion,False)

A=[[0.0 for j in range(num)],[0.0 for j in range(num)]]


for j in range(num):
        A[0][j]=np.mean(np.abs(pca_L[N*j:N*(j+1),1]))
        A[1][j]=np.std(np.abs(pca_L[N*j:N*(j+1),1])/np.sqrt(N*1.0))
        
write_text(np.array(A),"./graph12/DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(L)+"N"+str(N)+"Z"+str(zas)+".aux"+str(howmuch))
