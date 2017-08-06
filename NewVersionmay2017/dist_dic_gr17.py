dist_dic = {(1, 2): 30, 
             (1, 3): 26,
             (2, 3): 24,
             (1, 4): 50,
             (2, 4): 40,
             (3, 4): 24,
            (1,5): 40,
            (2,5): 50,
            (3,5): 26,
            (4,5): 30}
 
def newdual2(E_B,dist_dic,V):
    R = copy.deepcopy(V[0])
    N = copy.deepcopy(V[1])
    pi_dl = dict.fromkeys(set(R+N), None)
    xijkset = set()
    pivector = R
    #Vtail = set()
    for e in E_B[0]:
        if e[1] is None:
            pi_dl[e[0]] = dist_dic[e[0]]
    #    else:
    #        xijkset.add(e)
    #        pivector.append(e[0])
    for v in N:
        if (v,None) not in E_B[0]:
            pivector.append(v)
    
    for e in E_B[0]:
        if e[1] is not None:
            xijkset.add(e)
            
            
    xijkset = xijkset.union(E_B[1])
        
    MMM = np.zeros([len(xijkset),len(xijkset)])
    rhs = np.zeros(len(xijkset))
    
    
    counter = 0
    for e in xijkset:
        temp = 0
        if e[0] in pivector:
            #head so its -1
            MMM[counter][pivector.index(e[0])] = -1
    
        else:
            temp += pi_dl[e[0]]
            
        if (e[0][0],e[1]) in pivector:
            MMM[counter][pivector.index((e[0][0],e[1]))] = 1
            
        else:
            temp -= pi_dl[(e[0][0],e[1])]
        
        if (e[0][1],e[1]) in pivector:
            MMM[counter][pivector.index((e[0][1],e[1]))] = 1
            
        else:
            temp -= pi_dl[(e[0][1],e[1])]
            
        if e[1] in pivector:
            #head so its -1
            MMM[counter][pivector.index(e[1])] = 1
    
        else:
            temp -= pi_dl[e[1]]
        
        rhs[counter] = temp
        counter +=1
            
        
    sol = np.linalg.solve(MMM,rhs)
    counter = 0
    for v in pivector:
        pi_dl[v] = sol[counter]
        counter+=1
        
    return pi_dl

def find_e_star(E_B, e_prime):
    E_T = E_B[0]
    E_X = E_B[1]
    r = list(R)+list(N)
    c = list(E_T) + list(E_X)
    len_R = len(R)
    len_N = len(N)
    e_star_dic = set() 
    M = np.zeros([len_R+len_N,len_R+len_N])
    for cc in range(len(c)):
        if c[cc][1] is None:
            ij = r.index(c[cc][0])
            M[ij][cc] = 1
        else:
            ij = r.index(c[cc][0])
            k = r.index(c[cc][1])
            ik = r.index((c[cc][0][0],c[cc][1]))
            jk = r.index((c[cc][0][1],c[cc][1]))
            M[ij][cc] = 1
            M[k][cc] = -1
            M[ik][cc] = -1
            M[jk][cc] = -1
    
    M_eprime = np.zeros(len_R+len_N)
    
    if e_prime[1] is None:
        ij = r.index(e_prime[0])
        M_eprime[ij] = 1
    else:
        ij = r.index(e_prime[0])
        k = r.index(e_prime[1])
        ik = r.index((e_prime[0][0],e_prime[1]))
        jk = r.index((e_prime[0][1],e_prime[1]))
        M_eprime[ij] = 1
        M_eprime[k] = -1
        M_eprime[ik] = -1
        M_eprime[jk] = -1
    
    
    correct_rank = np.linalg.matrix_rank(M)
    counter = 0
    while counter<(len_R+len_N):
        cols = range(len_R+len_N)    
        cols.remove(counter)
        M[:,cols]
        test_rank = np.linalg.matrix_rank(np.c_[M[:,cols],M_eprime])
        if test_rank == correct_rank:
            e_star_dic.add(c[counter])
        counter+=1
    

    return e_star_dic
    
