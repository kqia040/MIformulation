# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 18:22:48 2017

MI 5 city example test

@author: Kun
"""
import api
import numpy as np
import primal as primal
import dual as dual

n = 5
V = api.makeVset(n)
R = V[0]
N = V[1]

#optimal Pedigree
#P = {((1, 3), 4), ((1, 4), 5)}
P = {((1, 2), 5), ((1, 3), 4)}
#e_x for the optimal P
#E_X = {((2, 3), 4), ((2, 3), 5)}
E_X = {((2, 3), 4), ((1, 4), 5)}
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

E_T = {((1, 2), 5), 
       ((1, 3), 4),
        ((1,4),None),
        ((3,4),None),
        ((1,5),None),
        ((2,5),None),
        ((2,3),None),
        ((2,4),None),
        ((3,5),None),
        ((4,5),None)}

E = api.makeE_set(n)
E_B = [E_T, E_X]
E_NB = E-E_T-E_X          


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

pi_R, pi_N, c_X = dual.dual(V, E_B, E_NB, MR_inv, c_bar)


f_NB = dict.fromkeys(E_NB, 0)

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

#get most negative
e_prime = min(violate)
rhs_R = dict.fromkeys(V[0], 0)
rhs_N = dict.fromkeys(V[1], 0)
v_head = e_prime[0]
if e_prime[1] is not None:
    v_tail = [(e_prime[0][0],e_prime[1]), (e_prime[0][1],e_prime[1]), e_prime[1]]
else:
    v_tail = None

if v_tail is None:
    rhs_N[v_head] = -1
else:
    rhs_N[v_head] = -1
    rhs_N[v_tail[0]] = 1
    rhs_N[v_tail[1]] = 1
    rhs_R[v_tail[2]] = 1



rhs_bar = [rhs_R, rhs_N]

ft_bar, fx_bar, rhsbbar = primal.Primal(V, E_B, MR_inv, rhs_bar)

violate = {}

f_NB[e_prime] = 1

for e in f_NB:
    if f_NB[e] == 0 and reduced_cost[e] < 0:
        violate[e] = reduced_cost[e]
    
    elif f_NB[e] == 1 and reduced_cost[e] > 0:
        violate[e] = reduced_cost[e]

print violate



#get most negative
e_prime = min(violate)
rhs_R = dict.fromkeys(V[0], 0)
rhs_N = dict.fromkeys(V[1], 0)
v_head = e_prime[0]
if e_prime[1] is not None:
    v_tail = [(e_prime[0][0],e_prime[1]), (e_prime[0][1],e_prime[1]), e_prime[1]]
else:
    v_tail = None

if v_tail is None:
    rhs_N[v_head] = -1
else:
    rhs_N[v_head] = -1
    rhs_N[v_tail[0]] = 1
    rhs_N[v_tail[1]] = 1
    rhs_R[v_tail[2]] = 1



rhs_bar = [rhs_R, rhs_N]

ft_bar, fx_bar, rhsbbar = primal.Primal(V, E_B, MR_inv, rhs_bar)


#I know that i can get rid of 234 and put in 124 and it'll give optimal solution, 
#but im gonna test leaving 230

#==============================================================================
# Basis change beloww
#==============================================================================


e_leaving = ((2,3), 4)
E_X.remove(e_leaving)
E_X.add(e_prime)
E_NB.remove(e_prime)
E_NB.add(e_leaving)
f_NB.pop(e_prime)
f_NB[e_leaving] = f_X[e_leaving]

E_B[1] = E_X
f_tt, f_xx, bbbbar = primal.Primal(V, E_B, MR_inv, b_bar)

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

pi_rr, pi_nn, temp = dual.dual(V, E_B, E_NB, MR_inv, c_bar)

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
        temp = pi_nn[(e[0][0],e[1])] + pi_nn[(e[0][1],e[1])] + pi_rr[e[1]]      
        reduced_cost[e] = c_e  + temp - pi_nn[e[0]]
    else:
        reduced_cost[e] = c_e - pi_nn[e[0]]


violate = {}

for e in f_NB:
    if f_NB[e] == 0 and reduced_cost[e] < 0:
        violate[e] = reduced_cost[e]
    
    elif f_NB[e] == 1 and reduced_cost[e] > 0:
        violate[e] = reduced_cost[e]

print violate




e_prime = min(violate)
rhs_R = dict.fromkeys(V[0], 0)
rhs_N = dict.fromkeys(V[1], 0)
v_head = e_prime[0]
if e_prime[1] is not None:
    v_tail = [(e_prime[0][0],e_prime[1]), (e_prime[0][1],e_prime[1]), e_prime[1]]
else:
    v_tail = None

if v_tail is None:
    rhs_N[v_head] = -1
else:
    rhs_N[v_head] = -1
    rhs_N[v_tail[0]] = 1
    rhs_N[v_tail[1]] = 1
    rhs_R[v_tail[2]] = 1



rhs_bar = [rhs_R, rhs_N]

fttt_bar, fxxx_bar, rhsbbar = primal.Primal(V, E_B, MR_inv, rhs_bar)



#==============================================================================
# when 130 gets added to the basis, it can only go into the ex
#==============================================================================


