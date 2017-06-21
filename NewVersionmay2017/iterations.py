# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 14:20:20 2017

iterations

@author: Kun
"""

import api
import numpy as np
import dual as dual
import primal as primal
n = 4 
V = api.makeVset(n)
R = V[0]
N = V[1]

dist_dic = {(1, 2): 1, 
             (1, 3): 5,
             (2, 3): 1,
             (1, 4): 1,
             (2, 4): 5,
             (3, 4): 1}
#iteration 2
E_T = {((1, 2), 4),
     ((1, 3), None),
     ((1, 4), None),
     ((2, 3), None),
     ((2, 4), None),
     ((3, 4), None)}

E_X =  {((1, 3), 4)}


             
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

b_bar = [{4: -1}, {(1, 2): 1, (1, 3): 1, (1, 4): 0, (2, 3): 1, (2, 4): 0, (3, 4): 0}]


f_T, f_X, bbarN = primal.Primal(V, E_B, MR_inv, b_bar)



c_T = dict.fromkeys(E_T, 0)

for e in E_T:
    if e[1] is None:
        c_T[e] = dist_dic[e[0]]
    else:
        c_T[e] = 0

c_X = dict.fromkeys(E_X, 0)
for e in E_X:
    if e[1] is None:
        c_X[e] = dist_dic[e[0]]
    else:
        c_X[e] = 0

c_bar = [c_T,c_X]

pi_R, pi_N, c_X = dual.dual(V, E_B, E_NB, MR_inv, c_bar)


#optimality testing
reduced_cost = dict.fromkeys(E_NB, 0)

for e in E_NB:
    if e[1] is not None:
        c_e = 0
    else:
        c_e = dist_dic[e[0]]
    
    #if there is a tail    
        
#    if e[1] is not None:
#        temp = pi_N[(e[0][0],e[1])] + pi_N[(e[0][1],e[1])] + pi_R[e[1]]      
#        reduced_cost[e] = c_e +temp - pi_N[e[0]]
#    else:
#        reduced_cost[e] = c_e - pi_N[e[0]]

    if e[1] is not None:
        temp = pi_N[(e[0][0],e[1])] + pi_N[(e[0][1],e[1])] + pi_R[e[1]]      
        reduced_cost[e] = c_e  + temp - pi_N[e[0]]
    else:
        reduced_cost[e] = c_e - pi_N[e[0]]

print reduced_cost




E_T = {((1, 2), 4),
     ((1, 3), None),
     ((1, 4), None),
     ((2, 3), None),
     ((3, 4), None)}

E_X =  {((1, 3), 4), ((1, 2), None)}


             
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

b_bar = [{4: -1}, {(1, 2): 1, (1, 3): 1, (1, 4): 0, (2, 3): 1, (2, 4): 0, (3, 4): 0}]


f_T, f_X, bbarN = primal.Primal(V, E_B, MR_inv, b_bar)



c_T = dict.fromkeys(E_T, 0)

for e in E_T:
    if e[1] is None:
        c_T[e] = dist_dic[e[0]]
    else:
        c_T[e] = 0

c_X = dict.fromkeys(E_X, 0)
for e in E_X:
    if e[1] is None:
        c_X[e] = dist_dic[e[0]]
    else:
        c_X[e] = 0

c_bar = [c_T,c_X]

pi_R, pi_N, c_X = dual.dual(V, E_B, E_NB, MR_inv, c_bar)


#optimality testing
reduced_cost = dict.fromkeys(E_NB, 0)

for e in E_NB:
    if e[1] is not None:
        c_e = 0
    else:
        c_e = dist_dic[e[0]]
    
    #if there is a tail    
        
#    if e[1] is not None:
#        temp = pi_N[(e[0][0],e[1])] + pi_N[(e[0][1],e[1])] + pi_R[e[1]]      
#        reduced_cost[e] = c_e +temp - pi_N[e[0]]
#    else:
#        reduced_cost[e] = c_e - pi_N[e[0]]

    if e[1] is not None:
        temp = pi_N[(e[0][0],e[1])] + pi_N[(e[0][1],e[1])] + pi_R[e[1]]      
        reduced_cost[e] = c_e  + temp - pi_N[e[0]]
    else:
        reduced_cost[e] = c_e - pi_N[e[0]]

print reduced_cost


