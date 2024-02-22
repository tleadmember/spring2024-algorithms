import networkx as nx

def algorithm(G):
    sccs = (G.subgraph(c) for c in nx.strongly_connected_components(G))
    listNodes = []
    
    for subgraph in sccs:
        c = nx.DiGraph(G.subgraph(subgraph))
        untangleScc(c, listNodes)

    return listNodes

def untangleScc(c, listNodes):
    if len(c.nodes()) < 2:
        return   
    
    maxDegreeNode = None
    maxDegree = 0
    for n in c:
        if maxDegreeNode is None:
            maxDegreeNode = n
            maxDegree = c.in_degree(n) + c.out_degree(n)
            continue
        if c.in_degree(n) + c.out_degree(n) > maxDegree:
            maxDegreeNode = n
            maxDegree = c.in_degree(n) + c.out_degree(n)
        
    c.remove_node(maxDegreeNode)
    listNodes.append(maxDegreeNode)

    sccs = (c.subgraph(g) for g in nx.strongly_connected_components(c))
    for scc in sccs:
        subgraph = nx.DiGraph(c.subgraph(scc))
        untangleScc(subgraph, listNodes)

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