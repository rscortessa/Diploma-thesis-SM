#Computes the Intrinsic dimensionality of a data set stored in input.dat
# It should be a simple text file in which each row corresponds to a vector of 
# features describing a single data point.
import numpy as np
import scipy as sp
import time
from math import log,sqrt,pow,exp,lgamma,pi
from sklearn.neighbors import NearestNeighbors
data=np.loadtxt("input.dat") 
nbrs = NearestNeighbors(n_neighbors=3, algorithm='ball_tree').fit(data)
distances, indices = nbrs.kneighbors(data)
Nele=distances.shape[0]
dim=Nele/(np.sum(np.log(distances[:,2]/distances[:,1])))
print (dim,dim/sqrt(Nele))
