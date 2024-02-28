import algorithm
import graph_input
import validator
import sys
from colorama import Fore
from timeit import default_timer as timer
import networkx as nx
from os import listdir
import os

def improve_output(G, removedCourses, forceImprove, forceImproveCount):
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

        c = nx.DiGraph(G.subgraph(subgraph))

        # find the removed nodes actually in this subgraph
        removedNodesInScc = []
        for n in removedCourses:
            if c.has_node(int(n)):
                removedNodesInScc.append(int(n))

        tmp = []
        if forceImprove:
            print("Force improving the output")
            sys.stdout.flush()
            algorithm.forceImprove(c, tmp, removedNodesInScc)
            for i in range(1, forceImproveCount):
                algorithm.forceImprove(c, tmp, tmp)
        else:
            print("Randomly improving the output")
            algorithm.algorithmRandomWithStartingPoint(c, tmp, removedNodesInScc, sccStartTime, sccMaxTime)
        
        print("Finished improve.")
        listNodes.extend(tmp)
        msg = "Time elapsed: {} seconds."
        formatted_msg = msg.format(timer() - sccStartTime)
        print(formatted_msg)
        sys.stdout.flush()

        sccsProcessed += 1
        # get allowed time remaining
        timeSpentImproving = timeSpentImproving - (timer() - sccStartTime)
        if sccsProcessed - len(sccsToProcess) != 0:
            sccMaxTime = (timeSpentImproving) / (len(sccsToProcess) - sccsProcessed)

    msg = "Total time elapsed: {} seconds."
    formatted_msg = msg.format(timer() - startTime)
    print(formatted_msg)
    sys.stdout.flush()
    return listNodes

def improveFile(filename):
    print("Loading graph for [" + filename + "]")
    sys.stdout.flush()
    G = graph_input.load_graph("inputs/" + filename, debug)
    sccs = list((G.subgraph(c) for c in nx.strongly_connected_components(G)))
        
    print("Loading output for [" + filename + "]")
    sys.stdout.flush()

    removedCourses = []
    with open("outputs/" + filename + "_output") as file:
        dumb = file.readline()
        removedCourses = file.readline().strip().split()

    print("Validating the input...")
    sys.stdout.flush()
    if not validator.validate_output(G, "outputs/" + filename + "_output", debug):
        print(Fore.RED + "WARNING, SADNESS: INPUT OUTPUT WAS NOT VALID FOR [" + filename + "]")
        sys.stdout.flush()

    listNodes = improve_output(G, removedCourses, forceImprove, forceImproveCount)

    if len(removedCourses) > len(listNodes):
        print("HOOORAYYYY!!! We've improved the output by " + str(len(removedCourses) - len(listNodes)) + " nodes!!!")

    if len(removedCourses) == len(listNodes) and forceImprove:
        print("Force improve was unable to improve the output. Output is optimal.")

    algorithm.write_output(listNodes, "outputs/" + filename + "_output")
    print("Validating the output...")
    sys.stdout.flush()
    if not validator.validate_output(G, "outputs/" + filename + "_output", debug):
        print(Fore.RED + "WARNING, SADNESS: OUTPUT WAS NOT VALID FOR [" + filename + "]")
        sys.stdout.flush()

if __name__ == "__main__":
    debug = False
    timeSpentImproving = 120 # spend 2 minutes attempting to improve the output
    # useful to check if we are already at the optimal output, but not so good for actually improving an output
    forceImprove = False # Whether or not to force an improvement by 1
    forceImproveCount = 1 # how many times to do a force improve

    filenames = []
    if len(sys.argv) > 1:
        filenames.append(sys.argv[1])
    else:
        filenames = listdir("inputs")

    for filename in filenames:
        improveFile(filename)