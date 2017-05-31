# -*- coding: utf-8 -*-
"""
Created on Tue May 02 10:57:12 2017

new flow

@author: Kun
"""

"""
First call, f_X is all 0
"""

"""
Flowwww testing

Input variables = V, E_T, d_N, f_X, b_bar

"""
def flow(V, E_T, E_X, d_N, f_X, b_bar):
    f_T = {}
    R = V[0]
    N = V[1]
    d_R = {}
    
    for v in R:
        d_R[v] = 0
        
    d_N.update(d_R)
    
    d = d_N
    #for e in E_X that looks like ijk 
    #i = e[0][0]
    #j = e[0][1]
    #k = e[1]
    for e in E_X:
#        if e[1] is None:
#            #d[(i,j)] = d[(i,j)] - f_X[e]
#            d[(e[0][0],e[0][1])] = d[(e[0][0],e[0][1])] - f_X[e]
#        else:
    #        d[(i,k)] = d[(i,k)] + f_X[e]
    #        d[(j,k)] = d[(j,k)] + f_X[e]
    #        d[(k)] = d[(k)] + f_X[e]
    #        d[(i,j)] = d[(i,j)] - f_X[e]
            d[(e[0][0],e[1])] = d[(e[0][0],e[1])] + f_X[e]
            d[(e[0][1],e[1])] = d[(e[0][1],e[1])] + f_X[e]
            d[(e[1])] = d[(e[1])] + f_X[e]
            d[(e[0][0],e[0][1])] = d[(e[0][0],e[0][1])] - f_X[e]
            
    
    unvisitedcount = dict.fromkeys(R, 0)
    unvisitedcount.update(dict.fromkeys(N, 0))               
    
    #==============================================================================
    # """
    # The below might be incorrect, based on the Pedigree
    # 
    # """
    #==============================================================================
    
    for v in Pedigree:
        unvisitedcount[v] = 1
    for v in slackvar:
        unvisitedcount[v] = 1
    
    #==============================================================================
    # 
    # """
    # Need to fix the function that creates the leaves queue
    # 
    # Leaves are all ik, jks in Xijk that is not in P. I think i've done it
    # 
    # """
    # 
    #==============================================================================
    
    #Q = []
    #the below code is wrong for leaf calculation
    #for v in unvisitedcount:
    #    if unvisitedcount[v] == 1:
    #        Q.append(v)
    
    
    #Incorrect find leaves I have it wrong with he and Te  = []
    for e in P:
        if (e[0][0], e[1]) not in Pedigree:
            Q.append((e[0][0], e[1]))
        
        if (e[0][1], e[1]) not in Pedigree:
            Q.append((e[0][1], e[1]))
    
    
    while Q:
        v_curr = Q.pop(0)
    #might throw error in the below loop    
        for e in E_T:
            if e[0] == v_curr:
                e_v = e            
                break
            elif (e[0][0], e[1]) == v_curr:
                e_v = (e[0][0], e[1])
                break
            elif (e[0][1], e[1]) == v_curr:
                e_v = (e[0][1], e[1])
                break
            
    
    
        if (v_curr != e_v):
            f_T[e_v] = d[v_curr]
        else:
            f_T[e_v] = -d[v_curr]
    
    #==============================================================================
    # """
    # line 22 of my code, when does v != i'j'
    # hmmm might be all possible combinations of some sort
    # 
    # """   
    #         
    # """
    # for w in (T_e_v U {h_e_v}) \ {v}
    # 
    # """
    #==============================================================================
    
    #==============================================================================
    #     ij = e_v[0]
    #     ik = (e_v[0][0], e_v[1])
    #     jk = (e_v[0][1], e_v[1])
    #     k = e_v[1]
    #     
    #==============================================================================
    
    
        
        W_nodes = set(e_v[0], (e_v[0][0], e_v[1]), (e_v[0][1], e_v[1]), e_v[1])
        for w in W_nodes:
            if w == v:
                continue
            else:
                if w == e_v[0]:
                    d[w] = d[w] - f_T[e_v]
                else:
                    d[w] = d[w] + f_T[e_v]
            
            unvisitedcount[w] = unvisitedcount[w] - 1
            if  unvisitedcount[w] ==1 and w not in R:
                Q.append(w)
        for v in R:
            d[v] = -d[v]
            
        for v in d:
            if v in R:
                d_R[v] = d[v]
        
    #==============================================================================
    # """
    # Idk if i need the following code to update the demand for d_N
    # Coz we don't return d_N
    # """
    #==============================================================================
        for v in N:
            d[v] = -d[v]
    
    return d_R, f_T