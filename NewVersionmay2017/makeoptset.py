# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 14:58:26 2017

@author: Kun
"""

iii = 1
jjj = 2
opt = []
while jjj<11:
    opt.append((iii,jjj))
    iii+=1
    jjj+=1

opt.append((1,jjj-1))


cost = 0
for e in f_T:
    if f_T[e] > 0 and e[1] is None:
        cost+= 1 * dist_dic[e[0]]
            
print cost

asd = []
for e in E_T:
    if e[1] is not None:
        asd.append(e)
print asd

iu = 0
for e in E_T:
    if e[1] is None:
        iu+=1
print iu


filename = "data/Matrix_Input/gr17.tsp"
    
f = open(filename, "r")
lines = f.readlines()
f.close()

starting_index = lines.index('EDGE_WEIGHT_SECTION\n') + 1
if 'DISPLAY_DATA_SECTION\n' in lines:
    ending_index = lines.index('DISPLAY_DATA_SECTION\n') - 1
else:
    ending_index = -2

dis_data = lines[starting_index:ending_index]



templist = []

for i in range(len(dis_data)):
    templist+=dis_data[i].split(' ')


#ttlist = []
#for i in templist:
#    if i != '' and i!='0' and i!='0\n':
#        if '\n' in i:        
#            ttlist.append(i[:-1])
#        else:
#            ttlist.append(i)
#            

keylist = []
n = 17
j = 2

while j < n+1:
    i = 1
    while i <j:
        keylist.append((i,j))
        i+=1
    j+=1
            
            


#aaa= bbb
ll = aaa.split(' ')
tt =[]
for i in ll:
    if i!='0' and i!='\n0' and i!='' and i!='0':
        tt.append(i)

d = {}
for counter in range(len(keylist)):
    d[keylist[counter]] = int(tt[counter])
    
    
    










rrr = []
for e in f_T:
    if f_T[e] != 0:
        rrr.append(e)





len(rrr)
cost = 0
for e in rrr:
    cost+=f_T[e]*dist_dic[e[0]]

print cost


















    