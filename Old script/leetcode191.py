# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 12:17:01 2017

@author: Kun
"""
# Python program for printing vertical order of a given
# binary tree
 
# A binary tree node
class Node:
    # Constructor to create a new node
    def __init__(self, key):
        self.val = key
        self.left = None
        self.right = None
 
# Utility function to store vertical order in map 'm' 
# 'hd' is horizontal distance of current node from root
# 'hd' is initially passed as 0

    # @param A : root node of tree
    # @return a list of list of integers
class Solution:
    def TraversalR(self, root):

        def traverse(root):
            if root.left is None and root.right is None:
                values.append(root.val)
                return
            
            values.append(root.val)
            if root.left:    
                traverse(root.left)
                
            
            
            if root.right:
                traverse(root.right)
                
            
            
        
        values = []                
        traverse(root)
        return values
        
#inorder
#    def TraversalI(self, root):
#        ret = []
#        s = []
#        cnode = root
#        while(len(s)!=0 or cnode):
#            if cnode:
#                s.append(cnode)
#                cnode = cnode.left
#            else:
#                tmp = s.pop(-1)
#                ret.append(tmp.val)
#                cnode = tmp.right
#        return ret
#post order
#    def TraversalI(self, root):
#        ret = []
#        s = [root]
#        while(len(s)!=0):
#            tmp = s.pop(-1)
#            if tmp.left:            
#                s.append(tmp.left)
#            if tmp.right:
#                s.append(tmp.right)
#            ret.append(tmp.val)
#        return ret[::-1]     
#preorder
    def TraversalI(self, root):
        ret = []
        s = []
        while(len(s)!=0 or root is not None):
            if root is None:
                root = s.pop(-1)
            else:
                ret.append(root.val)
                if root.right is not None:
                    s.append(root.right)
                root = root.left
        return ret
        
# Driver program to test above function
#root = Node(1)
#root.left = Node(2)
#root.right = Node(3)
#root.left.left = Node(4)
#root.left.right = Node(5)
#root.right.left = Node(6)
#root.right.right = Node(7)
#root.right.left.right = Node(8)
#root.right.right.right = Node(9)
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)

s = Solution()
print "R", s.TraversalR(root)
print "I", s.TraversalI(root)