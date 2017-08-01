# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 11:29:01 2017

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

E_T, P = api.makeE_Tset(n)
E_X = api.extendbasis(n, P)

#==============================================================================
# 
#
#
## script is below
#
#
##
#
#==============================================================================




E = api.makeE_set(n)
E_B = [E_T, E_X]
E_NB = E-E_T-set(E_X)        
f_NB = dict.fromkeys(E_NB, 0)
#f_NB[((1,3),None)] =1
#f_NB[((2,3),None)] =1
#f_NB[((2,3),5)] =1
r = R+N
c = list(E_T) + list(E_X)
M = np.zeros([len(R)+len(N),len(R)+len(N)])
M = np.zeros([12,12])


for cc in range(len(c)):
    if c[cc][1] is None:
        ij = r.index(c[cc][0])
        M[ij][cc] = 1
    else:
        ij = r.index(c[cc][0])
        k = r.index(c[cc][1])
        ik = r.index((c[cc][0][0],c[cc][1]))
        jk = r.index((c[cc][0][1],c[cc][1]))
        M[ij][cc] = 1
        M[k][cc] = -1
        M[ik][cc] = -1
        M[jk][cc] = -1


b = np.zeros(len(r))
for i in range(len(r)):
    if r[i] in R:
        b[i] = -1
    elif r[i] == (1,2) or r[i] == (1,3) or r[i] == (2,3):
        b[i] = 1
    else:
        b[i] = 0

f = np.dot(np.linalg.inv(M),b)


f_lp = {}
for i in range(len(f)):
    f_lp[c[i]] = f[i]
    
f_T = {}
f_X = {}

for e in f_lp:
    if e in E_T:
        f_T[e] = f_lp[e]
    elif e in E_X:
        f_X[e] = f_lp[e]
    
costv = np.zeros(len(c))
for j in range(len(c)):
    if c[j][1] is None:
        costv[j] = dist_dic[c[j][0]]
    else:
        costv[j] = 0

pi = np.dot(costv, np.linalg.inv(M))


pi_lp = {}
for i in range(len(pi)):
    pi_lp[r[i]] = pi[i]

pi_N = {}
pi_R = {}

for v in pi_lp:
    if v in N:
        pi_N[v] = pi_lp[v]
    elif v in R:
        pi_R[v] = pi_lp[v]



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
    
    
costRHS = np.zeros(len(r))
    
for j in range(len(r)):
    v_head = e_prime[0]
    
    if e_prime[1] is not None:
        v_tail = [(e_prime[0][0],e_prime[1]), (e_prime[0][1],e_prime[1]), e_prime[1]]
    else:
        v_tail = None
    
    if v_tail is None:
        costRHS[r.index(v_head)] = -1     
    else:
        costRHS[r.index(v_head)] = -1         
        costRHS[r.index(v_tail[0])] = 1  
        costRHS[r.index(v_tail[1])] = 1
        costRHS[r.index(v_tail[2])] = 1


fbar = np.dot(np.linalg.inv(M),costRHS)


fbar_lp = {}
for i in range(len(f)):
    fbar_lp[c[i]] = fbar[i]
    
fbar_T = {}
fbar_X = {}

for e in fbar_lp:
    if e in E_T:
        fbar_T[e] = fbar_lp[e]
    elif e in E_X:
        fbar_X[e] = fbar_lp[e]


#==============================================================================
# calculate s vector
#==============================================================================

s = {}

for e in f_T:
    if fbar_T[e] > 0:
        s[e] = (1-f_T[e])/fbar_T[e]
    elif fbar_T[e] < 0:
        s[e] = f_T[e]/(-fbar_T[e])
    elif fbar_T[e] == 0:
        s[e] = 0
    
for e in f_X:
    if fbar_X[e] > 0:
        s[e] = (1-f_X[e])/fbar_X[e]
    elif fbar_X[e] < 0:
        s[e] = f_X[e]/(-fbar_X[e])
    elif fbar_X[e] == 0:
        s[e] = 0

argminsetchoice = {}

for e in s:
    if e in f_T and fbar_T[e] != 0:
        argminsetchoice[e] = s[e]
    elif e in f_X and fbar_X[e] != 0:
        argminsetchoice[e] = s[e]

#print argminsetchoice

argminset = {}
minval = float('inf')
mincount = 0
for e in argminsetchoice:
    if argminsetchoice[e] < minval:
        minval = argminsetchoice[e]
        mincount = 1
        argminset = {}
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
            f_prime[e] = f_T[e] + fbar_T[e]*s[e_prime]
        elif e in f_X:
            f_prime[e] = f_X[e] + fbar_X[e]*s[e_prime]
    
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
    if e_leaving in E_X:
        f_NB[e_leaving] = f_X[e_leaving]        
        E_X[E_X.index(e_leaving)] = e_prime
    elif e_leaving in E_T:
        f_NB[e_leaving] = f_T[e_leaving]
        E_T.remove(e_leaving)
        E_T.add(e_prime)
    f_NB.pop(e_prime)
