# -*- coding: utf-8 -*-
"""
Created on Fri Apr 07 13:38:14 2017
Play scripting
@author: Kun
"""



import random
def get_pedigree(n):
	#R = set([range(4,n+1)])
    N = set(((1,2),(1,3),(2,3)))
    P = set()
    for i in xrange(4, n+1):
        random_node = random.sample(N,1)
        P.add((random_node[0], i))
        if i > random_node[0][0]:
            nodeInsert1 = (random_node[0][0], i)
        else:
            nodeInsert1 = (i, random_node[0][0])

        if i > random_node[0][1]:
            nodeInsert2 = (random_node[0][1], i)
        else:
            nodeInsert2 = (i, random_node[0][1])
        N.add(nodeInsert1)
        N.add(nodeInsert2)
        N.remove(random_node[0])
    return P, N
    
n = 6
P,N_0 = get_pedigree(n)

#P is the Pedigree
#N is the nodes inserted
#need to get the slack variables


#R = set(range(4,n+1))
#N.update(P)
#N.update(R)
#
#
def get_slack(P, N, n):
    slack_set = set()

    for j in range(2,n+1):
        for i in range(1, n):
            if i<j and (i,j) not in N and (i,j) not in Pdummy:
                slack_set.add((i, j))
    return slack_set


Pdummy = set()
for item in P:
    Pdummy.add(item[0])
s = get_slack(Pdummy, N, 6)

"""
Creating the v set

"""


v = set(range(4,n+1))
#v.update(P)
v.update(N)
v.update(s)

for i in P:
    v.add(i[0])




E_T = set()
E_T.update(P)
for i in N:
    E_T.add((i, None))


for i in s:
    E_T.add((i, None))
    
#E_X = set()
#for i in set(range(4,n+1)):
#    E_X.add((i, None))


"""

Build edge set

"""


n = 6
M_R_size = n - 3 
Xijk = set()

"""
All xijk edges
"""

for k in range(4,4+M_R_size):
    for j in range(2,4+M_R_size):
            for i in range(1,j):
                if i<j and j<k:
                    print ((i,j,k))

"""
uij edges

"""

Uij = set()
for j in range(2,4+M_R_size):
        for i in range(1,j):
            if i<j:
                Uij.add((i,j,None))
























