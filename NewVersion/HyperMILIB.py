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

#Import TSPLIB matrix

#set path of the file
path1 = "brazil58.tsp"

def read_tsp_file(path):
    tspfile = open(path,'r')
    details = tspfile.readlines()
    tspfile.close()
    return details
    
aa = read_tsp_file(path1)

def minimal_tsp():
    return { "COMMENT"          : ""
           , "DIMENSION"        : None
           , "TYPE"             : None
           , "EDGE_WEIGHT_TYPE" : None
           , "CITIES"           : []}

def scan_keywords(tsp,tspfile):
    for line in tspfile:
        words   = deque(line.split())
        keyword = words.popleft().strip(": ")

        if keyword == "COMMENT":
            tsp["COMMENT"] += " ".join(words).strip(": ")
        elif keyword == "NAME":
            tsp["NAME"] = " ".join(words).strip(": ")
        elif keyword == "TYPE":
            tsp["TYPE"] = " ".join(words).strip(": ")
        elif keyword == "DIMENSION":
            tsp["DIMENSION"] = int(" ".join(words).strip(": "))
        elif keyword == "EDGE_WEIGHT_TYPE":
            tsp["EDGE_WEIGHT_TYPE"] = " ".join(words).strip(": ")
        elif keyword == "NODE_COORD_SECTION":
            break
        
def read_cities(tsp,tspfile):
    for n in range(1, tsp["DIMENSION"] + 1):
        line  = tspfile.readline()
        words = deque(line.split())
        if tsp["EDGE_WEIGHT_TYPE"] == "EXPLICIT":
            tsp["CITIES"].append(read_numbered_euc_2d_city_line(n, words))
        elif tsp["EDGE_WEIGHT_TYPE"] == "GEO":
            tsp["CITIES"].append(read_numbered_geo_city_line(n, words))
        else:
            print("Unsupported coordinate type: " + tsp["EDGE_WEIGHT_TYPE"])        

#Create V set
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
