# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 12:45:22 2017

reduce cost

@author: Kun
"""
import api
import numpy as np
import primal as primal
import dual as dual

n = 4 
V = api.makeVset(n)
R = V[0]
N = V[1]

E_T = {((1, 2), 4),
     ((1, 3), None),
     ((1, 4), None),
     ((2, 3), None),
     ((2, 4), None),
     ((3, 4), None)}

P = {((1, 2), 4)}

E_X =  {((1, 3), 4)}

dist_dic = {(1, 2): 1, 
             (1, 3): 5,
             (2, 3): 1,
             (1, 4): 1,
             (2, 4): 5,
             (3, 4): 1}
             
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
        temp = -pi_N[(e[0][0],e[1])] - pi_N[(e[0][1],e[1])] - pi_R[e[1]]      
        reduced_cost[e] = c_e  + temp - pi_N[e[0]]
    else:
        reduced_cost[e] = c_e - pi_N[e[0]]

#opt = False
#entering_edge = None
#for e in E_NB:
#    if f_NB[e] == 0:
#        if reduced_cost[e] < 0:
#            entering_edge = e
#            break
#    elif f_NB[e] == 1:
#        if reduced_cost[e] > 0:
#            entering_edge = e
#            break
#    
#    opt = True
#
##entering edge e prime
#
#s_vector= []
#s