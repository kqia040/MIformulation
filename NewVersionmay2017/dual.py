# -*- coding: utf-8 -*-
"""
Created on Wed May 24 16:33:55 2017
dual
@author: Kun
"""
#import NodePotential as potential
import secondpotential
import numpy as np

#c_bar, for xijk c(e) = 0 and for uij, c(e) = d(ij)

def dual(V, E_B, E_NB, MR_inv, c_bar):
    c_T = c_bar[0].copy()
    c_X = c_bar[1].copy()
    #pi_R = np.zeros(len(V[0]), dtype='int')
    pi_R = dict.fromkeys(V[0], 0)
#    pi_R, pi_N, c_0 = potential.potential(V, E_B, E_NB, c_T, pi_R)
    pi_R, pi_N, c_0 = secondpotential.potential(V, E_B, c_T, pi_R)
    temp = {}
    for i in c_X:
        temp[i] = c_X[i] - c_0[i]    
    
    #make list in same order as R
    t2 = [None]*len(E_B[1])
    #R = V[0]
    for counter in xrange(len(E_B[1])):
        t2[counter] = temp[list(E_B[1])[counter]]
    #this vector should be in the order of the list E_X
    pi_R_vector = np.dot(np.array(t2), MR_inv)
    
    for counter in xrange(len(V[0])):
        pi_R[V[0][counter]] = pi_R_vector[counter]
        
    c_T = c_bar[0].copy()
#    pi_R, pi_N, c_X = potential.potential(V, E_B, E_NB, c_T, pi_R)
    pi_R, pi_N, c_X = secondpotential.potential(V, E_B, c_T, pi_R)
    return pi_R, pi_N, c_X