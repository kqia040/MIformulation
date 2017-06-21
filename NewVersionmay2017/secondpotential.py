# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:03:35 2017

@author: Kun
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 10 10:23:21 2017
Potential 
@author: Kun
"""
#dist_matrix will be a dictionary with distance of ij as value with ij as key
def potential(V, E_B, c_T, pi_R):
    R = V[0]
    N = V[1]    
    c_X = dict.fromkeys(E_B[1], 0)
    pi_N = dict.fromkeys(V[1], None)
    E_X = E_B[1].copy()
    E_T = E_B[0].copy()
#    E_NB = E_NB.copy()
    for e in E_X:
        c_X[e] = 0

#    for e in E_NB:
#        c_NB[e] = 0
    
    for v in R:
        for e in E_T:
            headtailunion = [e[0], e[1], (e[0][0],e[1]), (e[0][1],e[1])]
#            print v, "vvvv"
#            print e, "eeeee"            
            if v in headtailunion:
                if v == e[0]:
                    c_T[e] = c_T[e] - pi_R[v]
                else:
                    c_T[e] = c_T[e] + pi_R[v]
        #E_X set represents the M_R side of the basis
        for e in E_X:
            headtailunion = [e[0], e[1], (e[0][0],e[1]), (e[0][1],e[1])]
#            print v, "vvvv"
#            print e, "eeeee"            
            if v in headtailunion:
                if v == e[0]:
                    c_X[e] = c_X[e] - pi_R[v]
                else:
                    c_X[e] = c_X[e] + pi_R[v]
        
#        for e in E_NB:
#            headtailunion = [e[0], e[1], (e[0][0],e[1]), (e[0][1],e[1])]
##            print v, "vvvv"
##            print e, "eeeee"            
#            if v in headtailunion:
#                if v == e[0]:
#                    c_NB[e] = c_NB[e] - pi_R[v]
#                else:
#                    c_NB[e] = c_NB[e] + pi_R[v]
            
    unvisited = {}
    for e in E_T:
        count = 0
        if e[1] is None:
            if e[0] in N:
                count+=1
            unvisited[e] = count
        else:           
            if e[0] in N:
                count +=1
            if (e[0][0],e[1]) in N:
                count +=1
            if (e[0][1],e[1]) in N:
                count +=1
            if (e[1]) in N:
                count +=1
        #here i dont loop through and do stuff for Uij
        unvisited[e] = count
        
    for e in E_X:
        count = 0
        if e[1] is None:
            if e[0] in N:
                count+=1
            unvisited[e] = count
        else:           
            if e[0] in N:
                count +=1
            if (e[0][0],e[1]) in N:
                count +=1
            if (e[0][1],e[1]) in N:
                count +=1
            if (e[1]) in N:
                count +=1
        #here i dont loop through and do stuff for Uij
        unvisited[e] = count
        
#    for e in E_NB:
#        count = 0
#        if e[1] is None:
#            if e[0] in N:
#                count+=1
#            unvisited[e] = count
#        else:           
#            if e[0] in N:
#                count +=1
#            if (e[0][0],e[1]) in N:
#                count +=1
#            if (e[0][1],e[1]) in N:
#                count +=1
#            if (e[1]) in N:
#                count +=1
#        #here i dont loop through and do stuff for Uij
#        unvisited[e] = count
    
    Queue = []      
    
#ahhhhhhhhhhhh the prooblem is that there are every edge in unvisitd is 3 or 0, leaving queue be empty
    
    for e in unvisited:
        if e in E_T and unvisited[e] == 1:
            Queue.append(e)
    visited_node = set()
    while Queue:
        e_prime = Queue.pop(0)
        #this is wrong
        #v_prime = e_prime[0]
        v_prime = None        
        if e_prime[1] is None:
            v_prime = e_prime[0]
        else:
            e_incident = [e_prime[0], e_prime[1], (e_prime[0][0],e_prime[1]), (e_prime[0][1],e_prime[1])]
        
            for v in e_incident:
                if v in N and v not in visited_node:
                    v_prime = v
        if v_prime is None:
            print "errrrror v_prime is None"
            #so... when the edges of the Pedigree gets added to the Queue, then 
            #there will be no incident edges
            #break            
            continue
        visited_node.add(v_prime)
        if v_prime == e_prime[0]:
            if e_prime in E_T:                
                pi_N[v_prime] = c_T[e_prime]
            elif e_prime in E_X:
                pi_N[v_prime] = c_X[e_prime]
#            elif e_prime in E_NB:
#                pi_N[v_prime] = c_NB[e_prime]
                
        else:
            if e_prime in E_T:                
                pi_N[v_prime] = -c_T[e_prime]
            elif e_prime in E_X:
                pi_N[v_prime] = -c_X[e_prime]
#            elif e_prime in E_NB:
#                pi_N[v_prime] = -c_NB[e_prime]
        
        
        if e_prime in E_T:
            E_T.remove(e_prime)
        elif e_prime in E_X:
            E_X.remove(e_prime)
#        elif e_prime in E_NB:
#            E_NB.remove(e_prime)
            
        for e in E_T:
            temp_set = set()
            temp_set.add(e[0])
            temp_set.add((e[0][0],e[1]))
            temp_set.add((e[0][1],e[1]))
            temp_set.add(e[1])
            if v_prime in temp_set:
                #if v_prime is the head                
                if v_prime == e[0]:
                    c_T[e] = c_T[e] - pi_N[v_prime]
                else:
                    c_T[e] = c_T[e] + pi_N[v_prime]
                        
                unvisited[e] -=1
                if unvisited[e] == 1:
                    Queue.append(e)
        for e in E_X:
            temp_set = set()
            temp_set.add(e[0])
            temp_set.add((e[0][0],e[1]))
            temp_set.add((e[0][1],e[1]))
            temp_set.add(e[1])
            if v_prime in temp_set:
                if v_prime == e[0]:
                    c_X[e] = c_X[e] - pi_N[v_prime]
                else:
                    c_X[e] = c_X[e] + pi_N[v_prime]
                        
                unvisited[e] -=1
                

#        for e in E_NB:
#            temp_set = set()
#            temp_set.add(e[0])
#            temp_set.add((e[0][0],e[1]))
#            temp_set.add((e[0][1],e[1]))
#            temp_set.add(e[1])
#            if v_prime in temp_set:
#                if v_prime == e[0]:
#                    c_NB[e] = c_NB[e] - pi_N[v_prime]
#                else:
#                    c_NB[e] = c_NB[e] + pi_N[v_prime]
#                        
#                unvisited[e] -=1
#                if unvisited[e] == 1:
#                    Queue.append(e)
                
        if e_prime in E_T:
            E_T.add(e_prime)
        elif e_prime in E_X:
            E_X.add(e_prime)
#        elif e_prime in E_NB:
#            E_NB.add(e_prime)

    for e in E_X:
        c_X[e] = -c_X[e]
    return pi_R, pi_N, c_X
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
