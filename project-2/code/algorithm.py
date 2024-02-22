import networkx as nx
from collections import defaultdict

def is_complete(G):
    nodeList = list(G)
    H = G.subgraph(nodeList)
    n = len(nodeList)
    return H.size() == n*(n-1)


def algorithm(G):
    listNodes = []
    
    # check if a complete graph
    if is_complete(G):
        print("Complete graph detected!")
        listNodes = list(G)[1:] # delete everything but one node
    else:
        H = G.subgraph(list(G)) 
        H = H.copy()    # create subgraph copy of G to modify
        # create copy so the subgraph can be modified. The original graph actually does not need to be modified. however this might be slow idk
        while not nx.is_directed_acyclic_graph(H):
            cycles = nx.simple_cycles(H, length_bound=H.number_of_nodes())
            cyclesLst = [*cycles]
            # print("Cycles list: " + str(cyclesLst))
            # Find most common node(s) in cyclesLst (does not have to be in ALL cycles)
            counts = defaultdict(lambda: 0)
            for cycle in cyclesLst:
                for node in cycle:
                    counts[node] += 1
            maxCount = max(counts.values())
            commonNodes = [node for node, count in counts.items() if count == maxCount]
            # print("Common node(s):" + str(commonNodes))
            # Remove only the first of common nodes
            for commonNode in commonNodes:
                H.remove_node(commonNode)  
                listNodes.append(commonNode)
                if nx.is_directed_acyclic_graph(H):
                    break



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