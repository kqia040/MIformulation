# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 09:30:33 2017
Primal
@author: Kun
"""
import Flow
import Potential

def primal(H, T_R, M_R_Inv, b_bar):
    b_R = b_bar[0]
    b_N = b_bar[1]
    ##flow doesnt take T_R as an argument at this stage
    d_R, f_T = flow(V, E_T, E_X, b_N, 0)
    f_X = M_R_Inv * (b_R - d_R)
    b_R, f_T = flow(V, E_T, E_X, d_R, f_X)
    f = f_T.update(f_X)
    #d = d_R.update(d_N)    
    #return d, f
    return f
    
def dual(H, T_R, M_R_Inv, c_bar):
    c_T = c_bar[0]
    c_X = c_bar[1]
    c_0, pi_0_N = potential(V, E_T, E_X, c_T, 0)
    pi_R = (c_X - c_0)*M_R_Inv
    c_X, pi_N = potential(V, E_T, E_X, c_T, pi_R)
    c = c_T.update(c_X)
    pi = pi_R.update(pi_N)    
    return c, pi