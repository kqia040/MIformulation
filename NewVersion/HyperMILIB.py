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
import Support as sp

#Import TSPLIB matrix

#set path of the file
path1 = "tsp6problem.tsp"
def read_tsp_file(path):
    matrixFromFile = np.genfromtxt(path1, skip_header=7, skip_footer = 1)
    return matrixFromFile


#gives me the matrix    
MatrixFromFile = read_tsp_file(path1)
#returns the matrix I want. 


#Create V class
class Vertex:
    def __init__(self, name=None):
        self.name = name

#Create V set
v_set = []
R_set = []
N_set = []
#creates R
for i in range(4,7):
    x = Vertex()
    x.name = i
    R_set.append(x)

#creates N set
a, N_set = sp.calcPerm(6)

#Create V with R and N
v_set.append(R_set)
v_set.append(N_set)

#example reading it
len(v_set[0])
#41
len(v_set[1])
#861


#Generate Pedgree -> i'm going to cheat here and just use an existing pedgree
P = []
P.append([1,3])
P.append([1,4])
P.append([2,3])


#Generate E_T by pedegree is this E or ET. hmmmmm
E_T = []
for i in range(len(P)):
    E_T.append([int(v_set[0][i].name),P[i]])
    
for i in N_set:
    if i not in P:
        E_T.append([0,i])



dfRowNames = []
for i in R_set:
    dfRowNames.append(i.name)

for i in N_set:
    dfRowNames.append(i)
    
    
#df.index = dfRowNames

dfColNames = []
for i in N_set:
    dfColNames.append(i)


#Here u can appead any item that is linearly indenpendent
#later on we will pick the ones that are most optimal to pivot to later in optimatlity checking
#for the purposes of the initial solution, we can pick any that is linearly independent
dfColNames.append([1,2])
dfColNames.append([3,4])
dfColNames.append([3,5])


MatrixSize = (len(N_set) + len(P),len(N_set) + len(P))
matrixA = np.zeros(MatrixSize)
df = pd.DataFrame(data = matrixA)

#maybe dont use dataframe, use matrix
#setting the diagonal 1's
for i in range(3,len(dfRowNames)):
    indexOfi = dfColNames[0:15].index(dfRowNames[i])    
    print indexOfi, " ", i
    df[indexOfi][i] = 1
    
df

#insert the -1 (for the R nodes)
for i in R_set:
    colIndex = dfColNames[0:15].index(P[R_set.index(i)])
    rowIndex = R_set.index(i)
    df[colIndex][rowIndex] = -1
    

#andt hen we want to find the differnce btween the P and N_set and then 
#add that to the E_T list with edges of emptyset,IJ
#Create R, N set (from pedgree I think)



#Calculate demand for d(N)
#
#Create E set
#Create h_e set for e_i
#Create T_e set for e_i
#Assign cost for e_i
#Find capacity for e_i
#Find flows for f(X) (is it just 0, or is it adding up the capacity)
#Making H = (V, E)
#Making M the induced matrix
#Make \tau_r for the hypertree path (from random pedegree i think)
#Primal
#Flow
#Check Opt
#Efficincy testing/Benchmark testing
