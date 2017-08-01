# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 11:13:31 2017

@author: Kun
"""

#test scrfipt

import api
import numpy as np
import primal as primal
import newdualitseems as newdual
import changebasis

dist_dic = {(1, 2): 30, 
             (1, 3): 26,
             (2, 3): 24,
             (1, 4): 50,
             (2, 4): 40,
             (3, 4): 24,
            (1,5): 40,
            (2,5): 50,
            (3,5): 26,
            (4,5): 30}
n = 5
V = api.makeVset(n)
R = V[0]
N = V[1]

E_T, P = api.makeE_Tset(n)
E_X = api.extendbasis2(n, P)

E = api.makeE_set(n)
E_B = [E_T, E_X]
E_NB = E-E_T-set(E_X)        

f_NB = dict.fromkeys(E_NB, 0)

#==============================================================================
# this is where the simplex starts
#==============================================================================
M_R = np.zeros([len(E_X), len(E_X)], dtype='int')
E_X = list(E_X)
R = list(R)
for j in xrange(len(E_X)):
     i = R.index(E_X[j][1])
     M_R[i][j] = -1

MR_inv = np.linalg.inv(M_R)

b_R = dict.fromkeys(V[0], -1)
b_N = dict.fromkeys(V[1], 0)
b_N[(1,2)] = 1
b_N[(1,3)] = 1
b_N[(2,3)] = 1

b_bar = [b_R, b_N]

f_T, f_X, bbarN = primal.Primal(V, E_B, MR_inv, b_bar)


pi_dl = newdual.newdual(E_B, dist_dic, V)

pi_N = {}
pi_R = {}

for v in pi_dl:
    if v in N:
        pi_N[v] = pi_dl[v]
    elif v in R:
        pi_R[v] = pi_dl[v]



reduced_cost = dict.fromkeys(E_NB, 0)

for e in E_NB:
    if e[1] is not None:
        c_e = 0
    else:
        c_e = dist_dic[e[0]]

    if e[1] is not None:
        temp = pi_N[(e[0][0],e[1])] + pi_N[(e[0][1],e[1])] + pi_R[e[1]]      
        reduced_cost[e] = c_e  + temp - pi_N[e[0]]
    else:
        reduced_cost[e] = c_e - pi_N[e[0]]


violate = {}

for e in f_NB:
    if f_NB[e] == 0 and reduced_cost[e] < 0:
        violate[e] = reduced_cost[e]
    
    elif f_NB[e] == 1 and reduced_cost[e] > 0:
        violate[e] = reduced_cost[e]

print violate

if len(violate) == 0:
    output_cost = api.calcCost(f_T,dist_dic)    
    print "Terminate algorithm"
    print "cost is"
    print output_cost


else:
    minRC = float('inf')
    for e in violate:
        if violate[e] < minRC:
            minRC = violate[e]
            e_prime = e
        
        
    E_B, e_star, ex_or_et = changebasis.changebasis(E_B, e_prime)
    
    #ex_or_et tells us if e_star (the leaving arc) is from e_x or e_T
    #so that when we add estar to f_Nb we know where to get the flow data from
    if ex_or_et == "E_X":
        f_NB.pop(e_prime)
        E_NB.add(e_star)
        E_NB.remove(e_prime)    
        f_NB[e_star] = f_X[e_star]
    else:
        f_NB.pop(e_prime)
        E_NB.add(e_star)
        E_NB.remove(e_prime)    
        f_NB[e_star] = f_T[e_star]
    
    E_T = E_B[0]
    E_X = E_B[1]
    
    del(f_T)
    del(f_X)


 




















