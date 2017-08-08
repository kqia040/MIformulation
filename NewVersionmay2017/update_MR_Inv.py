# -*- coding: utf-8 -*-
"""
Created on Sun Aug 06 15:48:01 2017

@author: Kun
"""
#v_bar is v_bar_e_star
import primal
import numpy as np
def update_MR_inv(Case, MR_inv, V, newV, E_B, newE_B, e_prime, e_star, fbar_T, fbar_X):
    #essentially, we are just returning a cbinded matrix, a column for each e_X    
    print "case is ", Case    
    if newV is None:
        newV = V
    newR = newV[0]
    R = V[0]
    N = V[1]
    len_newR = len(newR)
#    temp_matrix = np.zeros([len_newR,len_newR])
    
    if Case == '1a':
        temp_matrix = np.zeros([len_newR,len_newR])
        #in the first iteration here
        #e_star is e_bar
        #e_prime is e_star        
        for v in newR:
            for e in newE_B[1]:
                if e == e_prime:
                    temp_val = -1*((MR_inv[E_B[1].index(e_star)][newR.index(v)])/fbar_X[e_star])
                    temp_matrix[newE_B[1].index(e)][newR.index(v)] = temp_val
                else:
                    #all the e is in existing E_X but v not be in existing R
                    temp_val = MR_inv[E_B[1].index(e)][V[0].index(v)] - (((MR_inv[E_B[1].index(e_star)][newR.index(v)])/fbar_X[e_star])*fbar_X[e])
                    temp_matrix[newE_B[1].index(e)][newR.index(v)] = temp_val
            
            
                    
        return temp_matrix 
        
    elif Case == '1b':
        temp_matrix = np.zeros([len_newR,len_newR])
        for v in newR:
            for e in newE_B[1]:
                    #all the e is in existing E_X but v not be in existing R
                    temp_val = MR_inv[E_B[1].index(e)][V[0].index(v)] - (((MR_inv[E_B[1].index(e_star)][newR.index(v)])/fbar_X[e_star])*fbar_X[e])
                    temp_matrix[newE_B[1].index(e)][newR.index(v)] = temp_val
            
            
                    
        return temp_matrix 
        
        
        
    elif Case == '2a':
        temp_matrix = np.zeros([len_newR,len_newR])
        #in the first iteration here
        #e_star is e_bar
        #e_prime is e_star      
        fbar_e_star = None
        if e_star in fbar_X:
            fbar_e_star = fbar_X[e_star]
        elif e_star in fbar_T:
            fbar_e_star = fbar_T[e_star]        

        for v in newR:
            for e in newE_B[1]:       
                if e == e_prime:    
                    temp_val = -1*((MR_inv[E_B[1].index(e_star)][newR.index(v)])/fbar_e_star)
                    temp_matrix[newE_B[1].index(e)][newR.index(v)] = temp_val
                else:
                    #all the e is in existing E_X but v not be in existing R
                    temp_val = MR_inv[E_B[1].index(e)][V[0].index(v)] - (((MR_inv[E_B[1].index(e_star)][newR.index(v)])/fbar_e_star)*fbar_X[e])
                    temp_matrix[newE_B[1].index(e)][newR.index(v)] = temp_val
            

        return temp_matrix 

