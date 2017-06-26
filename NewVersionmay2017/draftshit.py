# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 12:51:08 2017

@author: Kun
"""



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


b = np.zeros(len(r))
for i in range(len(r)):
    if r[i] in R:
        b[i] = -1
    elif r[i] == (1,2) or r[i] == (1,3) or r[i] == (2,3):
        b[i] = 1
    else:
        b[i] = 0

f = np.dot(np.linalg.inv(M),b)

brhs = np.zeros(len(r))
for i in range(len(r)):
    if r[i] == (3, 4):
        brhs[i] = -1
#    elif r[i] == (2, 5) or r[i] == (4, 5) or r[i] == 5:
#        brhs[i] = 1

fbarr = np.dot(np.linalg.inv(M),brhs)
costv = np.zeros(len(c))
for j in range(len(c)):
    if c[j][1] is None:
        costv[j] = dist_dic[c[j][0]]
    else:
        costv[j] = 0

pi = np.dot(costv, np.linalg.inv(M))



ft_bar = {((1, 2), None): 0,
         ((1, 3), None): 0,
         ((1, 4), None): -1,
         ((1, 5), None): 1,
         ((2, 3), 4): 0,
         ((2, 4), None): 1,
         ((2, 5), None): -1,
         ((3, 4), 5): 0,
         ((3, 5), None): 0,
         ((4, 5), None): 0}
         
fx_bar = {((1, 3), 4): 0, ((2, 4), 5): -1}


pi_R = {4: -36, 5: -32.0}

pi_N = {(1, 2): 30,
         (1, 3): 26,
         (1, 4): 38,
         (1, 5): 40,
         (2, 3): 28,
         (2, 4): 40,
         (2, 5): 50,
         (3, 4): 24,
         (3, 5): 26,
         (4, 5): 30}
 
 
e_leaving = ((1, 4), None)
e_prime = ((3, 4), None)

E_T.remove(e_leaving)
E_T.add(e_prime)
