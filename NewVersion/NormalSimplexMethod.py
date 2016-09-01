# -*- coding: utf-8 -*-
"""
Created on Thu Sep 01 09:49:34 2016

@author: kqia040
"""
import numpy as np

B = np.mat([[1,1,0,0],[1,0,0,0],[0,1,1,0],[0,1,0,1]])

from numpy.linalg import inv
BInv = inv(B)

A = np.mat([[1,1,1,1,0,0,0,],[1,0,0,0,1,0,0],[0,0,1,0,0,1,0],[0,3,1,0,0,0,1]])

b = np.array([[4,2,3,6]])
b = b.T

#second column of A
A[:,[1]]

c = np.array([[1,5,-2,0,0,0,0]])
cB = np.array([[1,-2,0,0]])
cB
0 - cB*BInv*A[:,[3]]

for i in xrange(0,len(c)):
    print c[i] - cB*BInv*A[:,[i]]
    
    
