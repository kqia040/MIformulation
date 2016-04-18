# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 08:34:34 2016

Script the will create the matrices needed for the MI formulation

@author: kqia040
"""
import numpy as np

def MakeMatrixEn(d):
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


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    