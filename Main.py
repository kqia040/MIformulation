# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 08:35:48 2016
This script will execute calculations
@author: kqia040
"""

import Support as sp
import numpy as np
from gurobipy import *


Matrix, b, c, s, constraintCost, constraint = calculateSTSP(5)

try:
    # Create a new model
    m = Model("mip1")
    # Create variables
    constraintCost = m.addVar(vtype=GRB.BINARY, name="constraintCost")
    
    # Integrate new variables
    m.update()
    # Set objective
    m.setObjective(constraintCost, GRB.MINIMISE)
    # Add constraint: x + 2 y + 3 z <= 4
    for i in range(len(constraint)):
        m.addConstr(constraint["constraint_{0}".format(i)] = b[i], "c0")
   
    m.optimize()
    
    for v in m.getVars():
        print v.varName, v.x
        print 'Obj:', m.objVal
except GurobiError:
    print 'Error reported'

#c = sp.InitiateA_nMatrix(5)
#print c.shape

#a, b = sp.calcPerm(5)

#d={}
#d = sp.MakeDictionaryOfEnVectors(6)
#b = MakeMatrixEn(d)
##print b
#matrix_size = len(d)+3
#print matrix_size
#b= np.row_stack((d["e_4"],d["e_5"]))
#for x in xrange(5,matrix_size):
#    b = np.row_stack((b,d["e_{0}".format(x+1)]))
#print b    
#print np.stack((d["e_4"],d["e_5"]))
