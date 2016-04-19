# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 08:34:34 2016

Script the will create the matrices needed for the MI formulation
1. To create E_n matrix: call MakeMatrixEn(n)
2. To create A_n matrix: call MakeMatrixA_n(n)
3. To create full matrix call MakeMatrixFull(n)
@author: kqia040
"""
import numpy as np

def MakeMatrixFull(n):
    E_n = MakeMatrixEn(n)
    A_n, leftlist = MakeMatrixA_n(n)
    print E_n, A_n
    LeftMatrix = np.row_stack((E_n,A_n))
    print LeftMatrix
    righttop = np.zeros((n-3,len(leftlist)))
    rightbot = np.identity(len(leftlist))
    print righttop, rightbot
    RightMatrix = np.row_stack((righttop,rightbot))
    print "LeftMatrix", LeftMatrix, LeftMatrix.shape
    print "-"*50
    print "RightMatrix", RightMatrix, RightMatrix.shape
    FullMatrix = np.hstack((LeftMatrix,RightMatrix))
    print FullMatrix, FullMatrix.shape
    return FullMatrix


def InitiateA_nMatrix(n):
    total_size = 0
    for x in xrange(n,3,-1):
        total_size = total_size + ((x-1)*(x-2)/2)
        
    rowNum = 0
    for x in xrange(1,n):
        rowNum = rowNum+x
      
    print "total_size = ", total_size    
    colNum = total_size
    Matrix = np.zeros((rowNum, total_size))
    print Matrix
    return Matrix
    
def MakeMatrixA_n(n):
#take the initiated all 0 matrix and fill it up with 1 -1 and 0 in appropriate places   
    emptyA_n = InitiateA_nMatrix(n)
    uptoplist, leftlist = calcPerm(n)
    print emptyA_n.shape
    for i in range((len(uptoplist))):
        z = leftlist.index([uptoplist[i][0], uptoplist[i][1]])
        x = leftlist.index([uptoplist[i][0], uptoplist[i][2]])
        y = leftlist.index([uptoplist[i][1], uptoplist[i][2]])
        print z,x,y
        emptyA_n[z][i] = 1
        emptyA_n[x][i] = -1
        emptyA_n[y][i] = -1
        
    return emptyA_n, leftlist
        
        
def calcPerm(n):

    uptoplist = [] 
    for k in range(4,n+1): 
        for j in range(2,k):
            for i in range(1,j):
                if i<j and j<k:                
#                    print i," ", j, " ", k
                    uptoplist.append([i, j, k])

    leftlist = []
    for j in range(2,n+1):
        for i in range(1, n):
            if i<j :
#                print i, " ", j
                leftlist.append([i, j])
#    print uptoplist, len(uptoplist) 
#    print leftlist, len(leftlist)
    return uptoplist, leftlist



    
def MakeMatrixEn(n):
    d = MakeDictionaryOfEnVectors(n)
    matrix_size = len(d)+3
    print matrix_size
    b= np.row_stack((d["e_4"],d["e_5"]))
    for x in xrange(5,matrix_size):
        b = np.row_stack((b,d["e_{0}".format(x+1)]))
    return b
    

def MakeDictionaryOfEnVectors(n):
    d={}
    total_size = 0
    e_n_minus1_size = 0
    for x in xrange(n,3,-1):
        total_size = total_size + ((x-1)*(x-2)/2)
          
    print "total_size = ", total_size
#    for x in xrange(n-1,3,-1):
#        if x == 4:
#            e_n_minus1_size = e_n_minus1_size +3
#        else:
#            e_n_minus1_size = e_n_minus1_size + ((n-2)*(n-3)/2)
    
    
    
    for x in xrange(4,n+1,1):
              
#        print x    
        e_n_minus1_size = e_n_minus1_size + ((x-2)*(x-3)/2)        
        
        
#        for y in xrange(n-1,3,-1):
#            if y == 4:
#                e_n_minus1_size = e_n_minus1_size +3
#            else:
#                e_n_minus1_size = e_n_minus1_size + ((y-2)*(y-3)/2)
#            print x,y, e_n_minus1_size
        
       
        if x == 4:
            e_n_minus1_size=0
            d["e_{0}".format(x)] = np.concatenate((np.ones(3),np.zeros(total_size-3)))
        else:
#            print x, e_n_minus1_size
            e_n_size = ((x-1)*(x-2)/2)
            #print e_n_minus1_size, e_n_size
            a_a = np.zeros(e_n_minus1_size)
            a_b = np.ones(e_n_size)  
            a_c = np.zeros(total_size-e_n_minus1_size-e_n_size)
            e_n_a_b = np.concatenate((a_a,a_b))   
            e_n_a_b_c = np.concatenate((e_n_a_b,a_c))
            #print e_n_a_b_c.size
#            print "dfa", total_size, e_n_minus1_size
#            print "rest", e_n_size, a_a.size, a_b.size, a_c.size
            d["e_{0}".format(x)]=e_n_a_b_c
#        print x, e_n_minus1_size    
#   
#    print d
    return d
#    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    