# -*- coding: utf-8 -*-
"""
Created on Tue May 02 10:56:06 2017

This is going to be the api that makes the sets and stuff

@author: Kun
"""

import random
#this returns a list of sets
#def makeVset(n):
#    N = set()
#    for j in range(2,n+1):
#            for i in range(1,j):
#                if i<j:
#                    N.add((i,j))
#    
#    R = set(range(4,n+1))
#    return [R, N]


#return list of lists
def makeVset(n):
    N = []
    for j in range(2,n+1):
            for i in range(1,j):
                if i<j:
                    N.append((i,j))
    
    R = range(4,n+1)
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
        
        
    
    return E_T, P
#, s, Pdummy, P
    
#this needs to be fixed
    
"""
THIS NEEDS TO BE FIXED

Sometimes len(MR) is 2 and NOT 3
WILL WORK FOR NOW I GUESS
"""
def makeE_Xset(n, E_T, P):
    M_R = set()
    kth = set()
    ijth = set()
    for k in range(4,n+1):
        for j in range(2,n+1):
                for i in range(1,j):
                    if i<j and j<k:
                        if ((i,j),k) not in E_T and (i,j) not in P:
                            if len(M_R) < n - 3:
                                if k in kth:
                                    continue
                                else:
                                    if (i,j) in ijth:
                                        continue
                                    else:
                                        M_R.add(((i,j),k))
                                        kth.add(k)
                                        ijth.add((i,j))
                                        break
                            else:
                                return M_R

    return M_R


#Don;t need to add the Uij coz thats part of E_T deffs
def makeE_set(n):
    E = set()
    for k in range(4,n+1):
        for j in range(2,n+1):
                for i in range(1,j):
                    if i<j and j<k:
                        E.add(((i,j),k))

#    for j in range(2,n+1):
#        for i in range(1, n):
#            if i<j:
#                E.add(((i, j), None))    
    
    return E

def extendbasis(n, P):
    xijk = set()
    E_X = set()    
    for k in range(4,n+1):
        for j in range(2,n+1):
                for i in range(1,j):
                    if i<j and j<k:
                        xijk.add(((i,j),k))
    
    E_X_candidate = xijk - P
    for counter in xrange(4, n+1):
        temp = set()
        for e in E_X_candidate:
            if e[1] == counter:
                temp.add(e)
        randomedge = random.sample(temp, 1)
        E_X.add(randomedge[0])
    
    return E_X
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
