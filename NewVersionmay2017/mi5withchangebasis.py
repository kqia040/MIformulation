# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:00:53 2017

Mi5 city where we need to change basis to get optimal sol


@author: Kun
"""

import api
import numpy as np
import primal as primal
import dual as dual

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

P = {((3, 4), 5), ((2, 3), 4)}
#e_x for the optimal P
#E_X = {((2, 3), 4), ((2, 3), 5)}
E_X = {((1, 2), 4), ((2, 4), 5)}

E_T = {((3, 4), 5), 
       ((2, 3), 4),
        ((1,4),None),
        ((1,2),None),
        ((1,5),None),
        ((2,5),None),
        ((1,3),None),
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
minRC = float('inf')
for e in violate:
    if violate[e] < minRC:
        minRC = violate[e]
        e_prime = e
    
    
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

#==============================================================================
# calculate s vector
#==============================================================================

s = {}

for e in f_T:
    if ft_bar[e] > 0:
        s[e] = (1-f_T[e])/ft_bar[e]
    elif ft_bar[e] < 0:
        s[e] = f_T[e]/(-ft_bar[e])
    elif ft_bar[e] == 0:
        s[e] = 0
    
for e in f_X:
    if fx_bar[e] > 0:
        s[e] = (1-f_X[e])/fx_bar[e]
    elif fx_bar[e] < 0:
        s[e] = f_X[e]/(-fx_bar[e])
    elif fx_bar[e] == 0:
        s[e] = 0

argminsetchoice = {}

for e in s:
    if e in f_T and ft_bar[e] != 0:
        argminsetchoice[e] = s[e]
    elif e in f_X and fx_bar[e] != 0:
        argminsetchoice[e] = s[e]

print argminsetchoice

argminset = {}
minval = float('inf')
mincount = 0
for e in argminsetchoice:
    if argminsetchoice[e] < minval:
        minval = argminsetchoice[e]
        mincount = 1
        argminset[e] = argminsetchoice[e]
    elif argminsetchoice[e] == minval:
        mincount +=1
        argminset[e] = argminsetchoice[e]

print argminset
s[e_prime] = 1

f_prime = {}

if s[e_prime] == minval:
    #then carry out this action
    for e in s:
        if e == e_prime:
            f_prime[e] = f_NB[e] + s[e_prime]
        elif e in f_T:
            f_prime[e] = f_T[e] + ft_bar[e]*s[e_prime]
        elif e in f_X:
            f_prime[e] = f_X[e] + fx_bar[e]*s[e_prime]
    
    print "we have the optimal solution"
    solution = set()    
    for e in f_prime:
        if e[1] is not None and f_prime[e] == 1:
            solution.add(e)
else:
    #basis change
    #assumption, all xijk part of argminset will be part of E_X and not E_T
    pivotrootnode = e_prime[1]
    temp = dict((key,value) for key, value in argminset.iteritems() if key[1] == pivotrootnode)
    templist = list(temp)
    if len(templist) < 1:
        print "error in basis change, there is xijk available to leave the basis"
    else:
        e_leaving = templist[0]
        
    E_NB.add(e_leaving)
    E_NB.remove(e_prime)
    #this is where the assumption above that all leavinng edges are in f_X    
    #this assumption is probably wrong

    #assumption not true    
    f_NB[e_leaving] = f_X[e_leaving]
    f_NB.pop(e_prime)
    #this way M_R doesnt change.... given assumption holds... need to check for MI6 and MI7
    E_X[E_X.index(e_leaving)] = e_prime

    
E_B=[E_T,set(E_X)]
f_T, f_X, bbarN = primal.Primal(V, E_B, MR_inv, b_bar)

#this code needs to be repeated coz the c vector changes
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
    




























#r = R+N
#c = list(E_T) + list(E_X)
#M = np.zeros([len(R)+len(N),len(R)+len(N)])
#
#for cc in range(len(c)):
#    if c[cc][1] is None:
#        ij = r.index(c[cc][0])
#        M[ij][cc] = 1
#    else:
#        ij = r.index(c[cc][0])
#        k = r.index(c[cc][1])
#        ik = r.index((c[cc][0][0],c[cc][1]))
#        jk = r.index((c[cc][0][1],c[cc][1]))
#        M[ij][cc] = 1
#        M[k][cc] = -1
#        M[ik][cc] = -1
#        M[jk][cc] = -1
#
#
#b = np.zeros(len(r))
#for i in range(len(r)):
#    if r[i] in R:
#        b[i] = -1
#    elif r[i] == (1,2) or r[i] == (1,3) or r[i] == (2,3):
#        b[i] = 1
#    else:
#        b[i] = 0
#
#f = np.dot(np.linalg.inv(M),b)
#
#costv = np.zeros(len(c))
#for j in range(len(c)):
#    if c[j][1] is None:
#        costv[j] = dist_dic[c[j][0]]
#    else:
#        costv[j] = 0
#
#pi = np.dot(costv, np.linalg.inv(M))







  