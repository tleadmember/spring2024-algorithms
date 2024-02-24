import networkx as nx
from collections import defaultdict

def algorithm(G):
    thresholdNodes = 100 # tbd
    thresholdEdges = 1000
    
    sccs = (G.subgraph(c) for c in nx.strongly_connected_components(G))
    listNodes = []
    
    for subgraph in sccs:
        if len(subgraph.nodes()) < 2:
            continue

        if subgraph.number_of_edges() == subgraph.number_of_nodes() * (subgraph.number_of_nodes() - 1):
            listNodes += list(subgraph)[1:] # delete everything but one node
            continue

        # if the graph is a complete graph missing exactly one edge
        if subgraph.number_of_edges() == subgraph.number_of_nodes() * (subgraph.number_of_nodes() - 1) - 1:
            # remove only the nodes that are connected to every other node
            for n in subgraph:
                if subgraph.out_degree(n) + subgraph.in_degree(n) == 2 * (subgraph.number_of_nodes() - 1):
                    listNodes.append(n)
            
            continue
        
        c = nx.DiGraph(G.subgraph(subgraph))

        if thresholdNodes < c.number_of_nodes() or thresholdEdges < c.number_of_edges():
            # if above the threshold, do the faster but less optimal algorithm.
            untangleScc(c, listNodes)
        else:
            # otherwise, do the slower but more optimal algorithm.
            algorithm2(G, listNodes)
            break

    return listNodes

def untangleScc(c, listNodes):    
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
        if len(scc.nodes()) < 2:
            continue
        
        subgraph = nx.DiGraph(c.subgraph(scc))
        untangleScc(subgraph, listNodes)

def algorithm2(G, listNodes):
    # check if a complete graph
    if is_complete(G):
        listNodes = list(G)[1:] # delete everything but one node
    else:
        H = G.subgraph(list(G))
        H = H.copy() # create subgraph copy of G to modify
        while not nx.is_directed_acyclic_graph(H):
            listNodes += delete_nodes(H)

def is_complete(G):
    nodeList = list(G)
    H = G.subgraph(nodeList)
    n = len(nodeList)
    return H.size() == n*(n-1)

def delete_nodes(H):
    listNodes2 = []
    # sccs = nx.strongly_connected_components(H)
    sccs = (H.subgraph(c) for c in nx.strongly_connected_components(H))
    for scc in sccs:
        if len(scc.nodes()) >= 2: # if SCC has only 1 node, go to next iteration of "for scc in sccs"
            sg = H.subgraph(scc)    # create subgraph copy to modify
            c = sg.copy()
            # while not nx.is_directed_acyclic_graph(c): ### instead of making each SCC DAG, just delete one common cycle node and recheck SCC's on whole graph
            cycles = nx.simple_cycles(c, length_bound=c.number_of_nodes())
            cyclesLst = [*cycles]
            delete_common(c, listNodes2, cyclesLst)
            # break   # only run "for scc in sccs" once after finding a SCC with at least 2 nodes, and recheck scc's in overall graph
    for node in listNodes2:
        H.remove_node(node)
    return listNodes2

def delete_common(c, listNodes2, cyclesLst):
    # Find most common node(s) in cyclesLst (does not have to be in ALL cycles)
    counts = defaultdict(lambda: 0)                
    for cycle in cyclesLst:
        for node in cycle:
            counts[node] += 1
    maxCount = max(counts.values())
    commonNodes = [node for node, count in counts.items() if count == maxCount]

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

    # Check if a cycle has had the node delete from it. If yes, then it probably is no longer a cycle and therefore not insignicant.
    # If the cycle hasn't been touched, then add it to a new list that needs more work on.
    cyclesLst2 = []
    for cycle in cyclesLst:
        isStubborn = True # initialize a flag
        for node in cycle:
            if node == commonNodes[0]:
                isStubborn = False
        if isStubborn == True:
            cyclesLst2.append(cycle)
    if len(cyclesLst2) > 0:
        delete_common(c, listNodes2, cyclesLst2) # recursive

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