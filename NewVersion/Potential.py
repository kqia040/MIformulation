# -*- coding: utf-8 -*-
"""
Created on Thu Apr 06 11:05:27 2017
Potential
@author: Kun
"""



"""
So, the Edge set is the union {xijk U uij} 
So for potential we need to find the reduced cost for all these edges,
For all edges in the basis, the reduce cost is already 0 

"""

def flow(V, E_T, E_X, c_T, pi_R):
    R = V[0]
    N = V[1]
    pi_N = {}
    pi = {}
    c = {}    
    c_X = {}
    for e in E_x:
        c_X[e] = 0
    for v in R:
        #for e in E such that v in {T_e Union {h_e}} 