# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 13:43:50 2017

linear independent

@author: Kun
"""

import api
import numpy as np
import random
import timeit
import newdualitseems as newdual



n = 5
V = api.makeVset(n)
R = V[0]
N = V[1]

dist_dic = {}
for v in N:
    dist_dic[v] = random.randint(10, 100)
    
E_T, E_X, P = api.makeE_B(n,N)
E = api.makeE_set(n)
E_B = [E_T, E_X]


E_NB = E-E_T-set(E_X)        

f_NB = dict.fromkeys(E_NB, 0)


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

#calculate violate buckets need to be its own fucntion
#dont keep track of f_NB and E_NB as well, do it iteratively


for e in f_NB:
    if f_NB[e] == 0 and reduced_cost[e] < 0:
        violate[e] = reduced_cost[e]
    
    elif f_NB[e] == 1 and reduced_cost[e] > 0:
        violate[e] = reduced_cost[e]

print violate


minRC = float('inf')

uij_violate = set()   
for e in violate:
    if e[1] is None:
        uij_violate.add(e)

if len(uij_violate) > 0:
    for e in uij_violate:
        if violate[e] < minRC:
            minRC = violate[e]
            e_prime = e
else:
    for e in violate:
        if violate[e] < minRC:
            minRC = violate[e]
            e_prime = e
        
        
print e_prime
        
        
        
        
        
def changebasis(E_B, e_prime):
    for e in E_B[0]:
        if e[0] == e_prime[0]:
            e_star = e
    
    E_B[0].add(e_prime)
    E_B[0].remove(e_star)
    return E_B, e_star
        
        
        
        
        
        
        
        
        
