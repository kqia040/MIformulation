# -*- coding: utf-8 -*-
"""
Created on Tue Aug 08 19:37:11 2017


CREATE INITIAL SPANNING TREE


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
from EdgeFlow import flow
from secondpotential import potential

from update_spanning_tree import update_spanning_tree
from update_spanning_tree2 import update_spanning_tree2



n = 5
V_vector = api.makeVset(n)
V = [[],V_vector[0] + V_vector[1]]
R= V[0]
N = V[1]
dist_dic = {}
for v in V_vector[0]:
    dist_dic[(None, v)] = float('inf')
for v in V_vector[1]:
    dist_dic[v] = random.randint(10, 100)
exceptset = set()
dist_dic = {(None, 4): float('inf'),
 (None, 5): float('inf'),
 (1, 2): 44,
 (1, 3): 22,
 (1, 4): 92,
 (1, 5): 25,
 (2, 3): 77,
 (2, 4): 87,
 (2, 5): 31,
 (3, 4): 20,
 (3, 5): 92,
 (4, 5): 35}
E_T = []
E_X = []
E_B = [E_T, E_X]

MR_inv = np.eye(0)

for v in V[1]:
    if v in [4, 5]:
        E_T.append((None, v))
    else:
        E_T.append((v, None))
    


c_T = dict.fromkeys(E_T, 0)

for e in E_T:
    if e[1] is None:
        c_T[e] = dist_dic[e[0]]
    else:
        if e[0] is None:
            c_T[e] = dist_dic[(None, e[1])]
        else:
            c_T[e] = 0

c_X = dict.fromkeys(E_X, 0)
for e in E_X:
    if e[1] is None:
        c_X[e] = dist_dic[e[0]]
    else:
        c_X[e] = 0


c_bar = [c_T,c_X]


c_T = copy.deepcopy(c_bar[0]) 
c_X = copy.deepcopy(c_bar[1]) 
#pi_R = np.zeros(len(V[0]), dtype='int')
pi_R = dict.fromkeys(V[0], 0)
#    pi_R, pi_N, c_0 = potential.potential(V, E_B, E_NB, c_T, pi_R)
pi_R, pi_N, c_0 = potential(V, E_B, c_T, pi_R)





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

f_X = {}
b_R = dict.fromkeys(V[0], 0)
b_N = dict.fromkeys(V[1], 0)
starting_b = [4,5,(1,2),(1,3),(2,3)]
for v in starting_b:
    if v ==4 or v ==5:
        b_N[v] = -1
    else:      
        b_N[v] = 1

b_bar = [b_R, b_N]

d_R, d_N, f_T = flow(V, E_B, f_X, b_N)

if len_violate == 0:        
    print "Terminate algorithm"
    calccost = api.calcCost(f_T,dist_dic)        
    print "cost is  ", calccost
    notopt = False



minRC = float('inf')
    
for e in violate:
    if violate[e] < minRC:
        minRC = violate[e]
        e_prime = e
#   
print "eprime", e_prime

if e_prime[1] is None:
    temp_R = dict.fromkeys(V[0], 0)
    temp_N = dict.fromkeys(V[1], 0)
    if e_prime[0] in R:      
        temp_R[e_prime[0]] = -1         
    else:
        temp_N[e_prime[0]] = -1  
    temp_bar = [temp_R, temp_N]

elif e_prime[1] is not None:
    ij = e_prime[0]
    k = e_prime[1]
    ik = (e_prime[0][0],e_prime[1])
    jk = (e_prime[0][1],e_prime[1])     
    temp_R = dict.fromkeys(V[0], 0)      
    temp_N = dict.fromkeys(V[1], 0)
    vset = [ij, ik, jk, k]            
    for v in vset:
        if v in V[0]:
            if v ==ij:
                temp_R[v] = -1
            else:
                temp_R[v] = 1
        if v in V[1]:
            if v == ij:
                temp_N[v] = -1
            else:
                temp_N[v] = 1
    
    temp_bar = [temp_R, temp_N]


dbar_R, dbar_N, fbar_T = flow(V, E_B, f_X, temp_N)  
fbar_X = {}
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

e_star = None
        
if len(argmin) == 0:
    e_star = e_prime

else:
#            for e in argmin:
#                if e[1] is not None and e[1] == e_prime[1]:
#                    e_star = e
#            
#            if e_star == None:    
#    argminvalue = min(argmin.values())
#
##        for e in argmin:
##            if argmin[e] > argminvalue:
##                argmin.pop(e)
#    keys_to_remove = [key for key, value in argmin.iteritems()
#              if value > argminvalue]
#    for key in keys_to_remove:
#        del argmin[key]
#    e_star = argmin.popitem()[0]
    for e in argmin:
        if e[0] is None:
            e_star = e
        
        if e_star is None:
        
            argminvalue = min(argmin.values())
        
    #        for e in argmin:
    #            if argmin[e] > argminvalue:
    #                argmin.pop(e)
            keys_to_remove = [key for key, value in argmin.iteritems()
                      if value > argminvalue]
            for key in keys_to_remove:
                del argmin[key]
            e_star = argmin.popitem()[0]
    
    print e_star






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
    E_B, V, MR_inv = update_spanning_tree2(E_B, MR_inv, V, e_prime, e_star, fbar_T, fbar_X)
    #test MR_inv
#    correct_MR_inv = api.test_MR_inv(E_B, V)
#    print "MR_inv correct ->>>>>>", np.array_equal(MR_inv, correct_MR_inv)









#E_B, V, MR_inv = ([[(None, 4),
#   ((1, 2), None),
#   ((1, 3), None),
#   ((2, 3), None),
#   ((1, 4), None),
#   ((2, 4), None),
#   ((3, 4), None),
#   ((1, 5), None),
#   ((2, 5), None),
#   ((3, 5), None),
#   ((4, 5), None)],
#  [((3, 4), 5)]],
# [[5],
#  [4,
#   (1, 2),
#   (1, 3),
#   (2, 3),
#   (1, 4),
#   (2, 4),
#   (3, 4),
#   (1, 5),
#   (2, 5),
#   (3, 5),
#   (4, 5)]],
#np.array([[-1.]]))




E_T = E_B[0]
E_X = E_B[1]
R = V[0]
N = V[1]


notopt = True
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
#==============================================================================
#     gotta fix this shit, not all v in R should be -1 only 4,5,6..etc
#==============================================================================
    b_R = dict.fromkeys(V[0], 0)
    b_N = dict.fromkeys(V[1], 0)
    starting_b = [4,5,(1,2),(1,3),(2,3)]
    for v in starting_b:
        if v ==4 or v ==5:
            if v in N:      
                b_N[v] = -1
            if v in R:
                b_R[v]= -1
        else:
            if v in N:      
                b_N[v] = 1
            if v in R:
                b_R[v]= 1
    
    b_bar = [b_R, b_N]
    
    f_T, f_X = primal.Primal(V, E_B, MR_inv, b_bar)    
#    f_lp = api.lp_find_flow(E_B, V, 'default')
    f_pri = f_T.copy()
    f_pri.update(f_X)
    if len(f_pri) == len(E_B[0]+E_B[1]):
        print "--------- ----> True"
    else:
        print "errrrrrorrrr"
#    if f_pri == f_lp:
#        print "f_pri == f_lp ----> True"
#    else:
#        print "errrrrrorrrr"
        
    
    if len_violate == 0:        
        print "Terminate algorithm"
        calccost = api.calcCost(f_T,dist_dic)        
        print "cost is  ", calccost
        notopt = False
#        break
#        return len_violate, E_B, E_B_pre, e_star, e_prime
    
    else:
        minRC = float('inf')
    
        for e in violate:
            if violate[e] < minRC:
                minRC = violate[e]
                e_prime = e
    #   
        print "eprime", e_prime
 
        
        if e_prime[0] is None:
            print "errrrrorrrr", e_prime, " trying to go into basis"
           
        
        if e_prime[1] is None:
            temp_R = dict.fromkeys(V[0], 0)
            temp_N = dict.fromkeys(V[1], 0)
            if e_prime[0] in R:      
                temp_R[e_prime[0]] = -1         
            else:
                temp_N[e_prime[0]] = -1  
            temp_bar = [temp_R, temp_N]
        
        elif e_prime[1] is not None:
            if e_prime[0] is not None:
                ij = e_prime[0]
                k = e_prime[1]
                ik = (e_prime[0][0],e_prime[1])
                jk = (e_prime[0][1],e_prime[1])     
                temp_R = dict.fromkeys(V[0], 0)      
                temp_N = dict.fromkeys(V[1], 0)
                vset = [ij, ik, jk, k]            
                for v in vset:
                    if v in V[0]:
                        if v ==ij:
                            temp_R[v] = -1
                        else:
                            temp_R[v] = 1
                    if v in V[1]:
                        if v == ij:
                            temp_N[v] = -1
                        else:
                            temp_N[v] = 1
                
                temp_bar = [temp_R, temp_N]
        fbar_T, fbar_X = primal.Primal(V, E_B, MR_inv, temp_bar)  
        
        
#        f_lp = lp_find_flow(E_B, V, 'default')
#        fbar_lp = api.lp_find_flow(E_B, V, e_prime)
        fbar_pri = fbar_T.copy()
        fbar_pri.update(fbar_X)
        if len(fbar_pri) == len(E_B[0]+E_B[1]):
            print "--------- ----> True"
        else:
            print "errrrrrorrrr"
#        if fbar_pri == fbar_lp:
#            print "fbar_pri == fbar_lp ----> True"
#        else:
#            print "errrrrrorrrr"
            
            
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
                
#        correct_argmin = api.find_e_star(E_B, V, e_prime)
#        argmin_set_difference = correct_argmin.difference(set(argmin.keys()))  
#        if len(argmin_set_difference) != 0:
#            print "errror with argmin set"
#        else:
#            print "argmin set correct"
        
        
        e_star = None
        
        if len(argmin) == 0:
            e_star = e_prime
        
        else:
#            for e in argmin:
#                if e[1] is not None and e[1] == e_prime[1]:
#                    e_star = e
#            
#            if e_star == None:
            for e in argmin:
                if e[0] is None:
                    e_star = e
            
            if e_star is None:
            
                argminvalue = min(argmin.values())
            
        #        for e in argmin:
        #            if argmin[e] > argminvalue:
        #                argmin.pop(e)
                keys_to_remove = [key for key, value in argmin.iteritems()
                          if value > argminvalue]
                for key in keys_to_remove:
                    del argmin[key]
                e_star = argmin.popitem()[0]
        
        print e_star
        
                    
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
            E_B, V, MR_inv = update_spanning_tree2(E_B, MR_inv, V, e_prime, e_star, fbar_T, fbar_X)
            #test MR_inv
#            correct_MR_inv = api.test_MR_inv(E_B, V)
#            print "MR_inv correct ->>>>>>", np.array_equal(MR_inv, correct_MR_inv)
            E_B = oldE_B
            MR_inv = oldMR_inv
            V = oldV

        E_T = E_B[0]
        E_X = E_B[1]
        R = V[0]
        N = V[1]
        print "in ",e_prime, "  out ", e_star
        print " "







































