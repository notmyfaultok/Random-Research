import random
import networkx as nx
from networkx.algorithms.isomorphism.isomorph import graph_could_be_isomorphic as isomorphic
from networkx.generators.atlas import graph_atlas_g
from itertools import product
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import itertools

# Exponential graph Node
class ExpNode:
    def __init__(self, label, value):
        self.label =label
        self.value =value
        
    def __str__(self):
        return str(self.label)


# create exponential graph E_num(g)
def createExpGraphNum( g,num): 
    resultG=nx.Graph()
    X=set(list(g.nodes))
    Y=set(list(range(num)))
    node_list = [dict(zip(X,y)) for y in product(Y,repeat=len(X))]
    for i in range(len(node_list)):
        resultG.add_node(ExpNode(i,node_list[i]))
    #add edges
    for nodeMapsrc in resultG.nodes:
        for nodeMapsnk in resultG.nodes:
            if nodeMapsrc==nodeMapsnk:
                continue
            else:
                isEdge=True
                for edge in g.edges:
                    if (nodeMapsrc.value[edge[0]] == nodeMapsnk.value[edge[1]]) or (nodeMapsrc.value[edge[1]] == nodeMapsnk.value[edge[0]]):
                        isEdge=False
                        break
                if isEdge:
                    resultG.add_edge(nodeMapsrc,nodeMapsnk)
    return resultG


# Create exponential graph h^g
def createExpGraph(h,g):
    resultG = nx.Graph()
    X= set(list(g.nodes))
    Y= set(list(h.nodes))
    node_list = [dict(zip(X,y)) for y in product(Y, repeat=len(X))]
        # add the nodes
    for i in range(len(node_list)):
        resultG.add_node(ExpNode(i,node_list[i]))
    #add edges
    for nodeMapsrc in resultG.nodes:
        for nodeMapsnk in resultG.nodes:
            if nodeMapsrc==nodeMapsnk:
                continue
            else:
                isEdge=True
                for edge in g.edges:
                    if (not(h.has_edge(nodeMapsrc.value[edge[0]],nodeMapsnk.value[edge[1]]))  or  not(h.has_edge(nodeMapsrc.value[edge[1]],nodeMapsnk.value[edge[0]]))):
                        isEdge=False
                        break
                if isEdge:
                    resultG.add_edge(nodeMapsrc,nodeMapsnk)
    return resultG

# method to verify if a coloring of an exponential graph is proper
def isSafe(g, c):
    for edge in g.edges:
        if c[edge[0]] == c[edge[1]]:
            return False
    return True

# method to compute a suited proper coloring using backtracking
def suitedColorExpG( g,n,i,c={}):
    if i == len(g.nodes):
        if isSafe(g,c):
            return (True, c)
        return (False, c)
    nodesList= list(g.nodes)
    for j in range(n):
        if len(set(nodesList[i].value.values())) == 1: # check if node is a constant map and assigne its value if it is
            c[nodesList[i]] = nodesList[i].value[1]
        else:
            c[nodesList[i]]=j
        if suitedColorExpG( g,n,i+1,c)[0]:
            return (True, c)
    print("Fail to find a suited proper coloring")
    return (False, c)
