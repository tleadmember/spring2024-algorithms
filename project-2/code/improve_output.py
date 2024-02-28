import algorithm
import graph_input
import validator
import sys
from colorama import Fore
from timeit import default_timer as timer
import networkx as nx

if __name__ == "__main__":
    debug = False
    timeSpentImproving = 120 # spend 2 minutes attempting to improve the output
    # useful to check if we are already at the optimal output, but not so good for actually improving an output
    forceImprove = True # Whether or not to force an improvement by 1

    filename = ""
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print("Please enter a filename when running this file.")
        exit()

    print("Loading graph for [" + filename + "]")
    sys.stdout.flush()
    G = graph_input.load_graph("inputs/" + filename, debug)
    print("Loading output for [" + filename + "]")
    sys.stdout.flush()

    removedCourses = []
    with open("outputs/" + filename + "_output") as file:
        dumb = file.readline()
        removedCourses = file.readline().strip().split()

    sccs = list((G.subgraph(c) for c in nx.strongly_connected_components(G)))
    listNodes = []
    sccsProcessed = 0
    sccsToProcess = []
    startTime = timer()
    for subgraph in sccs:
        if subgraph.number_of_nodes() < 2:
            # sccs of length 1 do not need to be processed
            continue

        # complete and almost complete subgraphs don't count towards the time
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
            
        sccsToProcess.append(subgraph)

    if len(sccsToProcess) > 0:
        sccMaxTime = timeSpentImproving / len(sccsToProcess)

    for subgraph in sccsToProcess:
        print("scc " + str(sccsProcessed + 1) + ", nodes: " + str(subgraph.number_of_nodes()) + ", edges: " + str(subgraph.number_of_edges()) + ", initial maxTime: " + str(sccMaxTime))
        sys.stdout.flush()
        sccStartTime = timer()

        # find the removed nodes actually in this subgraph
        removedNodesInScc = []
        for n in removedCourses:
            if subgraph.has_node(n):
                removedNodesInScc.append(n)

        c = nx.DiGraph(G.subgraph(subgraph))
        tmp = []
        if forceImprove:
            print("Force improving the output")
            sys.stdout.flush()
            algorithm.forceImprove(c, tmp, removedNodesInScc)
        else:
            print("Randomly improving the output")
            algorithm.algorithmRandomWithStartingPoint(c, tmp, removedNodesInScc, sccStartTime, timeSpentImproving)
        
        print("Finished improve.")
        listNodes.extend(tmp)
        msg = "Time elapsed: {} seconds."
        formatted_msg = msg.format(timer() - sccStartTime)
        print(formatted_msg)
        sys.stdout.flush()

    if len(removedCourses) > len(listNodes):
        print("HOOORAYYYY!!! We've improved the output by " + str(len(removedCourses) - len(listNodes)) + " nodes!!!")

    algorithm.write_output(listNodes, "outputs/" + filename + "_outputimproved")
    print("Validating the output...")
    sys.stdout.flush()
    if not validator.validate_output(G, "outputs/" + filename + "_output", debug):
        print(Fore.RED + "WARNING, SADNESS: OUTPUT WAS NOT VALID FOR [" + filename + "]")
        sys.stdout.flush()

    msg = "Total time elapsed: {} seconds."
    formatted_msg = msg.format(timer() - startTime)
    print(formatted_msg)
    sys.stdout.flush()