# -*- coding: utf-8 -*-
"""
Created on Thu Apr 06 11:05:27 2017
Potential
@author: Kun
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