# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 11:32:30 2016

This script contains the functions for MI on hyperloop

@author: kqia040
"""

import numpy as np
import pandas as pd
import sys
sys.path.append('C:\Users\kqia040\Documents\GitHub\MIformulation')

#Import TSPLIB matrix

#set path of the file
def read_tsp_file(path):
    matrixFromFile = np.genfromtxt(path, skip_header=7, skip_footer = 1)
    return matrixFromFile
    
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
        
#creates R of vertex objects not just names
def CreateRset(n):
    R_set = []
    for i in range(4,n+1):
        x = Vertex()
        x.name = i
        R_set.append(x)
    return R_set
    
#creates N set of permutations on the left    
def CreateNset(n):
    N_set = []
    for j in range(2,n+1):
        for i in range(1, n):
            if i<j :
                N_set.append([i, j])
    return N_set
    
    
#Generate E_T by pedegree is this E or ET. hmmmmm or give it autopedegree
def GenerateE_T(v_set, P):
    E_T = []
    R_set = v_set[0]
    N_set = v_set[1]
    for i in range(len(P)):
        edgeInstance = Edge([int(R_set[i].name),P[i]])        
        edgeInstance.head = P[i]
        edgeInstance.tail = [[int(R_set[i].name)],[P[i][0],int(R_set[i].name)],[P[i][1], int(R_set[i].name)]]    
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
    return E_T
    
    
#create dfRowNames and dfColNames
def GenearteDFLabels(v_set):
    R_set = v_set[0]
    N_set = v_set[1]
    dfRowNames = []
    dfColNames = []
    for i in R_set:
        dfRowNames.append(i.name)

    for i in N_set:
        dfRowNames.append(i)

    for i in N_set:
        dfColNames.append(i)
        
    return dfRowNames, dfColNames
    
#Auto generate Pedegree
def AuthoGeneratePedegree(M_R_size):
    #make random pedegree generator    
    np.random.seed(1)
    Auto_Pedegree = []
    N_list = CreateNset(3)
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
    return Auto_Pedegree
#choose slack variables    
def ChooseSlackVariables(v_set,autoPedegree, M_R_size):
    slack_list = []
    N_set = v_set[1]
    np.random.seed = 2
    for i in xrange(0,M_R_size):
        chosen = np.random.choice(len(N_set),1)
        slack_list.append(N_set[int(chosen)])
        N_set.remove(N_set[int(chosen)])
    return slack_list
    
    
#createDataFrameForIncidenceMatrix
#setting the diagonal 1's
def createDataFrameForIncidenceMatrix(df, dfColNames, dfRowNames, autoPedegree, R_set):
    for i in range(3,len(dfRowNames)):
        indexOfi = dfColNames[0:15].index(dfRowNames[i])    
#        print indexOfi, " ", i
        df[indexOfi][i] = 1
    
    df
#insert the -1 (for the R nodes)    
    for i in R_set:
        colIndexRoot = dfColNames[0:15].index(autoPedegree[R_set.index(i)])
#        print colIndexRoot, " ", autoPedegree[R_set.index(i)][0], " ", autoPedegree[R_set.index(i)][1], " ", R_set[R_set.index(i)].name
        newNode1 = [autoPedegree[R_set.index(i)][0],R_set[R_set.index(i)].name]
        newNode2 = [autoPedegree[R_set.index(i)][1],R_set[R_set.index(i)].name]    
        rowIndexRoot = R_set.index(i)
        rowIndexInsert1 = dfRowNames.index(newNode1)
        rowIndexInsert2 = dfRowNames.index(newNode2)
        df[colIndexRoot][rowIndexRoot] = -1
        df[colIndexRoot][rowIndexInsert1] = -1
        df[colIndexRoot][rowIndexInsert2] = -1
    df
    return df 

def createMatrixForIncidenceMatrix(matrixA, dfColNames, dfRowNames, autoPedegree, R_set):
    #insert +1s
    for i in range(3,len(dfRowNames)):
        indexOfi = dfColNames[0:15].index(dfRowNames[i])    
#        print indexOfi, " ", i
        matrixA[indexOfi][i] = 1
        
    matrixA
    
    #insert -1s
    for i in R_set:
        colIndexRoot = dfColNames[0:15].index(autoPedegree[R_set.index(i)])
#        print colIndexRoot, " ", autoPedegree[R_set.index(i)][0], " ", autoPedegree[R_set.index(i)][1], " ", R_set[R_set.index(i)].name
        newNode1 = [autoPedegree[R_set.index(i)][0],R_set[R_set.index(i)].name]
        newNode2 = [autoPedegree[R_set.index(i)][1],R_set[R_set.index(i)].name]    
        rowIndexRoot = R_set.index(i)
        rowIndexInsert1 = dfRowNames.index(newNode1)
        rowIndexInsert2 = dfRowNames.index(newNode2)
        matrixA[colIndexRoot][rowIndexRoot] = -1
        matrixA[colIndexRoot][rowIndexInsert1] = -1
        matrixA[colIndexRoot][rowIndexInsert2] = -1
        
    matrixA
    #Making M the induced matrix    
    return matrixA
    
    
def addInPlusAndMinusOnesforSlackVariables(df, dfColNames, dfRowNames, R_set):
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
    return df
    
    
def CreateFullEdgeSet(M_R_size, N_set):
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
    
        
#    for p in E_set: print "name ", p.name, "head " ,p.head, "tail", p.tail
    return E_set

def CreateE_X_set(E_set, E_T):
#create list of names in E_T
    E_TnameList = []    
    for i in E_T:
        E_TnameList.append(i.name)
    
    #create E_X 
    E_X =[] 
    for i in xrange(0,len(E_set)):
        if E_set[i].name not in E_TnameList:
            E_X.append(E_set[i])
    
#    len(E_X)
#    for p in E_X: print "name ", p.name, "head " ,p.head, "tail", p.tail
    return E_X
    
    
def makeSpanningTree(df, dfColNames, dfRowNames, v_set, P):    
    Tau_r = []
    R_set = v_set[0]
    #E_T_names = []    
    #for i in E_T: E_T_names.append(i.name)
    #append R
    for i in R_set: Tau_r.append(i)    
    for i in dfColNames[:len(dfColNames)-len(R_set)]:
        if i in P:
            edge = [P.index(i)+4, i]
            node = i
            Tau_r.append(edge)
            Tau_r.append(node)
        else:
            edge = [0, i]
            node = i
            Tau_r.append(edge)
            Tau_r.append(node)
    return Tau_r

def getMR(df, M_R_size, LenN_set):
    M_R = df[0:M_R_size][df.columns[LenN_set:LenN_set+M_R_size]]
    M_R_matrix = M_R.as_matrix()
    return M_R_matrix
    
def initialDemandVector(dfRowNames, P, numCity):
    demand = []
    for i in dfRowNames:
        if i < numCity+1:
            demand.append(1)
        elif i in P:
            demand.append(1)
        else:
            demand.append(0)
    return np.asarray(demand) 