import networkx as nx
from collections import defaultdict

def algorithm(G):
    sccs = nx.strongly_connected_components(G)
    listNodes = []
    
    for scc in sccs:
        # create copy so the subgraph can be modified. The original graph actually does not need to be modified. however this might be slow idk
        sg = G.subgraph(scc)
        c = sg.copy()
        while not nx.is_directed_acyclic_graph(c):
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
            # Remove all common nodes
            for commonNode in commonNodes:
                c.remove_node(commonNode)
                listNodes.append(commonNode)


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