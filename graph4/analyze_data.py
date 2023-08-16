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
            pca=PCA(n_components=1)
        else:
            pca=IncrementalPCA(n_components=1)
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
            #CC=np.multiply(pca.components_,vary)
            pca_L=np.dot(files,pca.components_.T)
            #print(files,"-",len(CC),"-",len(CC[0]))
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
