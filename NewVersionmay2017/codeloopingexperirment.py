# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:07:25 2017

code looping experiment

@author: Kun
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 16:31:25 2017

@author: Kun
"""
import api
import numpy as np
import primal as primal
import newdualitseems as newdual
import changebasis
import random
import timeit


n = 200
V = api.makeVset(n)
R = V[0]
N = V[1]


#dist_dic = d

dist_dic = {}
for v in N:
    dist_dic[v] = random.randint(10, 100)

#iii = 1
#jjj = 2
#opt = []
#while jjj<n+1:
#    opt.append((iii,jjj))
#    iii+=1
#    jjj+=1
#
#opt.append((1,jjj-1))
#
#for i in opt:
#    dist_dic[i] = 1



def loop(dist_dic, n, V, R, N):
    notopt = True
    #E_T, P = api.makeE_Tset(n)
    #E_X = api.extendbasis2(n, P)
    
    E_T, E_X, P = api.makeE_B(n,N)
    E = api.makeE_set(n)
    E_B = [E_T, E_X]
    E_NB = E-E_T-set(E_X)        
    
    f_NB = dict.fromkeys(E_NB, 0)
    
    
    while notopt:
        M_R = np.zeros([len(E_X), len(E_X)], dtype='int')
        E_X = list(E_X)
        R = list(R)
        for j in xrange(len(E_X)):
             i = R.index(E_X[j][1])
             M_R[i][j] = -1
        
        MR_inv = np.linalg.inv(M_R)
        
        b_R = dict.fromkeys(V[0], -1)
        b_N = dict.fromkeys(V[1], 0)
        b_N[(1,2)] = 1
        b_N[(1,3)] = 1
        b_N[(2,3)] = 1
        
        b_bar = [b_R, b_N]
        
        try:
            pi_dl = newdual.newdual(E_B, dist_dic, V)
        except:
            print "edge inserted created linear dependency"
            print "algo stopped, opt sol the previous result"
            output_cost = api.calcCost2(f_T,dist_dic)    
            output_cost2 = api.calcCost2(f_T,dist_dic)             
            print "Terminate algorithm"
            print "cost is"
            print output_cost, output_cost2
            break
#            return len(violate), output_cost, output_cost2, E_B, f_T, f_X        
            
        f_T, f_X, bbarN = primal.Primal(V, E_B, MR_inv, b_bar)
        
        pi_N = {}
        pi_R = {}
        
        for v in pi_dl:
            if v in N:
                pi_N[v] = pi_dl[v]
            elif v in R:
                pi_R[v] = pi_dl[v]
        
        
        
        reduced_cost = dict.fromkeys(E_NB, 0)
        
        for e in E_NB:
            if e[1] is not None:
                c_e = 0
            else:
                c_e = dist_dic[e[0]]
        
            if e[1] is not None:
                temp = pi_N[(e[0][0],e[1])] + pi_N[(e[0][1],e[1])] + pi_R[e[1]]      
                reduced_cost[e] = c_e  + temp - pi_N[e[0]]
            else:
                reduced_cost[e] = c_e - pi_N[e[0]]
        
        
        violate = {}
        
        for e in f_NB:
            if f_NB[e] == 0 and reduced_cost[e] < 0:
                violate[e] = reduced_cost[e]
            
            elif f_NB[e] == 1 and reduced_cost[e] > 0:
                violate[e] = reduced_cost[e]
        
#        print len(violate)
#        print api.calcCost(f_T,dist_dic)
        
        if len(violate) == 0:
            output_cost = api.calcCost(f_T,dist_dic)    
            output_cost2 = api.calcCost2(f_T,dist_dic)               
            print "Terminate algorithm"
            print "cost is"
            print output_cost, output_cost2
            notopt = False
            break
#            return len(violate), output_cost, output_cost2, E_B, f_T, f_X
        
        else:
            minRC = float('inf')
            
            uij_violate = set()   
            for e in violate:
                if e[1] is None:
                    uij_violate.add(e)
            
            if len(uij_violate) > 0:
                for e in uij_violate:
                    if violate[e] < minRC:
                        minRC = violate[e]
                        e_prime = e
            else:
                for e in violate:
                    if violate[e] < minRC:
                        minRC = violate[e]
                        e_prime = e
            
#            print "e_prime  ", e_prime
            
                
            E_B, e_star, ex_or_et = changebasis.changebasis(E_B, e_prime)
#            print "e_star   ", e_star
            #ex_or_et tells us if e_star (the leaving arc) is from e_x or e_T
            #so that when we add estar to f_Nb we know where to get the flow data from
    #        if ex_or_et == "E_X":
    #            f_NB.pop(e_prime)
    #            E_NB.add(e_star)
    #            E_NB.remove(e_prime)    
    #            f_NB[e_star] = f_X[e_star]
    #        else:
    #            f_NB.pop(e_prime)
    #            E_NB.add(e_star)
    #            E_NB.remove(e_prime)    
    #            f_NB[e_star] = f_T[e_star]
            
                    
            
            E_T = E_B[0]
            E_X = E_B[1]
            del(E_NB)        
            E_NB = E-E_T-set(E_X)        
            del(f_NB)
            f_NB = dict.fromkeys(E_NB, 0)
            
    #        del(f_T)
    #        del(f_X)
            del(pi_dl)
            del(pi_N)
            del(pi_R)
#            del(violate)
#            del(uij_violate)
        
        
        
count = 0        
while count < 100:
    start = timeit.timeit()      
    len_violate, cost, cost2, E_B, f_T, f_X = loop(dist_dic, n, V, R, N)
    end = timeit.timeit()
    if len_violate == 0:
        print "done, calculate cost is  ", cost
        print "time taken:   ", np.abs(end - start)
        break
    count +=1
    print count

print "number trials is up"
print "violate left", len_violate
print "cost is", cost
print "time taken:   ", np.abs(end - start)


#can write a function to confirm cost with fM = b