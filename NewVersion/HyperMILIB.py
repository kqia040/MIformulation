# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 08:49:42 2016

@author: kqia040
"""

#Starting week6 sem2
#Containing all the code for the MI project
#importing libs
import numpy as np
from collections import deque

import sys
sys.path.append('C:\Users\kqia040\Documents\GitHub\MIformulation')
import Support as sp

#Import TSPLIB matrix

#set path of the file
path1 = "swiss42.tsp"
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
for i in range(1,42):
    x = Vertex()
    x.name = i
    R_set.append(x)

#creates N set
a, N_set = sp.calcPerm(42)

#Create V with R and N
v_set.append(R_set)
v_set.append(N_set)

#example reading it
len(v_set[0])
#41
len(v_set[1])
#861



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
