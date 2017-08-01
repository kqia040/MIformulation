# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 11:26:20 2017

change basis

@author: Kun
"""

def changebasis(E_B, e_prime):
    #is eprime xijk or uij
    #if eprime is xijk
    if e_prime[1] is not None:
        k_prime = e_prime[1]
        e_star = None
        for e in E_B[1]:
            if e[1] == k_prime:
                e_star = e
        
        E_B[1].remove(e_star)
        E_B[1].add(e_prime)
        ex_or_et = "E_X"
    else:
        #e_prime is uij
        for e in E_B[0]:
            if e[0] == e_prime[0]:
                e_E_T_go_to_E_X = e
        
        for e in E_B[1]:
            if e[1] == e_E_T_go_to_E_X[1]:
                e_E_X_go_to_E_T = e
        
        for e in E_B[0]:
            if e[0] == e_E_X_go_to_E_T[0]:
                e_star = e
        E_B[0].add(e_prime)
        E_B[0].remove(e_star)
        E_B[1].add(e_E_T_go_to_E_X)
        E_B[0].remove(e_E_T_go_to_E_X)
        E_B[0].add(e_E_X_go_to_E_T)        
        E_B[1].remove(e_E_X_go_to_E_T)
        ex_or_et = "E_T"
        
    return E_B, e_star, ex_or_et

