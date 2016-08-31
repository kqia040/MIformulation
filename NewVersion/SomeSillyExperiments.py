# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 10:04:56 2016

@author: kqia040
"""
#in tirus paper
import os
os.chdir('C:\\Users\\kqia040\\Documents\\GitHub\\MIformulation\\NewVersion')
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
#41
len(v_set[1])
#861


#Generate Pedgree -> i'm going to cheat here and just use an existing pedgree
P = []
P.append([1,3])
P.append([1,4])
P.append([2,3])

E_T = sp.GenerateE_T(v_set,P)

dfColNames = [[0,[2,6]],[0,[3,6]],[6,[2,3]],[0,[1,5]],[0,[4,5]],
              [5,[1,4]],[0,[3,4]],[4,[1,3]],[0,[1,2]],[0,[2,4]],[0,[2,5]],
                [0,[3,5]],[0,[1,6]],[0,[4,6]],[0,[5,6]],[4,[1,2]],[5,[3,4]],[6,[3,5]]]
                
dfColNames = [[0,[2,6]],[0,[3,6]],[6,[2,3]],[0,[1,5]],[0,[4,5]],
              [5,[1,4]],[0,[3,4]],[4,[1,3]],[0,[1,2]],[0,[2,4]],[0,[2,5]],
                [0,[3,5]],[0,[1,6]],[0,[4,6]],[0,[5,6]]]                
                
                
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