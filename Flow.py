# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:07:55 2017

Flow


@author: Kun
"""

"""

Input: H = (V, E)
T_r 
d(N)
f(X) 

output: d(R), f(T)

"""
#need this f(e) this floww on edges of e(X)
def flow(V, E_T, E_X, d_N, f_X):
    R = V[0] #sets 
    N = V[1] #sets   
    d = {}
    f_T={}
    for v in R:
        d[v] = 0
    for e in E_X:
        k = e[0] 
        i,j = e[1]        
        if k != None:        
            d[(i,k)] = d[(i,k)] + f_X[e] #k component e[0] is a v
            d[(j,k)] = d[(j,k)] + f_X[e]
            d[(k)] = d[(k)] + f_X[e]
            d[(i,j)] = d[(i,j)] - f_X[e]
        elif k == None:
            d[(i,j)] = d[(i,j)] - f_X[e]

    incident = {}    
    for v in V:
        ###calculate number of hyperarcs incident to V
        incident[v] = calculateNumberIncidentEdges(v)
    
    queue = []
    """
    The incident thing below is wrong
    "a leaf" = any non root node v, not contained in tail of any
    hyperarc of T_R is a leaf.
    
    """
    leaf = getleaf(V, E_T,E_X)
    for v in leaf:
    #if leaf need to check this
        queue.append(v)
    
    
    while len(queue)!=0:
        v = queue.pop(0) #pop from queue
        k_prime,i_prime, j_prime = None, None, None
        #redefine this        
        #need to run loop of some sort        

        """
        let v in N, let e_v = the unique hyperarc incident to v
        on the unique hyperpath from R to v
        
        so aka, this is the arc that is going into v?
        There should only be ONE arc going into a node
        
        so e_v should be in E_T which is in T_R
            
        e_v = [k_prime,[i_prime, j_prime]]
        is the unique hyperarc that is incident to v, 
        
        """
        #e_v = the edge going into v
        e_v = [k_prime,[i_prime, j_prime]] #what is this lol
        
        #if v = ij then do ...
        #else if v = k then do...
        
        if v == (i_prime, j_prime):
            f_T[e_v] = d[v]
        else:
            f_T[e_v] = -d[v]
            
        V_set = R.union(N) 
        for w in V.difference(v):
            if w == (i_prime, j_prime):
                d[w] = d[w] - f_T[e_v]
            else:
                d[w] = d[w] + f_T[e_v]
            
            incident[v]-=1
            if incident[v] ==1 and w not in R:
                queue.append(w)
    
    for v in V:
        d[v] = -d[v]
    
    return d, f
            
def calculateNumberIncidentEdges():
    pass
    
    
    
    
def getleaf(V, E_T,E_X):
    pass
    
    
    
    
    
    
    
    
    
    