# -*- coding: utf-8 -*-
"""
Created on Tue May 02 10:56:06 2017

This is going to be the api that makes the sets and stuff

@author: Kun
"""

import random
import numpy as np
import newdualitseems as newdual



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


#Don;t need to add the Uij coz thats part of E_T deffs - this is wrong
def makeE_set(n):
    E = set()
    for k in range(4,n+1):
        for j in range(2,n+1):
                for i in range(1,j):
                    if i<j and j<k:
                        E.add(((i,j),k))

    for j in range(2,n+1):
        for i in range(1, n):
            if i<j:
                E.add(((i, j), None))    
    
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
    
    
def calcCost(f_T, dist_dic):
    cost = 0
    for e in f_T:
        if f_T[e] !=0 and e[1] is None:
            cost+= f_T[e] * dist_dic[e[0]]
            
    return cost

def calcCost2(f_T, dist_dic):
    cost = 0
    for e in f_T:
        if f_T[e] > 0 and e[1] is None:
            cost+= 1 * dist_dic[e[0]]
    return cost
    
    
def makeE_B(n, N_0):
    N = set(((1,2),(1,3),(2,3)))
    P = set()
    E_X = set()
    E_T = set()
    for i in xrange(4, n+1):      
        random_node = random.sample(N,1)
        P.add((random_node[0], i))
        N.remove(random_node[0])
        extendbasis_node = random.sample(N,1)
        E_X.add((extendbasis_node[0], i))
        N.remove(extendbasis_node[0])
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
    
    P_0 = set()
    for e in P:
        P_0.add(e[0])
        E_T.add(e)
    for v in N_0:
        if v not in P_0:
            E_T.add((v, None))
    
    return E_T, E_X, P
    
    
def calculateFlow(E_B, R, N):
    E_T = E_B[0]
    E_X = E_B[1]
    r = R+N
    c = list(E_T) + list(E_X)
    M = np.zeros([len(R)+len(N),len(R)+len(N)])
    
    
    
    for cc in range(len(c)):
        if c[cc][1] is None:
            ij = r.index(c[cc][0])
            M[ij][cc] = 1
        else:
            ij = r.index(c[cc][0])
            k = r.index(c[cc][1])
            ik = r.index((c[cc][0][0],c[cc][1]))
            jk = r.index((c[cc][0][1],c[cc][1]))
            M[ij][cc] = 1
            M[k][cc] = -1
            M[ik][cc] = -1
            M[jk][cc] = -1
    
    
    
    b = np.zeros(len(r))
    for i in range(len(r)):
        if r[i] in R:
            b[i] = -1
        elif r[i] == (1,2) or r[i] == (1,3) or r[i] == (2,3):
            b[i] = 1
        else:
            b[i] = 0
    
    f = np.dot(np.linalg.inv(M),b)
    
    
    f_lp = {}
    for i in range(len(f)):
        f_lp[c[i]] = f[i]    
    
    
    return f_lp
    
def changebasis(E_B, e_prime):
    for e in E_B[0]:
        if e[0] == e_prime[0]:
            e_star = e
    
    E_B[0].add(e_prime)
    E_B[0].remove(e_star)
    return E_B, e_star


def loop(dist_dic, n, V, R, N):
    notopt = True
    #E_T, P = api.makeE_Tset(n)
    #E_X = api.extendbasis2(n, P)
    
    E_T, E_X, P = makeE_B(n,N)
    E = makeE_set(n)
    E_B = [E_T, E_X]
    E_NB = E-E_T-set(E_X)        
    
    f_NB = dict.fromkeys(E_NB, 0)
#    try:
#        len_violate = len(violate)
#    except:
#        len_violate = float('inf')   
    
    
    
    
    
    while notopt:
        
        try:
            pi_dl = newdual.newdual(E_B, dist_dic, V)
        except:
            print "edge inserted created linear dependency"
            print "algo stopped, opt sol the previous result"
#            output_cost = api.calcCost2(f_T,dist_dic)    
#            output_cost2 = api.calcCost2(f_T,dist_dic)             
#            print "Terminate algorithm"
#            print "cost is"
#            print output_cost, output_cost2
#            break
#            return len(violate), output_cost, output_cost2, E_B, f_T, f_X
            return len_violate, E_B
            
#        f_T, f_X, bbarN = primal.Primal(V, E_B, MR_inv, b_bar)
        
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
        
        len_violate = len(violate)
        if len_violate == 0:
#            output_cost = api.calcCost(f_T,dist_dic)    
#            output_cost2 = api.calcCost2(f_T,dist_dic)               
            print "Terminate algorithm"
            print "cost is"
#            print output_cost, output_cost2
            notopt = False
#            break
            return len_violate, E_B
        
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
            
                
            E_B, e_star = changebasis(E_B, e_prime)
            E_T = E_B[0]
            E_X = E_B[1]
            del(E_NB)        
            E_NB = E-E_T-set(E_X)        
            del(f_NB)
            f_NB = dict.fromkeys(E_NB, 0)
            
            del(pi_dl)
            del(pi_N)
            del(pi_R)
#            print "violate len is", len_violate
        
