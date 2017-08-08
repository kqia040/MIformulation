# -*- coding: utf-8 -*-
"""
Created on Tue Aug 01 15:43:10 2017

@author: Kun
"""
E_T, E_X, P = api.makeE_B(n,N)
E_B = [E_T, E_X]


E = api.makeE_set(n)
E_NB = E-E_T-set(E_X)

M_R = np.zeros([len(E_X), len(E_X)], dtype='int')
E_X = list(E_X)
R = list(R)

for j in xrange(len(E_X)):
    i = R.index(E_X[j][1])
    M_R[i][j] = -1

MR_inv = np.linalg.inv(M_R)

for e_prime in E_NB:    
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
    fbar_pri = fbar_T.copy()
    fbar_pri.update(fbar_X)
    fbar_lp = lp_find_flow(E_B, V, e_prime)
    print "for edge ", e_prime, "working boolean is ",  fbar_pri == fbar_lp
    
    for e in fbar_pri:
        if fbar_pri[e]!=fbar_lp[e]:
            print e, fbar_pri[e],  fbar_lp[e] 
    
e_star_list = find_e_star(E_B, e_prime)
wrong= set()
for e in e_star_list:
    if e not in argmin:
        wrong.add(e)
    
for e in argmin:
    if e not in e_star_list:
        wrong.add(e)

print wrong
if len(wrong) ==0:
    print "wrong set is empty"
    
    
    
    
    
    
for e in E_NB:
    print e
    print find_e_star(E_B, e)
    print ""
    
    
import numpy as np 
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


rows = range(0,2)
cols = range(0,10)
B = M[rows][:,cols]
    
rows = range(2,12)
cols = range(0,10)
U = M[rows][:,cols]

rows = range(0,2)
cols = range(10,12)
C = M[rows][:,cols]


rows = range(2,12)
cols = range(10,12)
D = M[rows][:,cols]

MR11 = C - np.dot(np.dot(B,np.linalg.inv(U)),D)
MR_inv11 = np.linalg.inv(MR11)
print MR_inv11

b_R = np.array([0,0])
b_N = np.zeros(len(N))
for i in range(len(N)):
    if N[i] == (1,2):
        b_N[i] = -1


externalflow = np.dot(MR_inv,(b_R-np.dot(np.dot(B,np.linalg.inv(U)),b_N)))

        














