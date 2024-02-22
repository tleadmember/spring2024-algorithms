import networkx as nx

def algorithm(G):
    sccs = nx.strongly_connected_components(G)
    listNodes = []
    
    for scc in sccs:
        # create copy so the subgraph can be modified. The original graph actually does not need to be modified. however this might be slow idk
        sg = G.subgraph(scc)
        c = sg.copy()
        while not nx.is_directed_acyclic_graph(c):
            cycles = nx.simple_cycles(c)
            cyclesLst = [*cycles]
            print("Cycles list: " + str(cyclesLst))
            # Extract common elements from list of lists, using list comprehension and set intersection
            commonElmLst = list(set(cyclesLst[0]).intersection(*cyclesLst[1:]))           
            # printing result
            print("The common elements from N lists : " + str(commonElmLst))
            if len(commonElmLst) == 0:          # if no common element in cycles, just delete the first random node
                print("Deleting highest-degree node...")
                badNode = cyclesLst[0][0]
                c.remove_node(badNode)
                listNodes.append(badNode)
            else:
                print("Got some common node(s) among cycles!")
                for badNode in commonElmLst:    # if there is a common node in cycles, delete that node
                    c.remove_node(badNode)
                    listNodes.append(badNode)

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