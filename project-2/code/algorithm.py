import networkx as nx
from collections import defaultdict

def is_complete(G):
    nodeList = list(G)
    H = G.subgraph(nodeList)
    n = len(nodeList)
    return H.size() == n*(n-1)

def delete_nodes(H):
    listNodes2 = []
    sccs = nx.strongly_connected_components(H)
    for scc in sccs:
        if len([_ for _ in scc]) >= 2: # if SCC has only 1 node, go to next iteration of "for scc in sccs"
            sg = H.subgraph(scc)    # create subgraph copy to modify
            c = sg.copy()
            # while not nx.is_directed_acyclic_graph(c): ### instead of making each SCC DAG, just delete one common cycle node and recheck SCC's on whole graph
            cycles = nx.simple_cycles(c, length_bound=c.number_of_nodes())
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

            # Remove common nodes one by one and check if SCC is DAG yet
            # for commonNode in commonNodes:
            #     c.remove_node(commonNode)
            #     # H.remove_node(commonNode)  
            #     listNodes2.append(commonNode)
            #     if nx.is_directed_acyclic_graph(c):
            #         break

            # Remove the first of common nodes in cycles and go back to checking if SCC is DAG, and find cycles again
            c.remove_node(commonNodes[0])
            listNodes2.append(commonNodes[0])

            break   # only run "for scc in sccs" once after finding a SCC with at least 2 nodes, and recheck scc's in overall graph
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
        while not nx.is_directed_acyclic_graph(H):
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