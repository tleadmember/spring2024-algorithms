import networkx as nx
from collections import defaultdict
import random
import math

def is_complete(G):
    nodeList = list(G)
    H = G.subgraph(nodeList)
    n = len(nodeList)
    return H.size() == n*(n-1)

def delete_nodes(H):
    listNodes2 = []
    sccs = (H.subgraph(c) for c in nx.strongly_connected_components(H))
    for scc in sccs:
        if len(scc.nodes()) >= 2: # if SCC has only 1 node, go to next iteration of "for scc in sccs"
            sg = H.subgraph(scc)    # create subgraph copy to modify
            c = sg.copy()
            while not nx.is_directed_acyclic_graph(c):
                cycle = nx.find_cycle(c)
                cycle = [*cycle]
                # Take 1 random node out to remove
                min = 0
                max = len(cycle)-1
                randIndex = random.randint(min,max)
                edge = cycle[randIndex]
                randIndex = random.randint(0,1)
                node = edge[randIndex]
                # Remove nodes one by one and check if SCC is DAG yet
                c.remove_node(node)
                listNodes2.append(node)
            # break   # only run "for scc in sccs" once after finding a SCC with at least 2 nodes, and recheck scc's in overall graph
    for node in listNodes2:
        H.remove_node(node)
    return listNodes2

def algorithm(G):
    listNodes = []
    
    # check if a complete graph
    if is_complete(G):
        listNodes = list(G)[1:] # delete everything but one node
    else:
        H = G.subgraph(list(G))
        H = H.copy() # create subgraph copy of G to modify
        # while not nx.is_directed_acyclic_graph(H):
        listNodes += delete_nodes(H)

    return listNodes


def create_output(G, filename):
    removedNodes = algorithm(G)

    with open(filename, "w") as file:
        file.write(str(len(removedNodes)))
        file.write("\n")

        for i in range(len(removedNodes)):
            file.write(str(removedNodes[i]))

            # don't write the space if it is the last node
            if i != len(removedNodes) - 1:
                file.write(" ")