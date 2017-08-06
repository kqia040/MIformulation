# -*- coding: utf-8 -*-
"""
Created on Tue May 16 11:55:30 2017

Test flow


@author: Kun
"""

#our notation is going to change
#E = E_B union E_N are basic and non basic edges, which refer to as E_T and E_X
#E_T and E_X are part of E_B, where |E_X| = |R|


def flow(V, E_B, f_X, d_N):
    R = V[0]
    N = V[1]
    f_T = {}
    #demand dictionary of nodes    
    d = {}
    E_X = E_B[1]
    E_T = E_B[0]
    d.update(d_N)
    for v in R:
        d[v] = 0
        
    #need to fix this so that we dont need to store E_X in memory
    #shouldnt f_X be all 0? because there is no flow on external arcs
    #below hsould be E_X and not E_NB
    for e in E_X:
        #tail set
        if e[1] is None:
            d[e[0]] = d[e[0]] - f_X[e]
        else:
            d[(e[0][0],e[1])] = d[(e[0][0],e[1])] + f_X[e]
            d[(e[0][1],e[1])] = d[(e[0][1],e[1])] + f_X[e]
            d[(e[1])] = d[(e[1])] + f_X[e]
            #head
            d[(e[0][0],e[0][1])] = d[(e[0][0],e[0][1])] - f_X[e]

    unvisitedcount = dict.fromkeys(R, 0)
    unvisitedcount.update(dict.fromkeys(N, 0))     
    
    #for v in V, unvisited(v) = number of hyperarcs of T_R incident to v
    #tail set
    tail_set = set()
    #here should be E_T instead of E_B    
    for e in E_T:
        if e[1] is None:
            unvisitedcount[e[0]] += 1
        else:
            #ij
            unvisitedcount[e[0]] += 1
            #k            
            unvisitedcount[e[1]] += 1
            tail_set.add(e[1])             
            #i,k            
            unvisitedcount[(e[0][0],e[1])] +=1
            tail_set.add((e[0][0],e[1]))            
            #j,k            
            unvisitedcount[(e[0][1],e[1])] +=1
            tail_set.add((e[0][1],e[1])) 
        
    Queue = []    
    #leaf: non root node that is not in a tail set of any e in T_R
    #great!    
#    print unvisitedcount
    for v in N:
        if v not in tail_set:
            Queue.append(v)
        
#    print Queue        
        
    while Queue:
        v_curr = Queue.pop(0) 
#        print v_curr
        for e in E_T:
            if e[0] == v_curr:
                e_v = e
        #need to handle error better
        
            
#        print e_v
        ij = e_v[0]
        k = e_v[1]        
        ik = (e_v[0][0],e_v[1])
        jk = (e_v[0][1],e_v[1])
        
        f_T[e_v] = d[v_curr]
#        if v_curr == ij:
#            f_T[e_v] = d[v_curr]
#        else:
#            f_T[e_v] = -d[v_curr]
        
        
        if e_v[1] is not None:
            w_list = [ij, k, ik, jk]
        else:
            w_list = [ij]
#        print w_list
        #or if v_curr in w_list: remove
        if v_curr in w_list:
            w_list.remove(v_curr)
#        print w_list
#        if w_list is None:
#            print "w_list is None, wtf"
        for w in w_list:
            if w is not None:
                if w == ij:
                    d[w] = d[w] - f_T[e_v]
                else:
                    d[w] = d[w] + f_T[e_v]
                #d[w] = d[w] + f_T[e_v]
#            print w
#            print unvisitedcount[w]
#            print "stooooooooooooop"
            unvisitedcount[w] -= 1
            if unvisitedcount[w] == 1 and w not in R:
                Queue.append(w)

#        print Queue
#        print f_T   
#        print v_curr
        
    for v in V[0]:     
        temp = d[v]        
        d[v] = -temp        
        
      
    d_R = {}
    d_N = {}
    for v in d:
        if v in R:
            d_R[v] = d[v]
    
    for v in d:
        if v in N:
            d_N[v] = d[v]
            
    return d_R, d_N, f_T
        
        

        
        
        
        
        
        
        
        
        
        
