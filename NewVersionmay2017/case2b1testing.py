# -*- coding: utf-8 -*-
"""
Created on Tue Aug 08 13:18:34 2017

@author: Kun
"""
import api
import numpy as np
import random
import newdualitseems as newdual
import time
import copy
import primal
import dual


e_prime =  ((2, 4), 5)
e_star = ((2, 4), None)

E_B = [[((3, 5), None),
  ((1, 4), 5),
  ((2, 4), None),
  ((1, 5), None),
  ((3, 4), None),
  ((2, 3), None),
  ((1, 2), 5),
  ((4, 5), None),
  ((1, 3), 4)],
 [((2, 3), 4), ((1, 2), None), ((3, 4), 5)]]
 
V = [[4, 5, (2, 5)],
 [(1, 2), (1, 3), (2, 3), (1, 4), (2, 4), (3, 4), (1, 5), (3, 5), (4, 5)]]

MR_inv = np.array([[-1.,  0.,  0.],
       [ 0.,  0.,  1.],
       [ 0., -1.,  1.]])
       
fbar_T = {((1, 2), 5): -1.0,
 ((1, 3), 4): 0,
 ((1, 4), 5): 0,
 ((1, 5), None): -1.0,
 ((2, 3), None): 0.0,
 ((2, 4), None): -1.0,
 ((3, 4), None): 0.0,
 ((3, 5), None): 0.0,
 ((4, 5), None): 1.0}

fbar_X = {((1, 2), None): 1.0, ((2, 3), 4): 0.0, ((3, 4), 5): 0.0}

Case = None
R = V[0]
N = V[1]    
#    RR = set(V[0])    
if e_star[1] is not None:    
    e_star_head_tail_set_union = {e_star[0], (e_star[0][0],e_star[1]), (e_star[0][1],e_star[1]), e_star[1]}
elif e_star[1] is None:
    e_star_head_tail_set_union = {e_star[0]}
    
e_bar = None
tempset = copy.deepcopy(e_star_head_tail_set_union)
for e in E_B[1]:
    if e[1] is not None:
        temp_e_v_set = {e[0], (e[0][0],e[1]), (e[0][1],e[1]), e[1]}
    elif e[1] is None:
        temp_e_v_set = {e[0]}
    
    if tempset.issubset(temp_e_v_set):
#                if fbar_X[e] != 0:                
        e_bar = e
        break
    
    

Case = 'first'
newV = copy.deepcopy(V)
intermediateE_B = copy.deepcopy(E_B)
intermediateE_B[0][intermediateE_B[0].index(e_star)] = e_bar
intermediateE_B[1][intermediateE_B[1].index(e_bar)] = e_star
intermediateMR_inv = None
newE_B = None
intermediateMR_inv = update_MR_inv(Case, MR_inv, intermediateMR_inv, V, newV, E_B, intermediateE_B, newE_B, e_prime, e_star, e_bar, fbar_T, fbar_X)
#            Case = '2a-second-iteration'
Case = 'second'
newE_B = copy.deepcopy(intermediateE_B)
newE_B[1][newE_B[1].index(e_star)] = e_prime
newMR_inv = update_MR_inv(Case, MR_inv, intermediateMR_inv, V, newV, E_B, intermediateE_B, newE_B, e_prime, e_star, e_bar, fbar_T, fbar_X)





def update_MR_inv(Case, MR_inv, intermediateMR_inv, V, newV, E_B, intermediateE_B, newE_B, e_prime, e_star, e_bar, fbar_T, fbar_X):
    print "case is ", Case    
    if newV is None:
        newV = V
    newR = newV[0]
    R = V[0]
    N = V[1]
    len_newR = len(newR)
    if Case == 'first':        
        temp_matrix = np.zeros([len_newR,len_newR])
        #in the first iteration here
        #e_star is e_bar
        #e_prime is e_star      
        fbar_e_star = None
        if e_star in fbar_X:
            fbar_e_star = fbar_X[e_star]
        elif e_star in fbar_T:
            fbar_e_star = fbar_T[e_star]        
        print fbar_e_star
        for v in newR:
            temp_R = dict.fromkeys(V[0], 0)
            temp_N = dict.fromkeys(V[1], 0)
            if v in R:
                temp_R[v] = 1
            elif v in N:
                temp_N[v] = 1
            temp_bar = [temp_R, temp_N]
            phi_T, phi_X = primal.Primal(V, E_B, MR_inv, temp_bar)
#            nn, mm = primal.Primal(V, intermediateE_B, intermediateMR_inv1, temp_bar)
            
            for e in intermediateE_B[1]:       
                if e == e_star:    
                    temp_val = -1*((phi_T[e_star])/fbar_e_star)
                    temp_matrix[intermediateE_B[1].index(e)][newR.index(v)] = temp_val
                else:
                    #all the e is in existing E_X but v not be in existing R
                    temp_val = MR_inv[E_B[1].index(e)][V[0].index(v)] - (((phi_T[e_star])/fbar_e_star)*fbar_X[e])
                    temp_matrix[intermediateE_B[1].index(e)][newR.index(v)] = temp_val
                    break
            break
                    
            
        return temp_matrix 

#    elif Case == 'second':
#        temp_matrix = np.zeros([len_newR,len_newR])
#        #in the first iteration here
#        #e_star is e_bar
#        #e_prime is e_star      
#        fbar_e_star = None
#        if e_star in fbar_X:
#            fbar_e_star = fbar_X[e_star]
#        elif e_star in fbar_T:
#            fbar_e_star = fbar_T[e_star]        
#        print fbar_e_star
#        for v in newR:
#            temp_R = dict.fromkeys(V[0], 0)
#            temp_N = dict.fromkeys(V[1], 0)
#            if v in R:
#                temp_R[v] = 1
#            elif v in N:
#                temp_N[v] = 1
#            temp_bar = [temp_R, temp_N]
#            phi_T, phi_X = primal.Primal(V, E_B, MR_inv, temp_bar)
##            nn, mm = primal.Primal(V, intermediateE_B, intermediateMR_inv1, temp_bar)
#            
#            for e in newE_B[1]:       
#                if e == e_prime:    
#                    temp_val = -1*((intermediateMR_inv[intermediateE_B[1].index(e_star)][newR.index(v)])/fbar_e_star)
#                    temp_matrix[newE_B[1].index(e)][newR.index(v)] = temp_val
#                else:
#                    #all the e is in existing E_X but v not be in existing R
#                    if e in fbar_T:
#                        f__e = fbar_T[e]
#                    else:
#                        f__e = fbar_X[e]
#                    temp_val = intermediateMR_inv[intermediateE_B[1].index(e)][V[0].index(v)] - (((intermediateMR_inv[intermediateE_B[1].index(e_star)][newR.index(v)])/fbar_e_star)*f__e)
#                    temp_matrix[newE_B[1].index(e)][newR.index(v)] = temp_val
#            
#        return temp_matrix 











