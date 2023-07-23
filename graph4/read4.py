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

sys.path.append("./")
from analyze_data import PCA_txt_




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


pca,pca_L=PCA_txt_(L,t,pp,dp,sites,"/graph4/",entire_set,centralized,read_portion,False)

A=[[0 for j in range(num)],[0 for j in range(num)]]


for j in range(num):
        A[0][j]=np.mean(np.abs(pca_L[N*j:N*(j+1)]))
        A[1][j]=np.std(np.abs(pca_L[N*j:N*(j+1)])/np.sqrt(N*1.0))
        
write_text(np.array(A),"./graph4/DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(L)+"N"+str(N)+"Z"+str(zas)+".aux"+str(howmuch))
