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
#how to i assign capacity per node?
class Vertex:
    def __init__(self, name=None):
        self.name = name

#Creat Edge Class
#how do i assign flow per node?
class Edge:
    def __init__(self, name, tail=[], head=[]):
        self.name = name
        #tail = [[k],[i,k],[j,k]]        
        self.tail = tail
        self.head = head
        


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

def CreateNSet(n):
    leftlist = []
    for j in range(2,n+1):
        for i in range(1, n):
            if i<j :
#                print i, " ", j
                leftlist.append([i, j])
#    print uptoplist, len(uptoplist) 
#    print leftlist, len(leftlist)
    return leftlist


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
    edgeInstance = Edge([int(v_set[0][i].name),P[i]])        
    edgeInstance.head = P[i]
    edgeInstance.tail = [[int(v_set[0][i].name)],[P[i][0],int(v_set[0][i].name)],[P[i][1], int(v_set[0][i].name)]]    
    #print edgeInstance.name    
    E_T.append(edgeInstance)
    
for i in N_set:
    if i not in P:
        edgeInstance = Edge([0,i])
        edgeInstance.head = i
        edgeInstance.tail = [0]
        #print edgeInstance.name        
        E_T.append(edgeInstance)

for p in E_T: print "name ", p.name, "head " ,p.head, "tail", p.tail

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
    colIndexRoot = dfColNames[0:15].index(P[R_set.index(i)])
    print colIndexRoot, " ", P[R_set.index(i)][0], " ", P[R_set.index(i)][1], " ", R_set[R_set.index(i)].name
    newNode1 = [P[R_set.index(i)][0],R_set[R_set.index(i)].name]
    newNode2 = [P[R_set.index(i)][1],R_set[R_set.index(i)].name]    
    rowIndexRoot = R_set.index(i)
    rowIndexInsert1 = dfRowNames.index(newNode1)
    rowIndexInsert2 = dfRowNames.index(newNode2)
    df[colIndexRoot][rowIndexRoot] = -1
    df[colIndexRoot][rowIndexInsert1] = -1
    df[colIndexRoot][rowIndexInsert2] = -1
    
df
#Making M the induced matrix

#slack variables
U_set = dfColNames[len(dfColNames) - len(R_set):len(dfColNames)]
M_R_size = len(R_set)
ColCounter = M_R_size
rowCounter = 0
for i in range(4,4+M_R_size):        
    rowRootNumIndex = dfRowNames.index(i)
    colIndex = len(dfColNames)-ColCounter    
    df[colIndex][rowRootNumIndex] = -1
    rowInsertPlusOneIndex = dfRowNames.index(U_set[rowCounter])
    if U_set[rowCounter][0] < i:
        newNode1 = [colIndex, dfRowNames.index([U_set[rowCounter][0],i])]
    else:
        newNode1 = [colIndex, dfRowNames.index(i,[U_set[rowCounter][0]])]
    if U_set[rowCounter][1] < i:
        newNode2 = [colIndex, dfRowNames.index([U_set[rowCounter][1],i])]
    else:
        newNode2 = [colIndex, dfRowNames.index(i,[U_set[rowCounter][1]])]    

    df[colIndex][newNode1[1]] = -1
    df[colIndex][newNode2[1]] = -1
    df[colIndex][rowInsertPlusOneIndex] = 1   
    ColCounter = ColCounter-1
    rowCounter = rowCounter +1
df



#andt hen we want to find the differnce btween the P and N_set and then 
#add that to the E_T list with edges of emptyset,IJ
#Create R, N set (from pedgree I think)



#Calculate demand for d(N)
#
#Create E set
E_set = []

#Create h_e set for e_i
#Create T_e set for e_i
for i in N_set:
    edgeInstance = Edge([0,i])
    edgeInstance.head = i
    edgeInstance.tail = [0]    
    E_set.append(edgeInstance)



for k in range(4,4+M_R_size):
    for j in range(2,4+M_R_size):
            for i in range(1,j):
                if i<j and j<k:
                    edge = Edge([k,[i,j]])
                    edge.head = [i,j]
                    edge.tail = [[k],[i,k],[j,k]]                    
                    E_set.append(edge)

    
for p in E_set: print "name ", p.name, "head " ,p.head, "tail", p.tail

#create list of names in E_T
E_TnameList = []    
for i in E_T:
    E_TnameList.append(i.name)

#create E_X 
E_X =[] 
for i in xrange(0,len(E_set)):
    if E_set[i].name in E_TnameList:
        E_X.append(E_set[i])

len(E_X)
for p in E_X: print "name ", p.name, "head " ,p.head, "tail", p.tail
        

#make H=(V,E)
H = [v_set, E_set]    

#make random pedegree generator    
np.random.seed(1)
N_set_subset = []
Avaiable_N_set = []
Auto_Pedegree = []
N_list = CreateNSet(3)
nodeCreated1 = []
nodeCreated2 = []
#set it starting from 3 because we start from the n=3
for i in range(3,3+M_R_size):
    root_index = i+1       
    randomIndex = np.random.choice(len(N_list), 1)
    Auto_Pedegree.append(N_list[int(randomIndex)])
    PedegreeNode = N_list[int(randomIndex)]
    nodeCreated1 = [PedegreeNode[0],root_index]
    nodeCreated2 = [PedegreeNode[1],root_index]
    N_list.remove(PedegreeNode)
    N_list.append(nodeCreated1)
    N_list.append(nodeCreated2)
    
for i in Auto_Pedegree: print i
    
    
#and then write the code to generate matrix M based on pedegree    

#Make \tau_r for the hypertree path (from random pedegree i think)    
    
    

#Assign cost for e_i
#Find capacity for e_i
#Find flows for f(X) (is it just 0, or is it adding up the capacity)
#Making H = (V, E)

#Make \tau_r for the hypertree path (from random pedegree i think)
#Primal
#Flow
#Check Opt
#Efficincy testing/Benchmark testing
