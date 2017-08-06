# -*- coding: utf-8 -*-
"""
Created on Tue Aug 01 10:20:43 2017


1/aug/2017

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
n = 5
V = api.makeVset(n)
R = V[0]
N = V[1]

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


notopt = True
exceptset = set()

E_T, E_X, P = api.makeE_B(n,N)

#
#
#E_T = E_B[0]
#E_X = E_B[1]

E_T = list(E_T)
E_X = list(E_X)

E_B = [E_T, E_X]

len_E_X = len(E_X)

M_R = np.zeros([len_E_X, len_E_X])


for j in xrange(len_E_X):
     i = R.index(E_X[j][1])
     M_R[i][j] = -1

MR_inv = np.linalg.inv(M_R)

#num_iter = 0

while notopt:
    
#    num_iter +=1
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
    pi_R, pi_N, c_X = dual.dual(V, E_B, MR_inv, c_bar)
    pi_R.update(pi_N)
    pi_dl = pi_R
    violate = {}
#==============================================================================
#     LAST THING TO IMPLEMENT IS THE BUCKETING THE VIOLATE EDGES
#==============================================================================
    for k in range(4,n+1):
        for j in range(2,n+1):
                for i in range(1,j):
                    if i<j and j<k:
#                        E.add(((i,j),k))
                        e = ((i,j),k)                        
                        if e not in E_B[0] and e not in E_B[1]:
                            c_e = 0
                            temp = pi_dl[(e[0][0],e[1])] + pi_dl[(e[0][1],e[1])] + pi_dl[e[1]]      
                            reduced_cost_e = c_e  + temp - pi_dl[e[0]]
                            if e in exceptset and reduced_cost_e > 0:
                                violate[e] = reduced_cost_e
                            elif e not in exceptset and reduced_cost_e < 0:
                                violate[e] = reduced_cost_e
                        else:
                            continue

    for j in range(2,n+1):
        for i in range(1, n):
            if i<j:
                e = ((i, j), None)
                if e not in E_B[0] and e not in E_B[1]:
                    c_e = dist_dic[e[0]]
                    reduced_cost_e = c_e - pi_dl[e[0]]
                    if e in exceptset and reduced_cost_e > 0:
                        violate[e] = reduced_cost_e
                    elif e not in exceptset and reduced_cost_e < 0:
                        violate[e] = reduced_cost_e
                else:
                    continue
                
    
    len_violate = len(violate)
    print violate
    
    if len_violate == 0:        
        print "Terminate algorithm"
        calccost = api.calcCost(f_T,dist_dic)        
        print "cost is  ", calccost
        notopt = False
        break
#        return len_violate, E_B, E_B_pre, e_star, e_prime
    
    else:
        minRC = float('inf')
    
        for e in violate:
            if violate[e] < minRC:
                minRC = violate[e]
                e_prime = e
    #   
        print "eprime", e_prime
 
        
        
        b_R = dict.fromkeys(V[0], -1)
        b_N = dict.fromkeys(V[1], 0)
        starting_b = [(1,2),(1,3),(2,3)]
        for v in starting_b:
            if v in N:      
                b_N[v] = 1
        
        b_bar = [b_R, b_N]
        
        f_T, f_X = primal.Primal(V, E_B, MR_inv, b_bar)        
        
        if e_prime[1] is None:
            temp_R = dict.fromkeys(V[0], 0)
            temp_N = dict.fromkeys(V[1], 0)
            temp_N[e_prime[0]] = -1         
            temp_bar = [temp_R, temp_N]
        
        elif e_prime[1] is not None:
            ij = e_prime[0]
            k = e_prime[1]
            ik = (e_prime[0][0],e_prime[1])
            jk = (e_prime[0][1],e_prime[1])     
            temp_R = dict.fromkeys(V[0], 0)
            temp_R[k] = 1            
            temp_N = dict.fromkeys(V[1], 0)
            temp_N[ij] = -1
            temp_N[ik] = 1
            temp_N[jk] = 1
            temp_bar = [temp_R, temp_N]
        fbar_T, fbar_X = primal.Primal(V, E_B, MR_inv, temp_bar)  
        
        
#        f_lp = lp_find_flow(E_B, V, 'default')
#        fbar_lp = lp_find_flow(E_B, V, e_prime)
        
        s = {}
        for e in E_B[0]:
            if fbar_T[e] > 0:
                s[e] = ((1-f_T[e])/fbar_T[e])
            elif fbar_T[e] < 0:
                s[e] = f_T[e]/(-fbar_T[e])
            else:
                s[e] = 0
        for e in E_B[1]:
            if fbar_X[e] > 0:
                s[e] = ((1-f_X[e])/fbar_X[e])
            elif fbar_X[e] < 0:
                s[e] = f_X[e]/(-fbar_X[e])
            else:
                s[e] = 0
        
        s[e_prime] = 1
        
        argmin = {}
        for e in s:
            if e in E_B[0] and fbar_T[e] !=0:
                argmin[e] = s[e]
            elif e in E_B[1] and fbar_X[e] !=0:
                argmin[e] = s[e]
                
        argminvalue = min(argmin.values())
    
#        for e in argmin:
#            if argmin[e] > argminvalue:
#                argmin.pop(e)
        keys_to_remove = [key for key, value in argmin.iteritems()
                  if value > argminvalue]
        for key in keys_to_remove:
            del argmin[key]
        
        e_star = None
        
        if len(argmin) == 0:
            e_star = e_prime
        
        else:
#            for e in argmin:
#                if e[1] is not None and e[1] == e_prime[1]:
#                    e_star = e
#            
#            if e_star == None:
            e_star = argmin.popitem()[0]
        
        
                    
        #eprime and estar is not in basis
        
#==============================================================================
#         HERE SHOULD BE WHERE THE CHNAGE BASIS HAPPENS
#       NEED TO TRY KEEP THE BASIS AS A SPANNING TREE OTHERWISE
#       THE FLOW AND PRIMAL ALGORITHM WILL NOT WORK        
#==============================================================================
        
        
        #HERE BSIS DOES NOT CHANGE
        if e_prime == e_star:
        #basis not changed
            if e_prime in exceptset:
                exceptset.remove(e_prime)
            elif e_prime not in exceptset:
                exceptset.add(e_prime)
                
#            gotta change f_T
            f_prime = {}
            for e in E_B[0]:
                if e == e_prime:
                    f_prime[e] = f_T[e]+s[e_star]
                else:
                    f_prime[e] = f_T[e]+fbar_T[e]*s[e_star]
                    
            f_T = f_prime
#            for e in E_B[1]:
#                if e == e_prime:
#                    f_prime[e] = f_X[e]+s[e_star]
#                else:
#                    f_prime[e] = f_X[e]+fbar_X[e]*s[e_star]
       
           
        else:
            #ELSE: BASIS CHANGE            
            oldE_B = copy.deepcopy(E_B) 
            oldV = copy.deepcopy(V) 
            oldMR_inv = copy.deepcopy(MR_inv) 
            E_B, V, MR_inv = update_spanning_tree(E_B, MR_inv, V, e_prime, e_star, fbar_T, fbar_X)
       

        E_T = E_B[0]
        E_X = E_B[1]
        R = V[0]
        N = V[1]
        print "in ",e_prime, "  out ", e_star
        print " "
#        print "len violate", len_violate