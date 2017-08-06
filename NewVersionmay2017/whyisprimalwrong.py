# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 14:51:58 2017

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




M_R = np.zeros([len(E_X), len(E_X)], dtype='int')
E_X = list(E_X)
R = list(R)
for j in xrange(len(E_X)):
     i = R.index(E_X[j][1])
     M_R[i][j] = -1

MR_inv = np.linalg.inv(M_R)

MR_inv = np.array([[-1.,  0.,  0.],
       [ 0.,  0.,  1.],
       [ 0.,  1.,  1.]])



b_R = dict.fromkeys(V[0], -1)
b_N = dict.fromkeys(V[1], 0)
starting_b = [(1,2),(1,3),(2,3)]
for v in starting_b:
    if v in N:      
        b_N[v] = 1


b_bar = [b_R, b_N]

f_T, f_X = primal.Primal(V, E_B, MR_inv, b_bar)


#start = time.time()
r = R+N
c = list(E_T) + list(E_X)
#import numpy as np 
M = np.zeros([len(R)+len(N),len(R)+len(N)])
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



b = np.zeros(len(r), dtype='int')
for i in range(len(r)):
    if r[i] in R:
        b[i] = -1
    elif r[i] == (1,2) or r[i] == (1,3) or r[i] == (2,3):
        b[i] = 1
    else:
        b[i] = 0
invM = np.linalg.inv(M)
f = np.dot(invM,b)
#end = time.time()
#print end-start

f_lp = {}
for i in range(len(f)):
    f_lp[c[i]] = f[i]

f_pri = f_T.copy()
f_pri.update(f_X)

f_pri == f_lp



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

pi_dl = pi_R.copy()
pi_dl.update(pi_N)

pi_dl == pi_lp

pi_dl = pi_lp
















#for i in pi_lp:
#    if pi_lp[i] != pi_dl[i]:
#        print i, pi_lp[i],  pi_dl[i]








      
    