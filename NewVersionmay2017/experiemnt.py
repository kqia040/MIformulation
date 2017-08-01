# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 13:09:49 2017

experiment

@author: Kun
"""
#import time
#
#start = time.time()
#print("hello")
#time.sleep(4)
#end = time.time()
#print(end - start)



import api
import numpy as np
import random
import time

n = 17
V = api.makeVset(n)
R = V[0]
N = V[1]


#dist_dic = d
####hmmmmmmmmmmm maybe its because the len(E_X) is not the same as len(P) in E_T

dist_dic = {}
for v in N:
    dist_dic[v] = random.randint(10, 100)
        
count = 0        
while count < 100:
    start = time.time()   
    len_violate, E_B = api.loop(dist_dic, n, V, R, N)
    end = time.time()
    if len_violate == 0:
        print "done, calculate"
        print "time taken:   ", np.abs(end - start)
        break
    count +=1
    print count

start2 = time.time()
f_lp = api.calculateFlow(E_B, R, N)
cost1 = api.calcCost(f_lp, dist_dic)
cost2 = api.calcCost2(f_lp, dist_dic)
end2 = time.time()
print "number trials is up"
print "violate left", len_violate
print "cost is", cost1, cost2
print "time taken:   ", np.abs(end - start)+np.abs(end2 - start2)









tmp = True
while tmp:
    len_violate, E_B = api.loop(dist_dic, n, V, R, N)
    print len_violate    
    if len_violate == 0:
        break













