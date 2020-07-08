
import random
import networkx as nx
from networkx.algorithms.isomorphism.isomorph import graph_could_be_isomorphic as isomorphic
from networkx.generators.atlas import graph_atlas_g
from itertools import product

class ExpNode:
    def __init__(self, label, value):
        self.label =label
        self.value =value
        
    def __str__(self):
        return str(self.label)



def createExpGraph( g,num): 
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



try:
    import pygraphviz
    from networkx.drawing.nx_agraph import graphviz_layout
except ImportError:
    try:
        import pydot
        from networkx.drawing.nx_pydot import graphviz_layout
    except ImportError:
        raise ImportError("This example needs Graphviz and either "
                          "PyGraphviz or pydot.")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

pp = PdfPages('multipage.pdf')
for i in range(10):
    G = graph_atlas_g()[int((i+2)/2)+60] #iterate over all graph of less than 7 vertices
    Exp = createExpGraph(G,3)
    
    if i%2 ==0:
        plt.figure(i+1, figsize=(10,15))
        # plt.subplot(211)
        pos = graphviz_layout(G, prog="neato")
        nx.draw(G,
                pos,
                node_size=260,
                vmin=0.0,
                vmax=1.0,
                node_color= "pink",
                with_labels=False
               )
        plt.savefig(pp, format='pdf')

    else:
        plt.figure(i+1, figsize=(10,15))
        # plt.subplot(212)
        pos = graphviz_layout(Exp, prog="neato")
        nx.draw(Exp,
                pos,
                node_size=260,
                vmin=0.0,
                vmax=1.0,
                node_color= "pink",
                with_labels=True
               )
        plt.savefig(pp, format='pdf')
    
pp.close()
