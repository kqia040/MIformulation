# -*- coding: utf-8 -*-
"""
Created on Tue Aug 08 11:15:11 2017
trail primal

@author: Kun
"""

import trail_edge_flow as flow
import numpy as np


#b_bar needs to contain two dictionarys

def Primal(V, E_B, MR_inv, b_bar):
    b_N = b_bar[1].copy()
    b_R = b_bar[0].copy()
    #delete this after
    #d_N = b_N
    #E_B[1] is E_X and thus len(E_B[1]) will be size of f_X    
    #hmmm maybe this f_X needs to be a dictionary with edges and shit.
    #f_X = np.zeros(len(E_B[1]), dtype = 'int')
    f_X = dict.fromkeys(E_B[1], 0)
    d_R, d_N, f_T = flow.flow(V, E_B, f_X, b_N)
    
    #hmm u cant just minus those coz those are sets, d_R is a dictionary
    #should be something like this dict(set(b.items()) - set(a.items()))
    #temp = np.array(b_R) - np.array(d_R)    
    temp = {}    
    for i in b_R:
        temp[i] = b_R[i] - d_R[i]
    
    
    #################
    #make list in same order as R
    t2 = [None]*len(V[0])
    #R = V[0]
    for counter in xrange(len(V[0])):
        t2[counter] = temp[V[0][counter]]
    #this vector should be in the order of the list E_X
        
    f_X_vector = np.dot(MR_inv, np.array(t2))
    
    #f_X_vector.astype(int)
    for counter in xrange(len(E_B[1])):
        f_X[list(E_B[1])[counter]] = f_X_vector[counter]
    b_N = b_bar[1].copy()
    b_R, b_N, f_T = flow.flow(V, E_B, f_X, b_N)
    
    return f_T, f_X