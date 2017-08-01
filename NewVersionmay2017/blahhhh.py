# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 15:12:21 2017

asdhfdsjfhdsajkfhladsfjadsf


test script


@author: Kun
"""
import api
import numpy as np
import random
import timeit
import newdualitseems as newdual
import primal


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

E_B = [{((1, 2), 5),
  ((1, 3), None),
  ((1, 4), None),
  ((1, 5), None),
  ((2, 3), 4),
  ((2, 4), None),
  ((2, 5), None),
  ((3, 4), None),
  ((3, 5), None),
  ((4, 5), None)},
 {((1, 3), 4), ((3, 4), 5)}]
 
e_prime = ((2, 3), None)

E_T = E_B[0]
E_X = E_B[1]

r = R+N
c = list(E_T) + list(E_X)
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

print np.linalg.det(M)

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
    
    
    
    
    
    
    
    
