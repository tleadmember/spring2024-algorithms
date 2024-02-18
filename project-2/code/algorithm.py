import networkx as nx
from heapdict import heapdict

def algorithm(G):
    sccs = (G.subgraph(c) for c in nx.strongly_connected_components(G))
    listNodes = []
    
    for subgraph in sccs:
        # create copy so the subgraph can be modified. The original graph actually does not need to be modified. however this might be slow idk
        c = nx.DiGraph(G.subgraph(subgraph))
        q = heapdict()
        for n in c:
            # negative because heapdict takes the lowest priority, not the highest priority
            q[n] = - c.in_degree(n) - c.out_degree(n)

        while not nx.is_directed_acyclic_graph(c):
            (maxDegreeNode, d) = q.popitem()
            neighbors = nx.all_neighbors(c, maxDegreeNode)
            c.remove_node(maxDegreeNode)
            listNodes.append(maxDegreeNode)
            for a in neighbors:
                q[a] = - c.in_degree(a) - c.out_degree(a)

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