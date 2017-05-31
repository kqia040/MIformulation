# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 11:23:17 2017

Main Potential


@author: Kun
"""

#==============================================================================
# Define inputs here 
# Need: V, E_T, E_X, 
#c_T, is 0 for all xijk and the distance matrix ij for all uij edges
#==============================================================================

"""

have to write a function to create the cost vector from the data set from tsplib
the cost vector c_bar is for all xijk is 0 and for uij is the cost between i and j

"""

R =set()
N= set()
E_X = set()

c_T = {}
pi_R = {}
c_X = {}
#values need to be initiated as 0 or something
c = {}
#==============================================================================
#Run potential  
#==============================================================================


for e in E_X:
    c_X[e] = 0
    
for v in R:
    #for e in E such that v in TeU{he} 
    #in other words, all edges associated with v
    #first loop through xijk
    #second loop through uij

#==============================================================================
# """
# The below code doesnt take into the condition that this e in E cant be in E_X
# """    
#==============================================================================

#==============================================================================
# It seems that R changes, so the below code doesnt actually 
#loop through the E set as we think it does
#==============================================================================

    n = len(R)
    for k in range(4,n+1):
        for j in range(2,n+1):
                for i in range(1,j):
                    if i<j and j<k:
                        #((i,j),k)
                        if v == (i,j) or v == (j,k) or v == (i,k) or v == k:
                            c[((i,j),k)] = c[((i,j),k)] + pi_R[v]



    for j in range(2,n+1):
        for i in range(1,j):
            if i<j and v == (i,j):
                #c[((i,j),None)] needs to be defined as the slack variable 
                #which is the cost of the actual distance between i-j
                c[((i,j),None)] = c[((i,j),None)] - pi_R[v]





























