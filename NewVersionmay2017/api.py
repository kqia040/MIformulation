# -*- coding: utf-8 -*-
"""
Created on Tue May 02 10:56:06 2017

This is going to be the api that makes the sets and stuff

@author: Kun
"""

import random
import numpy as np
import newdualitseems as newdual
import copy


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
    pass

def traverse(E_B, V):
#    j = 0
    V_prime = copy.deepcopy(V[0])
    E_prime = copy.deepcopy(E_B[0])
    e_list = []
    v_list = []    
    len_e_prime = len(E_prime)
    while len_e_prime > 0:
        e = E_prime.pop(0)
#        print e
        if e[1] is not None:
            temp_e_v_set = {(e[0][0],e[1]), (e[0][1],e[1]), e[1]}
        elif e[1] is None:
            temp_e_v_set = set()
    
        if temp_e_v_set.issubset(V_prime):
            e_list.append(e)
            v_list.append(e[0])
            V_prime.append(e[0])
            len_e_prime -=1
#            print "yes"
        else:
            E_prime.append(e)
#            print "no"
    TR = [V[0]]
    
    for i in range(len(e_list)):
        TR.append(e_list[i])
        TR.append(v_list[i])

    return TR, e_list, v_list

def find_e_bar(E_B, v_list, e_star):
    len_v_list = len(v_list)
    critical_node_dict = dict.fromkeys(E_B[1], None)
    e_bar_dict = dict.fromkeys(E_B[1], None)
    for e in E_B[1]:
        if e[1] is not None:
            temp_e_v_set = {e[0], (e[0][0],e[1]), (e[0][1],e[1])}
        elif e[1] is None:
            temp_e_v_set = set(e[0])

        for i in range(len_v_list-1,-1,-1):
            if v_list[i] in temp_e_v_set:
                critical_node_dict[e] = v_list[i]
                break
    
    for e_x in critical_node_dict:
        if critical_node_dict[e_x] is not None:
            for e in E_B[0]:
                if e[1] is not None:
                    temp_e_v_set = {e[0], (e[0][0],e[1]), (e[0][1],e[1]), e[1]}
                elif e[1] is None:
                    temp_e_v_set = {e[0]}
                
                if critical_node_dict[e_x] in temp_e_v_set:
                    e_bar_dict[e_x] = e    
    
    e_bar = None    
    for e in e_bar_dict:
        if e_bar_dict[e] == e_star:
            e_bar = e_star
    
    if e_bar == None:
        return None
        
    else:
        return e_bar
        
        
def test_MR_inv(E_B, V):
    r = copy.deepcopy(V[0])
    temp1 = []
    temp2 = []
    for e in E_B[0]:
        if e[1] is None:
            temp1.append(e)
        else:
            temp2.append(e)
            
    c = temp1+temp2+E_B[1]
    
    
    for e in temp1:
        r.append(e[0])
    
    for e in temp2:
        if e[1] is not None:
            temp_e_v_set = {e[0], (e[0][0],e[1]), (e[0][1],e[1])}
        elif e[1] is None:
            temp_e_v_set = set(e[0])
            
        for v in temp_e_v_set:
            if v not in r:
                r.append(v)
                continue
    
    len_R = len(r)
    M = np.zeros([len_R,len_R])
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
    
    
    rows = range(0,len(V[0]))
    cols = range(0,len(V[1]))
    B = M[rows][:,cols]
        
    rows = range(len(V[0]),len_R)
    cols = range(0,len(V[1]))
    U = M[rows][:,cols]
    
    rows = range(0,len(V[0]))
    cols = range(len(V[1]),len_R)
    C = M[rows][:,cols]
    
    
    rows = range(len(V[0]),len_R)
    cols = range(len(V[1]),len_R)
    D = M[rows][:,cols]
    
    MR11 = C - np.dot(np.dot(B,np.linalg.inv(U)),D)
    MR_inv11 = np.linalg.inv(MR11)
    return MR_inv11
    
    
def find_e_star(E_B, V, e_prime):
    E_T = E_B[0]
    E_X = E_B[1]
    R = V[0]
    N = V[1]
    r = list(R)+list(N)
    c = list(E_T) + list(E_X)
    len_R = len(R)
    len_N = len(N)
    e_star_dic = set() 
    M = np.zeros([len_R+len_N,len_R+len_N])
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
    
    M_eprime = np.zeros(len_R+len_N)
    
    if e_prime[1] is None:
        ij = r.index(e_prime[0])
        M_eprime[ij] = 1
    else:
        ij = r.index(e_prime[0])
        k = r.index(e_prime[1])
        ik = r.index((e_prime[0][0],e_prime[1]))
        jk = r.index((e_prime[0][1],e_prime[1]))
        M_eprime[ij] = 1
        M_eprime[k] = -1
        M_eprime[ik] = -1
        M_eprime[jk] = -1
    
    
    correct_rank = np.linalg.matrix_rank(M)
    counter = 0
    while counter<(len_R+len_N):
        cols = range(len_R+len_N)    
        cols.remove(counter)
        M[:,cols]
        test_rank = np.linalg.matrix_rank(np.c_[M[:,cols],M_eprime])
        if test_rank == correct_rank:
            e_star_dic.add(c[counter])
        counter+=1
    

    return e_star_dic
    
def lp_find_flow(E_B, V, rhs_indicator):
    R = V[0]
    N = V[1]    
    r = R+N
    E_T = E_B[0]
    E_X = E_B[1]    
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
    if rhs_indicator == 'default':    
        for i in range(len(r)):
            if r[i] in R:
                b[i] = -1
            elif r[i] == (1,2) or r[i] == (1,3) or r[i] == (2,3):
                b[i] = 1
            else:
                b[i] = 0
    else:
        #we get an edge ((ij)k) or ((ij) None)
        if rhs_indicator[1] is None:
            for i in range(len(r)):
                if r[i] == rhs_indicator[0]:
                    b[i] = -1
        else:
            ij = rhs_indicator[0]
            k = rhs_indicator[1]
            ik = (rhs_indicator[0][0], rhs_indicator[1])  
            jk = (rhs_indicator[0][1], rhs_indicator[1]) 
            for i in range(len(r)):
                if r[i] == ij:
                    b[i] = -1
                elif r[i] == k or r[i] == ik or r[i] == jk:
                    b[i] = 1

    
    f = np.dot(np.linalg.inv(M),b)
   
    f_lp = {}
    for i in range(len(f)):
        f_lp[c[i]] = f[i]
    
    return f_lp