def lp_find_flow(E_B, V, rhs_indicator):
    R = V[0]
    N = V[1]    
    r = R+N
    E_T = E_B[0]
    E_X = E_B[1]    
    c = list(E_T) + list(E_X)
    M = np.zeros([len(R)+len(N),len(R)+len(N)])
    for cc in range(len(c)):
        if c[cc][1] is None:
            ij = r.index(c[cc][0])
            M[ij][cc] = 1
        else:
            ij = r.index(c[cc][0])
            k = r.index(c[cc][1])
            ik = r.index((c[cc][0][0],c[cc][1]))
            jk = r.index((c[cc][0][1],c[cc][1]))
            M[ij][cc] = 1
            M[k][cc] = -1
            M[ik][cc] = -1
            M[jk][cc] = -1  
    
    b = np.zeros(len(r))
    if rhs_indicator == 'default':    
        for i in range(len(r)):
            if r[i] in R:
                b[i] = -1
            elif r[i] == (1,2) or r[i] == (1,3) or r[i] == (2,3):
                b[i] = 1
            else:
                b[i] = 0
    else:
        #we get an edge ((ij)k) or ((ij) None)
        if rhs_indicator[1] is None:
            for i in range(len(r)):
                if r[i] == rhs_indicator[0]:
                    b[i] = -1
        else:
            ij = rhs_indicator[0]
            k = rhs_indicator[1]
            ik = (rhs_indicator[0][0], rhs_indicator[1])  
            jk = (rhs_indicator[0][1], rhs_indicator[1]) 
            for i in range(len(r)):
                if r[i] == ij:
                    b[i] = -1
                elif r[i] == k or r[i] == ik or r[i] == jk:
                    b[i] = 1

    
    f = np.dot(np.linalg.inv(M),b)
   
    f_lp = {}
    for i in range(len(f)):
        f_lp[c[i]] = f[i]
    
    return f_lp
    
    
    
#def update_spanning_tree(E_B, e_star, e_prime, f_T, f_X, fbar_T, fbar_X, V):
#    #realy just change basis
#    R = set(V[0])    
#    if e_star[1] is not None:    
#        e_star_v_set = {e_star[0], (e_star[0][0],e_star[1]), (e_star[0][1],e_star[1]), e_star[1]}
#    elif e_star[0] is None:
#        e_star_v_set = {e_star[0]}
#    
#    if e_star in E_B[1]:
#        if (not e_star_v_set.issubset(R)):           
#            E_B[1].add(e_prime)
#            E_B[1].remove(e_star)
#    
#        else:
#            E_B[1].remove(e_star)
#            E_B[0].add(e_prime)
#            R.remove(e_star_v_set)
#    
#    elif e_star in E_B[0]:
#        #find critical node
#        #check if still spanning tree
#        copy_e_star_v_set = copy.deepcopy(e_star_v_set)       
#        for e in E_B[0]:
#            if e == e_star:
#                continue
#
#            if e[1] is not None:
#                temp_e_v_set = {e[0], (e[0][0],e[1]), (e[0][1],e[1]), e[1]}
#            elif e[1] is None:
#                temp_e_v_set = {e[0]}
#                
#            for v in temp_e_v_set:
#                if v in copy_e_star_v_set:
#                    copy_e_star_v_set.remove(v)
#            
#            if len(copy_e_star_v_set) == 0:
#                #means that we can remove this edge
#                E_B[0].remove(e_star)
#                E_B[0].add(e_prime)
#                       
#        for e in E_B[1]:
#            temp_e_v_set = {e[0], (e[0][0],e[1]), (e[0][1],e[1]), e[1]}
#            if copy_e_star_v_set.issubset(copy_e_star_v_set):
#                e_bar = e
#        
#        E_B[0].add(e_bar)
#        E_B[1].remove(e_bar)
#        E_B[1].add(e_prime)
#        E_B[0].remove(e_star)
#    
#    
#    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    