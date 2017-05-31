# -*- coding: utf-8 -*-
"""
Created on Tue May 02 10:50:18 2017

@author: Kun
"""

#trailpy

import random
def makeVset(n):
    N = set()
    for j in range(2,n+1):
            for i in range(1,j):
                if i<j:
                    N.add((i,j))
    
    R = set(range(4,n+1))
    return [R, N]


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
    

def get_slack(P_0, N, n):
    slack_set = set()
    for j in range(2,n+1):
        for i in range(1, n):
            if i<j and (i,j) not in N and (i,j) not in P_0:
                slack_set.add((i, j))
    return slack_set

def makeE_Tset(n):
    Pdummy = set()
    P, N = get_pedigree(n)
    for item in P:
        Pdummy.add(item[0])
    s = get_slack(Pdummy, N, n)
    E_T = set()
    E_T.update(P)
    for i in N:
        E_T.add((i, None))
    for i in s:
        E_T.add((i, None))
        
        
    
    return E_T, s, Pdummy, P
    
#this needs to be fixed
    
"""
THIS NEEDS TO BE FIXED

This does not consider all E

All e needs to include the Uij set as well

E = Xijk U uij

WILL WORK FOR NOW I GUESS
"""
def makeE_Xset(n, E_T, P):
    E_X = set()
    kth = set()
    ijth = set()
    for k in range(4,n+1):
        for j in range(2,n+1):
                for i in range(1,j):
                    if i<j and j<k:
                        if ((i,j),k) not in E_T and (i,j) not in P:
                            if len(E_X) < n - 3:
                                if k in kth:
                                    continue
                                else:
                                    if (i,j) in ijth:
                                        continue
                                    else:
                                        E_X.add(((i,j),k))
                                        kth.add(k)
                                        ijth.add((i,j))
                                        break
                            else:
                                return E_X
