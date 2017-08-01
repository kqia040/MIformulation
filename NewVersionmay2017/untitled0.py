# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 13:30:31 2017

@author: Kun
"""
import random

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
    
P = {((1, 2), 5), ((1, 3), 4)}
n = 5
P_0 = set()
for i in P:
    P_0.add(i[0])



def extendbasis2(n, P):
    count = 4
    templist = []
    E_X = set()
    P_0 = set()
    for i in P:
        P_0.add(i[0])
        
    for j in range(2,n+1):
        for i in range(1,j):
            if len(templist) < n-3:
                if i<j and (i,j) not in P_0:
                    templist.append((i,j))

    for v in templist:
        E_X.add(((v),count))
        count+=1
    
    


    return E_X
                
E_X = extendbasis2(n, P)
print E_X