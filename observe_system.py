import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy as np

def write_text(A,filename):
    if(len(A))>0:
        C=open(filename,"w")
        for ii in range(len(A[0,:])):
            C.write(" ".join(map(str,A[:,ii]))+str("\n"))

def rho_steady(L,t,pp,dp,N,zas,allsys,sites,m):	
    rho=[0 for i in range(m)]
    p=[pp+zas*i for i in range(m)]
    A=pd.read_csv("DP_L"+str(L)+"T"+str(t)+"P("+str(pp)+"-"+str(pp+dp)+")S"+str(sites)+".txt",delim_whitespace=True,header=None)
    A=np.array(A)
    ###Create an array of the values of rho for the steady state for different values of p.
    for i in range(m):
        rho[i]= np.mean(np.array([ np.mean(A[j,:]) for j in range(i*N,(i+1)*N)]))
    return rho
