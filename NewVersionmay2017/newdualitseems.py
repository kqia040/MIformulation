# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 13:17:47 2017

@author: Kun
"""

import copy
import numpy as np

def newdual(E_B,dist_dic,V):
    R = copy.deepcopy(V[0])
    N = copy.deepcopy(V[1])
    pi_dl = dict.fromkeys(set(R+N), None)
    xijkset = set()
    pivector = R
    #Vtail = set()
    for e in E_B[0]:
        if e[1] is None:
            pi_dl[e[0]] = dist_dic[e[0]]
        else:
            xijkset.add(e)
            pivector.append(e[0])
            
            
    xijkset = xijkset.union(E_B[1])
        
    MMM = np.zeros([len(xijkset),len(xijkset)])
    rhs = np.zeros(len(xijkset))
    
    
    counter = 0
    for e in xijkset:
        temp = 0
        if e[0] in pivector:
            #head so its -1
            MMM[counter][pivector.index(e[0])] = -1
    
        else:
            temp += pi_dl[e[0]]
            
        if (e[0][0],e[1]) in pivector:
            MMM[counter][pivector.index((e[0][0],e[1]))] = 1
            
        else:
            temp -= pi_dl[(e[0][0],e[1])]
        
        if (e[0][1],e[1]) in pivector:
            MMM[counter][pivector.index((e[0][1],e[1]))] = 1
            
        else:
            temp -= pi_dl[(e[0][1],e[1])]
            
        if e[1] in pivector:
            #head so its -1
            MMM[counter][pivector.index(e[1])] = 1
    
        else:
            temp -= pi_dl[e[1]]
        
        rhs[counter] = temp
        counter +=1
            
        
    sol = np.linalg.solve(MMM,rhs)
    counter = 0
    for v in pivector:
        pi_dl[v] = sol[counter]
        counter+=1
    
    return pi_dl

    







#def newdual2(E_B,dist_dic,V):
#    R = copy.deepcopy(V[0])
#    N = copy.deepcopy(V[1])
#    pi_dl = dict.fromkeys(set(R+N), None)
#    xijkset = set()
#    pivector = R
#    #Vtail = set()
#    for e in E_B[0]:
#        if e[1] is None:
#            pi_dl[e[0]] = dist_dic[e[0]]
#    #    else:
#    #        xijkset.add(e)
#    #        pivector.append(e[0])
#    for v in N:
#        if (v,None) not in E_B[0]:
#            pivector.append(v)
#    
#    for e in E_B[0]:
#        if e[1] is not None:
#            xijkset.add(e)
#            
#            
#    xijkset = xijkset.union(E_B[1])
#        
#    MMM = np.zeros([len(xijkset),len(xijkset)])
#    rhs = np.zeros(len(xijkset))
#    
#    
#    counter = 0
#    for e in xijkset:
#        temp = 0
#        if e[0] in pivector:
#            #head so its -1
#            MMM[counter][pivector.index(e[0])] = -1
#    
#        else:
#            temp += pi_dl[e[0]]
#            
#        if (e[0][0],e[1]) in pivector:
#            MMM[counter][pivector.index((e[0][0],e[1]))] = 1
#            
#        else:
#            temp -= pi_dl[(e[0][0],e[1])]
#        
#        if (e[0][1],e[1]) in pivector:
#            MMM[counter][pivector.index((e[0][1],e[1]))] = 1
#            
#        else:
#            temp -= pi_dl[(e[0][1],e[1])]
#            
#        if e[1] in pivector:
#            #head so its -1
#            MMM[counter][pivector.index(e[1])] = 1
#    
#        else:
#            temp -= pi_dl[e[1]]
#        
#        rhs[counter] = temp
#        counter +=1
#            
#        
#    sol = np.linalg.solve(MMM,rhs)
#    counter = 0
#    for v in pivector:
#        pi_dl[v] = sol[counter]
#        counter+=1
#        
#    return pi_dl



def newdual2(E_B,dist_dic,V):
    R = copy.deepcopy(V[0])
    N = copy.deepcopy(V[1])
    pi_dl = dict.fromkeys(set(R+N), None)
    xijkset = set()
    pivector = R
    #Vtail = set()
    for e in E_B[0]:
        if e[1] is None:
            pi_dl[e[0]] = dist_dic[e[0]]
    #    else:
    #        xijkset.add(e)
    #        pivector.append(e[0])
    for v in N:
        if (v,None) not in E_B[0]:
            pivector.append(v)
    
    for e in E_B[0]:
        if e[1] is not None:
            xijkset.add(e)
            
            
    xijkset = xijkset.union(E_B[1])
        
    MMM = np.zeros([len(xijkset),len(xijkset)])
    rhs = np.zeros(len(xijkset))
    
    
    counter = 0
    for e in xijkset:
        temp = 0
        if e[0] in pivector:
            #head so its -1
            MMM[counter][pivector.index(e[0])] = -1
    
        else:
            temp += pi_dl[e[0]]
            
        if (e[0][0],e[1]) in pivector:
            MMM[counter][pivector.index((e[0][0],e[1]))] = 1
            
        else:
            temp -= pi_dl[(e[0][0],e[1])]
        
        if (e[0][1],e[1]) in pivector:
            MMM[counter][pivector.index((e[0][1],e[1]))] = 1
            
        else:
            temp -= pi_dl[(e[0][1],e[1])]
            
        if e[1] in pivector:
            #head so its -1
            MMM[counter][pivector.index(e[1])] = 1
    
        else:
            temp -= pi_dl[e[1]]
        
        rhs[counter] = temp
        counter +=1
            
        
    sol = np.linalg.solve(MMM,rhs)
    counter = 0
    for v in pivector:
        pi_dl[v] = sol[counter]
        counter+=1
        
    return pi_dl

















