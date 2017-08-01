#dist_dic = {(1, 2): 633,
# (1, 3): 257,
# (1, 4): 91,
# (1, 5): 412,
# (1, 6): 150,
# (1, 7): 80,
# (1, 8): 134,
# (1, 9): 0,
# (1, 10): 249,
# (1, 11): 495,
# (1, 12): 154,
# (1, 13): 435,
# (1, 14): 254,
# (1, 15): 145,
# (1, 16): 57,
# (1, 17): 426,
# (2, 3): 390,
# (2, 4): 661,
# (2, 5): 227,
# (2, 6): 488,
# (2, 7): 572,
# (2, 8): 530,
# (2, 9): 259,
# (2, 10): 505,
# (2, 11): 353,
# (2, 12): 324,
# (2, 13): 70,
# (2, 14): 211,
# (2, 15): 268,
# (2, 16): 0,
# (2, 17): 483,
# (3, 4): 228,
# (3, 5): 169,
# (3, 6): 112,
# (3, 7): 196,
# (3, 8): 154,
# (3, 9): 555,
# (3, 10): 289,
# (3, 11): 282,
# (3, 12): 638,
# (3, 13): 567,
# (3, 14): 466,
# (3, 15): 420,
# (3, 16): 246,
# (3, 17): 121,
# (4, 5): 383,
# (4, 6): 120,
# (4, 7): 77,
# (4, 8): 105,
# (4, 9): 372,
# (4, 10): 262,
# (4, 11): 110,
# (4, 12): 437,
# (4, 13): 191,
# (4, 14): 74,
# (4, 15): 53,
# (4, 16): 745,
# (4, 17): 518,
# (5, 6): 267,
# (5, 7): 351,
# (5, 8): 309,
# (5, 9): 175,
# (5, 10): 476,
# (5, 11): 324,
# (5, 12): 240,
# (5, 13): 27,
# (5, 14): 182,
# (5, 15): 239,
# (5, 16): 472,
# (5, 17): 142,
# (6, 7): 63,
# (6, 8): 34,
# (6, 9): 338,
# (6, 10): 196,
# (6, 11): 61,
# (6, 12): 421,
# (6, 13): 346,
# (6, 14): 243,
# (6, 15): 199,
# (6, 16): 237,
# (6, 17): 84,
# (7, 8): 29,
# (7, 9): 264,
# (7, 10): 360,
# (7, 11): 208,
# (7, 12): 329,
# (7, 13): 83,
# (7, 14): 105,
# (7, 15): 123,
# (7, 16): 528,
# (7, 17): 297,
# (8, 9): 232,
# (8, 10): 444,
# (8, 11): 292,
# (8, 12): 297,
# (8, 13): 47,
# (8, 14): 150,
# (8, 15): 207,
# (8, 16): 364,
# (8, 17): 35,
# (9, 10): 402,
# (9, 11): 250,
# (9, 12): 314,
# (9, 13): 68,
# (9, 14): 108,
# (9, 15): 165,
# (9, 16): 332,
# (9, 17): 29,
# (10, 11): 352,
# (10, 12): 95,
# (10, 13): 189,
# (10, 14): 326,
# (10, 15): 383,
# (10, 16): 349,
# (10, 17): 36,
# (11, 12): 578,
# (11, 13): 439,
# (11, 14): 336,
# (11, 15): 240,
# (11, 16): 202,
# (11, 17): 236,
# (12, 13): 287,
# (12, 14): 184,
# (12, 15): 140,
# (12, 16): 685,
# (12, 17): 390,
# (13, 14): 391,
# (13, 15): 448,
# (13, 16): 542,
# (13, 17): 238,
# (14, 15): 202,
# (14, 16): 157,
# (14, 17): 301,
# (15, 16): 289,
# (15, 17): 55,
# (16, 17): 96}


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
    
    
    
def update_spanning_tree(E_B, e_star, e_prime, f_T, f_X, fbar_T, fbar_X, V):
    #realy just change basis
    R = set(V[0])    
    if e_star[1] is not None:    
        e_star_v_set = {e_star[0], (e_star[0][0],e_star[1]), (e_star[0][1],e_star[1]), e_star[1]}
    elif e_star[0] is None:
        e_star_v_set = {e_star[0]}
    
    if e_star in E_B[1]:
        if (not e_star_v_set.issubset(R)):           
            E_B[1].add(e_prime)
            E_B[1].remove(e_star)
    
        else:
            E_B[1].remove(e_star)
            E_B[0].add(e_prime)
            R.remove(e_star_v_set)
    
    elif e_star in E_B[0]:
        #find critical node
        #check if still spanning tree
        copy_e_star_v_set = copy.deepcopy(e_star_v_set)       
        for e in E_B[0]:
            if e == e_star:
                continue

            if e[1] is not None:
                temp_e_v_set = {e[0], (e[0][0],e[1]), (e[0][1],e[1]), e[1]}
            elif e[1] is None:
                temp_e_v_set = {e[0]}
                
            for v in temp_e_v_set:
                if v in copy_e_star_v_set:
                    copy_e_star_v_set.remove(v)
            
            if len(copy_e_star_v_set) == 0:
                #means that we can remove this edge
                E_B[0].remove(e_star)
                E_B[0].add(e_prime)
                       
        for e in E_B[1]:
            temp_e_v_set = {e[0], (e[0][0],e[1]), (e[0][1],e[1]), e[1]}
            if copy_e_star_v_set.issubset(copy_e_star_v_set):
                e_bar = e
        
        E_B[0].add(e_bar)
        E_B[1].remove(e_bar)
        E_B[1].add(e_prime)
        E_B[0].remove(e_star)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    