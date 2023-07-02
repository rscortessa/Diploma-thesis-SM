
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

L=int(sys.argv[1])
t=int(sys.argv[2])

def LinearR2(col_1, col_2):
    col_1 = sm.add_constant(col_1)
    model = sm.OLS(col_2, col_1)
    results = model.fit()
    COEF = [results.params[0], results.bse[0], results.params[1], results.bse[1],results.rsquared]
    COEF =  np.array(COEF)
    return COEF


plt.figure()
plt.title("$Directed\; Percolation\; in\; (1+1)\; dimensions$ \n"+"$\;L="+str(L)+"\;t="+str(t)+"$")
plt.xlabel(r"$t$")
plt.ylabel(r"$\rho(t)$")
plt.xscale("log")
plt.yscale("log")

for i in range(8):
    B=pd.read_csv("./graph7/DP_OP_L"+sys.argv[1]+"T"+sys.argv[2]+"P"+sys.argv[3+i]+"S"+sys.argv[1]+".txt",delim_whitespace=True,header=None)
    eps=B[0]
    zet=B[1]
    iot=B[2]
    plt.errorbar(eps,zet,yerr=iot,label=r"$\rho(t)$"+" $p="+str(float(sys.argv[3+i])/10000)+"$")

plt.tight_layout()
plt.legend()
plt.savefig("./graph7/L"+str(L)+"T"+str(t)+"graph1.png")