#    elif Case == '2a-1st':
#        temp_matrix = np.zeros([len_newR,len_newR])
#        #in the first iteration here
#        #e_star is e_bar
#        #e_prime is e_star      
#        fbar_e_star = None
#        if e_prime in fbar_X:
#            fbar_e_star = fbar_X[e_prime]
#        elif e_prime in fbar_T:
#            fbar_e_star = fbar_T[e_prime]        
#
#        for v in newR:
#            temp_R = dict.fromkeys(V[0], 0)
#            temp_N = dict.fromkeys(V[1], 0)
#            if v in R:
#                temp_R[v] = 1
#            elif v in N:
#                temp_N[v] = 1
#            temp_bar = [temp_R, temp_N]
#            phi_T, phi_X = primal.Primal(V, E_B, MR_inv, temp_bar)
#            
#            
#            for e in newE_B[1]:       
#                if e == e_prime:    
#                    temp_val = -1*((phi_T[e_prime])/fbar_e_star)
#                    temp_matrix[newE_B[1].index(e)][newR.index(v)] = temp_val
#                else:
#                    #all the e is in existing E_X but v not be in existing R
#                    temp_val = MR_inv[E_B[1].index(e)][V[0].index(v)] - (((phi_T[e_prime])/fbar_e_star)*fbar_X[e])
#                    temp_matrix[newE_B[1].index(e)][newR.index(v)] = temp_val
#                    
#
#
#        return temp_matrix
#   
#    elif Case == '2a-2nd':
#        temp_matrix = np.zeros([len_newR,len_newR])
#        #in the first iteration here
#        #e_star is e_bar
#        #e_prime is e_star      
#        fbar_e_star = None
#        if e_star in fbar_X:
#            fbar_e_star = fbar_X[e_star]
#        elif e_star in fbar_T:
#            fbar_e_star = fbar_T[e_star]        
#
#        for v in newR:
#            for e in newE_B[1]:       
#                if e == e_prime:    
#                    temp_val = -1*((MR_inv[E_B[1].index(e_star)][newR.index(v)])/fbar_e_star)
#                    temp_matrix[newE_B[1].index(e)][newR.index(v)] = temp_val
#                else:
#                    #all the e is in existing E_X but v not be in existing R
#                    temp_val = MR_inv[E_B[1].index(e)][V[0].index(v)] - (((MR_inv[E_B[1].index(e_star)][newR.index(v)])/fbar_e_star)*fbar_X[e])
#                    temp_matrix[newE_B[1].index(e)][newR.index(v)] = temp_val
#            
#
#        return temp_matrix
        
        
    elif Case == '2b1':
        #thing e_prime replace e_star as tree arc, E_X does not change
        #MR_inv does not change
        temp_matrix = np.zeros([len_newR,len_newR])       
        for v in newR:
            temp_R = dict.fromkeys(V[0], 0)
            temp_N = dict.fromkeys(V[1], 0)
            if v in R:
                temp_R[v] = 1
            elif v in N:
                temp_N[v] = 1
            temp_bar = [temp_R, temp_N]
            phi_T, phi_X = primal.Primal(V, E_B, MR_inv, temp_bar)
            
            for e in newE_B[1]:
                #all the e is in existing E_X but v not be in existing R
                temp_val = MR_inv[E_B[1].index(e)][V[0].index(v)] - (((phi_T[e_star])/fbar_T[e_star])*fbar_X[e])
                temp_matrix[newE_B[1].index(e)][newR.index(v)] = temp_val
    
            
                    
        return temp_matrix            
        
        
    elif Case == '2b2':
        #v_bar is the node that gets added to R
#        col_num = E_X_list.index(e_star)
        
        #v_bar should have already been added to R        
        #i thin kthat e_prime is already added to E_X_list        
#        E_X_list.append(e_prime)    
        temp_matrix = np.zeros([len_newR,len_newR])
        for v in newR:
            temp_R = dict.fromkeys(V[0], 0)
            temp_N = dict.fromkeys(V[1], 0)
            if v in R:
                temp_R[v] = 1
            elif v in N:
                temp_N[v] = 1
            temp_bar = [temp_R, temp_N]
            phi_T, phi_X = primal.Primal(V, E_B, MR_inv, temp_bar)
            
            for e in newE_B[1]:
                if e == e_prime:
                    temp_val = -1*((phi_T[e_star])/fbar_T[e_star])
                    temp_matrix[newE_B[1].index(e)][newR.index(v)] = temp_val
                else:
                    #all the e is in existing E_X but v not be in existing R
                    if v in R:
                        temp_val = MR_inv[E_B[1].index(e)][V[0].index(v)] - (((phi_T[e_star])/fbar_T[e_star])*fbar_X[e])
                        temp_matrix[newE_B[1].index(e)][newR.index(v)] = temp_val
            
                    else:
                        temp_val = (phi_X[e]) - (((phi_T[e_star])/fbar_T[e_star])*fbar_X[e])
                        temp_matrix[newE_B[1].index(e)][newR.index(v)] = temp_val
            
                    
        return temp_matrix            
                        
