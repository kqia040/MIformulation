# -*- coding: utf-8 -*-
"""
Created on Tue May 02 10:59:49 2017

Main py
@author: Kun
"""

import api
import numpy as np
import primal as primal
import dual as dual
#n = 6
n = 4 
V = api.makeVset(n)
R = V[0]
N = V[1]

#dist_dic = {(1, 2): 30, 
#             (1, 3): 26,
#             (2, 3): 24,
#             (1, 4): 50,
#             (2, 4): 40,
#             (3, 4): 24,
#             (1, 5): 40,
#             (2, 5): 50,
#             (3, 5): 26,
#             (4, 5): 30,
#             (1, 6): 25,
#             (2, 6): 60,
#             (3, 6): 30,
#             (4, 6): 45,
#             (5, 6): 10}

dist_dic = {(1, 2): 30, 
             (1, 3): 26,
             (2, 3): 24,
             (1, 4): 50,
             (2, 4): 40,
             (3, 4): 24}


E_T, P = api.makeE_Tset(n)  
  
#need to make E_X somehow
E_X = api.extendbasis(n, P)
#E_T.update(M_R)
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



#need to make c_bar and b_bar
b_bar = [dict.fromkeys(V[0], 1),  dict.fromkeys(V[1], 0)]

c_bar = [{}, {}]
for e in E_T:
    #if edge is uij
    if e[1] is None:
        c_bar[0][e] = dist_dic[e[0]]
    else:
        c_bar[0][e] = 0

for e in E_X:
    c_bar[1][e] = 0

#call primal
f_T, b_bar[0] = primal.Primal(V, E_B, MR_inv, b_bar)
#call dual
pi_N, c_bar[1] = dual.dual(V, E_B, E_NB, MR_inv, c_bar, dist_dic)

#while optimality unmet

#calculate this in a sec
#reducedcost = dict.fromkeys(E_B[0]|E_B[1], None)
#
#
#for e in E_B[0]:
#    temp =     
#    reducedcost[e] = c_bar[0][e] + sum()
#for e in E_B[1]:
#select out of basis arc

#entering arc

#update tree and MR

#call primal and dual again












