# -*- coding: utf-8 -*-
"""
Created on Sun Aug 06 15:48:30 2017

@author: Kun
"""
import copy
from update_MR_Inv import update_MR_inv
import api

def update_spanning_tree(E_B, MR_inv, V, e_prime, e_star, fbar_T, fbar_X):
    #ebar is the cirtical edge
    Case = None
    R = V[0]
    N = V[1]    
#    RR = set(V[0])    
    if e_star[1] is not None:    
        e_star_head_tail_set_union = {e_star[0], (e_star[0][0],e_star[1]), (e_star[0][1],e_star[1]), e_star[1]}
    elif e_star[1] is None:
        e_star_head_tail_set_union = {e_star[0]}
    #case1
    if e_star in E_B[1]:
        if (not e_star_head_tail_set_union.issubset(R)):           
            Case = '1a'
            newV = None
            newE_B = copy.deepcopy(E_B)
            newE_B[1][newE_B[1].index(e_star)] = e_prime
            newMR_inv = update_MR_inv(Case, MR_inv, V, newV, E_B, newE_B, e_prime, e_star, fbar_T, fbar_X)
            return newE_B, V, newMR_inv
        else:
            #this case will never happen
#==============================================================================
#           need to select node in R to remove            
#==============================================================================
            tempset = copy.deepcopy(e_star_head_tail_set_union)
            v_remove_from_R = None            
            for v in R:
                if v in tempset:
                    v_remove_from_R = v
                    break
            if v_remove_from_R is None:
                print "errrrrrorrr, at v_remove from R for case 1b" 
            Case = '1b'
            newV = copy.deepcopy(V)
            newR = newV[0]
            newE_B = copy.deepcopy(E_B)
            newE_B[1].remove(e_star)
            newE_B[0].append(e_prime)
            newR.remove(v_remove_from_R)
            newMR_inv = update_MR_inv(Case, MR_inv, V, newV, E_B, newE_B, e_prime, e_star, fbar_T, fbar_X)            

            
            return newE_B, newV, newMR_inv
        
    elif e_star in E_B[0]:
        #if e is a tree arc
        
        #if e_bar
        #if critical edge exisits        
        T_R, e_list, v_list = api.traverse(E_B, V)
        e_bar = api.find_e_bar(E_B, v_list, e_star)
        
#==============================================================================
#         NEED TO CHECK THIS CASE
#==============================================================================
        
        if e_bar is not None:
            #here need to update the E_B 
            Case = '2a'
            newV = None
            intermediateE_B = copy.deepcopy(E_B)
            intermediateE_B[0][intermediateE_B[0].index(e_star)] = e_bar
            intermediateE_B[1][intermediateE_B[1].index(e_bar)] = e_star
            intermediateMR_inv = update_MR_inv(Case, MR_inv, V, newV, E_B, intermediateE_B, e_star, e_bar, fbar_T, fbar_X)
#            Case = '2a-second-iteration'
            newE_B = copy.deepcopy(intermediateE_B)
            newE_B[1][newE_B[1].index(e_star)] = e_prime
            newMR_inv = update_MR_inv(Case, intermediateMR_inv, V, newV, intermediateE_B, newE_B, e_prime, e_star, fbar_T, fbar_X)
                    

            return newE_B, newV, newMR_inv


        #if tehre is no critical edge!
        else:
            len_v_list = len(v_list)            
            v_bar_e_prime = None
            v_bar_e_star = None            
            if e_prime[1] is not None:
                temp_e_prime_v_set = {e_prime[0], (e_prime[0][0],e_prime[1]), (e_prime[0][1],e_prime[1])}
            elif e_prime[1] is None:
                temp_e_prime_v_set = {e_prime[0]}
                
            for i in range(len_v_list-1,-1,-1):
                if v_list[i] in temp_e_prime_v_set:
                    v_bar_e_prime = v_list[i]
                    break
            
            if e_star[1] is not None:
                temp_e_star_v_set = {e_star[0], (e_star[0][0],e_star[1]), (e_star[0][1],e_star[1])}
            elif e_star[1] is None:
                temp_e_star_v_set = {e_star[0]}

            for i in range(len_v_list-1,-1,-1):
                if v_list[i] in temp_e_star_v_set:
                    v_bar_e_star = v_list[i]
                    break
                
            #here is where the real case a or b starts
            if v_bar_e_prime == v_bar_e_star:
                #eprime replace estar as a tree arc
                Case = '2b1'
                newV = copy.deepcopy(V) 
                newE_B = copy.deepcopy(E_B)  
                newE_B[0].append(e_prime)
                newE_B[0].remove(e_star)
                
                newMR_inv = update_MR_inv(Case, MR_inv, V, newV, E_B, newE_B, e_prime, e_star, fbar_T, fbar_X)
                    

                return newE_B, newV, newMR_inv

                
            else:
                #the last case 2b2
                #case1
                if not(temp_e_prime_v_set.issubset(V[0])):
                    newV = copy.deepcopy(V)                    
                    newV[0].append(v_bar_e_star)
                    newV[1].remove(v_bar_e_star)
                    Case = '2b2'
                    newE_B = copy.deepcopy(E_B)   
                    newE_B[1].append(e_prime)
                    newE_B[0].remove(e_star)
                    
                    newMR_inv = update_MR_inv(Case, MR_inv, V, newV, E_B, newE_B, e_prime, e_star, fbar_T, fbar_X)
                    

                    return newE_B, newV, newMR_inv
                else:
                    newV = copy.deepcopy(V)                    
                    newE_B = copy.deepcopy(E_B) 
                    for v in temp_e_prime_v_set:
                        if v in V[0]:
                            newV.remove(v)
                            newV.append(v_bar_e_star)
                            break
                    
                    newE_B[0].append(e_prime)
                    newE_B[0].remove(e_star)
                    Case = '2b2'                    
                    newMR_inv = update_MR_inv(Case, MR_inv, V, newV, E_B, newE_B, e_prime, e_star, fbar_T, fbar_X)
                    

                    return newE_B, newV, newMR_inv