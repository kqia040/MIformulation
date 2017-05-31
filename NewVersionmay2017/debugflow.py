# -*- coding: utf-8 -*-
"""
Created on Wed May 31 11:47:45 2017

Debugg flow

@author: Kun
"""
import api
import numpy as np
import primal as primal
#n = 6
n = 4 
V = api.makeVset(n)
R = V[0]
N = V[1]

E_T = {((1, 2), None),
     ((1, 3), 4),
     ((1, 4), None),
     ((2, 3), None),
     ((2, 4), None),
     ((3, 4), None)}

P = {((1, 3), 4)}

E_X =  {((1, 2), 4)}

dist_dic = {(1, 2): 30, 
             (1, 3): 26,
             (2, 3): 24,
             (1, 4): 50,
             (2, 4): 40,
             (3, 4): 24}
             
E = api.makeE_set(n)
E_B = [E_T, E_X]
E_NB = E-E_T-E_X
#need to make MR_inv matrx with R and M_R

M_R = np.zeros([len(E_X), len(E_X)], dtype='int')
E_X = list(E_X)
R = list(R)
for j in xrange(len(E_X)):
     i = R.index(E_X[j][1])
     M_R[i][j] = -1

MR_inv = np.linalg.inv(M_R)

b_bar = [dict.fromkeys(V[0], 1),  dict.fromkeys(V[1], 0)]


#############################

#Calling primal below

#############################

#f_T, b_bar[0] = primal.Primal(V, E_B, MR_inv, b_bar)

























