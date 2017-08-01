import numpy as np

np.array([[1,1,1,1],
          [1,1,1,1],[1,1,1,1],[1,1,1,1]])
          
M = np.eye(4)
e_prime = np.array([0,0,0,1])

correct_rank = np.linalg.matrix_rank(M)

counter = 0
while counter<len(M):
    cols = range(len(M))    
    cols.remove(counter)
    M[:,cols]
    test_rank = np.linalg.matrix_rank(np.c_[M[:,cols],e_prime])
    if test_rank == correct_rank:
        print counter
        break
    counter+=1



#==============================================================================
# For bigger matrix to determine e_star
#==============================================================================

import api
import numpy as np
import random
import time

n = 7
V = api.makeVset(n)
R = V[0]
N = V[1]
dist_dic = {}
for v in N:
    dist_dic[v] = random.randint(10, 100)
    
E_B = [{((1, 2), None),
  ((1, 3), 4),
  ((1, 4), 5),
  ((1, 5), None),
  ((1, 6), None),
  ((1, 7), None),
  ((2, 3), 5),
  ((2, 4), 5),
  ((2, 5), None),
  ((2, 6), None),
  ((2, 7), None),
  ((3, 4), 5),
  ((3, 5), None),
  ((3, 6), None),
  ((3, 7), None),
  ((4, 5), 6),
  ((4, 6), None),
  ((4, 7), None),
  ((5, 6), None),
  ((5, 7), None),
  ((6, 7), None)},
 {((1, 2), 5), ((1, 5), 6), ((2, 3), 4), ((4, 5), 7)}]
 
e_prime = ((4, 6), 7)

#E_T = E_B[0]
#E_X = E_B[1]

def find_e_star(E_B, e_star):
    E_T = E_B[0]
    E_X = E_B[1]
    r = R+N
    c = list(E_T) + list(E_X)
    len_R = len(R)
    len_N = len(N)
    M = np.zeros([len_R+len_N,len_R+len_N])
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
    
    M_eprime = np.zeros(len_R+len_N)
    
    if e_prime[1] is None:
        ij = r.index(e_prime[0])
        M_eprime[ij] = 1
    else:
        ij = r.index(e_prime[0])
        k = r.index(e_prime[1])
        ik = r.index((e_prime[0][0],e_prime[1]))
        jk = r.index((e_prime[0][1],e_prime[1]))
        M_eprime[ij] = 1
        M_eprime[k] = -1
        M_eprime[ik] = -1
        M_eprime[jk] = -1
    
    
    correct_rank = np.linalg.matrix_rank(M)
    counter = 0
    while counter<(len_R+len_N):
        cols = range(len_R+len_N)    
        cols.remove(counter)
        M[:,cols]
        test_rank = np.linalg.matrix_rank(np.c_[M[:,cols],M_eprime])
        if test_rank == correct_rank:
            break
        counter+=1
    
    e_star = c[counter]
    return e_star





