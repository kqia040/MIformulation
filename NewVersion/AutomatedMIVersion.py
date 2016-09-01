# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 08:49:42 2016

@author: kqia040
"""

#Starting week6 sem2
#Containing all the code for the MI project
#importing libs
import numpy as np
import pandas as pd
import sys
sys.path.append('C:\Users\kqia040\Documents\GitHub\MIformulation')
import HyperSupport as sp

#set path of the file
path1 = "tsp6problem.tsp"

#gives me the matrix    
MatrixFromFile = sp.read_tsp_file(path1)
#returns the matrix I want. 

#find n
numCity = len(MatrixFromFile)

#Create V set

#create R set of root nodes
R_set = sp.CreateRset(numCity)

#creates N set
N_set = sp.CreateNset(numCity)
#Create V with R and N
v_set = []
v_set.append(R_set)
v_set.append(N_set)

#example reading it
len(v_set[0])
len(v_set[1])
#861


#Generate Pedgree -> i'm going to cheat here and just use an existing pedgree
P = []
P.append([1,3])
P.append([1,4])
P.append([2,3])

#or use the auto pedegree generator function

#Generate E_T by pedegree is this E or ET. hmmmmm
E_T = sp.GenerateE_T(v_set,P)

#generating row col labels
dfRowNames, dfColNames = sp.GenearteDFLabels(v_set)


#Here u can appead any item that is linearly indenpendent
#later on we will pick the ones that are most optimal to pivot to later in optimatlity checking
#for the purposes of the initial solution, we can pick any that is linearly independent


M_R_size = len(R_set)
#auto pedegree list
autoPedegree = sp.AuthoGeneratePedegree(M_R_size)

#Need to write a funciton to generate slack variables from autopedegree
slackList = sp.ChooseSlackVariables(v_set, autoPedegree, M_R_size)

#append the slack variables to dfColname
for i in slackList:
    dfColNames.append(i)

#manual
dfColNames.append([1,2])
dfColNames.append([3,4])
dfColNames.append([3,5])


MatrixSize = (len(N_set) + len(P),len(N_set) + len(P))
matrixA = np.zeros(MatrixSize)
#not sure if it is nessessary to change into df
df = pd.DataFrame(data = matrixA, dtype = int)

#maybe dont use dataframe, use matrix
#below code plants the +1 and -1s    
#using P for tiru's example or autopedegree 
df = sp.createDataFrameForIncidenceMatrix(df, dfColNames, dfRowNames, P, R_set)
#matrixA =  sp.createMatrixForIncidenceMatrix(matrixA, dfColNames, dfRowNames, P, R_set)
#slack variables from the df or matrix

df = sp.addInPlusAndMinusOnesforSlackVariables(df, dfColNames, dfRowNames, R_set)


#andt hen we want to find the differnce btween the P and N_set and then 
#add that to the E_T list with edges of emptyset,IJ
#Create R, N set (from pedgree I think)



#Calculate demand for d(N)
#
#Create E set
E_set = sp.CreateFullEdgeSet(M_R_size, N_set)
E_X = sp.CreateE_X_set(E_set, E_T)
E = []
E.append(E_T)
E.append(E_X)
#make H=(V,E)
H = [v_set, E_set]    



#and then write the code to generate matrix M based on pedegree    

#Make \tau_r for the hypertree path (from random pedegree i think)    
Tau_r = sp.makeSpanningTree(df, dfColNames, dfRowNames, v_set, P)
LenN_set = len(N_set)
M_R_matrix = sp.getMR(df, M_R_size, LenN_set)
from numpy.linalg import inv
M_R_inv = inv(M_R_matrix)

#Initial demand
Initial_demand = sp.initialDemandVector(dfRowNames, P, numCity)
d_R = Initial_demand[:numCity-3]
d_N = Initial_demand[numCity-3:]
f_X = np.zeros(len(E_X))
#d_R is 1, d_N is like 1 for the 12,13,23 and 0 for the rest f_X is initially 0
#def Flow(H, v_set, E_X, E_T, Tau_r, d_R, d_N, f_X):  
#    for i in xrange(0,len(d_R)):
#        d_R[i] = 0
#    
#    for e in E_X:
#        if e.name[0] = 0:
#            pass
#        else:
#            pass
#    
#    for v in 
#    return d_R, f_T
    
    

#Assign cost for e_i
#Find capacity for e_i
#Find flows for f(X) (is it just 0, or is it adding up the capacity)
#Making H = (V, E)

#Make \tau_r for the hypertree path (from random pedegree i think)
#Primal
#Flow
#Check Opt
#Efficincy testing/Benchmark testing
