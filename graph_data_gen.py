#### For generating all functions from A to B: https://stackoverflow.com/questions/28649683/a-list-of-all-functions-from-x-to-y-in-python
# SQL tutorial: https://www.geeksforgeeks.org/sql-using-python/

import sqlite3 
import random
import networkx as nx
from networkx.algorithms.isomorphism.isomorph import graph_could_be_isomorphic as isomorphic
from networkx.generators.atlas import graph_atlas_g
from itertools import product

class Node:
    def __init__(self, label, value):
        self.label =label
        self.value =value
        
    def __str__(self):
        return self.label+""


def createExpGraph( g,num): 
    resultG=nx.Graph()
    X=set(list(g.nodes))
    Y=set(list(range(num)))
    node_list = [dict(zip(X,y)) for y in product(Y,repeat=len(X))]
    # add the nodes
    for i in range(len(node_list)):
        resultG.add_node(Node(i,node_list[i]))
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
   
def isRegular( g):
    degl= g.degree()
    return int(all(elem == list(degl)[0][1] for elem in [d for n, d in list(degl)]))

def numOfTriangles( g):
    return sum(list(nx.triangles(g).values()))/3
    
def maxDegree(g):
    degl= g.degree()
    return max([d for n, d in list(degl)])

def minDegree(g):
    degl= g.degree()
    return min([d for n, d in list(degl)])

def avgDegree(g):
    degl=g.degree()
    l=[d for n, d in list(degl)]
    return sum(l)/len(l)

def diam(g):
    try:
        return nx.diameter(g)
    except nx.NetworkXError:
        return -1

if __name__ == "__main__":
    
    #make a database of examples:
    connection = sqlite3.connect("sixvertexorle.db")
    
    # cursor  
    crsr = connection.cursor() 

    # SQL command to create a table in the database 
    sql_command = """CREATE TABLE grahhhhhh (  
    c INTEGER,
    n_verticesO INTEGER,  
    n_edgesO INTEGER,
    n_edgesE INTEGER,
    maxDegO INTEGER,
    maxDegE INTEGER,
    avrgDegO INTEGER,
    avrgDegE INTEGER,
    minDegO INTEGER,
    minDegE INTEGER,
    diameterO INTEGER,
    diameterE INTEGER,
    isRegularO INTEGER,
    isRegularE INTEGER,
    numTriangleO INTEGER,
    numTriangleE INTEGER,
    isConnectedO INTEGER,
    isConnectedE INTEGER,
    isPlanarO INTEGER,
    isPlanarE INTEGER);"""

    # execute the statement 
    crsr.execute(sql_command) 
    
    Atlas = graph_atlas_g()[1:46] 
    for G in Atlas:
        for i in range(4): # c values
            expG = createExpGraph( G, i+1)
            cc = i+1
            cn_verticesO = len(G)  
            cn_edgesO = G.number_of_edges()
            cn_edgesE = expG.number_of_edges()
            cmaxDegO = maxDegree(G)
            cmaxDegE = maxDegree(expG)
            cavrgDegO = avgDegree(G)
            cavrgDegE = avgDegree(expG)
            cminDegO = minDegree(G)
            cminDegE = minDegree(expG)
            cdiameterO = diam(G)
            cdiameterE = diam(expG)
            cisRegularO =isRegular(G)
            cisRegularE = isRegular(expG)
            cnumTriangleO = numOfTriangles(G)
            cnumTriangleE = numOfTriangles(expG)
            cisConnectedO = int(nx.is_connected(G))
            cisConnectedE = int(nx.is_connected(expG))
            cisPlanarO = int(nx.check_planarity(G)[0])
            cisPlanarE = int(nx.check_planarity(expG)[0])
            
       # %d,%d,%d, %d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d


            sql_command = """INSERT INTO grahhhhhh (c,
                n_verticesO,  
                n_edgesO,
                n_edgesE,
                maxDegO,
                maxDegE,
                avrgDegO,
                avrgDegE,
                minDegO,
                minDegE,
                diameterO,
                diameterE,
                isRegularO,
                isRegularE,
                numTriangleO,
                numTriangleE,
                isConnectedO,
                isConnectedE,
                isPlanarO,
                isPlanarE) 
            VALUES (?,?,?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""
        
            recordTuple = (cc,
            cn_verticesO, 
            cn_edgesO, 
            cn_edgesE,
            cmaxDegO,
            cmaxDegE,
            cavrgDegO,
            cavrgDegE,
            cminDegO,
            cminDegE,
            cdiameterO,
            cdiameterE,
            cisRegularO,
            cisRegularE,
            cnumTriangleO,
            cnumTriangleE,
            cisConnectedO,
            cisConnectedE,
            cisPlanarO,
            cisPlanarE)

            crsr.execute(sql_command, recordTuple)
            connection.commit() 
    connection.close() 
