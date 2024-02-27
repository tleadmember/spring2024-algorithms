import networkx as nx
from collections import defaultdict
import random
import math
from timeit import default_timer as timer
import signal
import subprocess
import sys

RANDOM_FLAG = False

def algorithm(G):
    maxTime = 120.0 # 4 minutes per input max, this would end up being about 120 seconds per each random algorithm
    thresholdNodes = 0 # tbd
    thresholdEdges = 0
    thresholdNodesUntangleScc = 10000
    thresholdEdgesUntangleScc = 30000
    
    sccs = list((G.subgraph(c) for c in nx.strongly_connected_components(G)))
    listNodes = []
    
    sccsProcessed = 0
    sccsToProcess = []
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
        sccMaxTime = maxTime / len(sccsToProcess)

    for subgraph in sccsToProcess:
        print("scc " + str(sccsProcessed + 1) + ", nodes: " + str(subgraph.number_of_nodes()) + ", edges: " + str(subgraph.number_of_edges()) + ", initial maxTime: " + str(sccMaxTime))
        sys.stdout.flush()
        sccStartTime = timer()

        # H = G.subgraph(list(G))
        # H = H.copy() # create subgraph copy of G to modify

        # Do all the algorithms, and compare them to find the best one. 
        listListNodes = []

        startTime = timer()
        count = 0
        # Do algorithm random for maxTime seconds or 1000 times (will we win the lottery???)
        # while timer() - startTime < sccMaxTime and count < 1000:
        #     sys.stdout.flush()
        #     c = nx.DiGraph(G.subgraph(subgraph))
        #     tmp = []
        #     algorithmRandom(c, tmp)
        #     listListNodes.append(tmp)
        #     count += count

        print("done with initial random")
        sys.stdout.flush()
        tmp = []
        c = nx.DiGraph(G.subgraph(subgraph))
        if thresholdNodesUntangleScc >= c.number_of_nodes() and thresholdEdgesUntangleScc >= c.number_of_edges():
            print("untangle scc is used")
            sys.stdout.flush()
            untangleScc(c, tmp)
            listListNodes.append(tmp)
            print("done with untangle scc")
            sys.stdout.flush()
        
        tmp = []
        c = nx.DiGraph(G.subgraph(subgraph))
        print("starting old algorithm")
        sys.stdout.flush()
        old_algorithm(c, tmp)
        print("done with old algorithm")
        sys.stdout.flush()

        listListNodes.append(tmp)

        # Let the slow algorithm run for maxTime before timing it out (arg this is too annoying, windows why do you suck)
        # tmp = []
        # c = nx.DiGraph(H.subgraph(subgraph))
        # timeout = False
        
        # try:
        #     r = subprocess.run(algorithmSlow(c, tmp), timeout=maxTime)
        # except subprocess.TimeoutExpired as e:
        #     print("algorithm slow timed out")
        #     sys.stdout.flush()
        #     timeout = True

        # if not timeout:
        #     listListNodes.append(tmp)

        # signal.signal(signal.SIGABRT, timeout_handler)
        # signal.alarm(maxTime)
        # try:
        #     tmp = []
        #     c = nx.DiGraph(H.subgraph(subgraph))
        #     algorithmSlow(c, tmp)
        #     listListNodes.append(tmp)
        # except Exception as ex:
        #     pass
        # finally:
        #     signal.alarm(0)


        c = nx.DiGraph(G.subgraph(subgraph))
        # if below the threshold then do the slow algorithm
        if thresholdNodes >= c.number_of_nodes() or thresholdEdges >= c.number_of_edges():
            tmp = []
            algorithmSlow(c, tmp)

        # find the one with the smallest number of elements removed
        minimumListNodes = min(listListNodes, key = len)
        tmp = []
        c = nx.DiGraph(G.subgraph(subgraph))
        startTime = timer()
        print("starting random with starting point")
        sys.stdout.flush()
        listNodes.extend(algorithmRandomWithStartingPoint(c, tmp, minimumListNodes, startTime, sccMaxTime))
        print("done with random with starting point")
        sys.stdout.flush()

        # get allowed time remaining
        maxTime = maxTime - (timer() - sccStartTime)
        # divide it among remaining sccs
        sccsProcessed += 1
        if sccsProcessed is not len(sccsToProcess):
            sccMaxTime = maxTime / (len(sccsToProcess) - sccsProcessed)

    return listNodes

def timeout_handler(num, stack):
    print("algorithmSlow timed out")
    sys.stdout.flush()
    raise Exception("FUBAR")

def old_algorithm(c, listNodes):
    while not nx.is_directed_acyclic_graph(c):
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

def algorithmRandom(c, listNodes):
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
        listNodes.append(node)
    return listNodes

def algorithmRandomWithStartingPoint(c, listNodes, startingPoint, startTime, maxTime, count = 0):
    if len(startingPoint) == 1:
        listNodes = startingPoint
        return listNodes
    
    # run 1000 times or until max time
    # print("count:", count)
    # print("elapsed time:", timer() - startTime)
    # print("max time:", maxTime)
    sys.stdout.flush()
    if count == 900 or (timer() - startTime) >= maxTime:
        listNodes = startingPoint
        return listNodes
    
    newStartingPoint = []
    randomNodes = random.sample(startingPoint, k = 2)
    n1 = randomNodes[0]
    n2 = randomNodes[1]
    d = c.copy()

    for n in startingPoint:
        if n != n1 and n != n2: 
            d.remove_node(n)
            newStartingPoint.append(n)

    nodes = list(d.nodes())
    for i in range(0, 500):
        e = d.copy()
        n = random.choice(nodes)
        e.remove_node(n)
        if nx.is_directed_acyclic_graph(e):
            newStartingPoint.append(n)
            break
    
    if len(newStartingPoint) == len(startingPoint) - 2:
        listNodes = algorithmRandomWithStartingPoint(c, listNodes, startingPoint, startTime, maxTime, count + 1)
    else:
        listNodes = algorithmRandomWithStartingPoint(c, listNodes, newStartingPoint, startTime, maxTime, count + 1)

    return listNodes

def algorithmSlow(c, listNodes):
    while not nx.is_directed_acyclic_graph(c):
        cycles = nx.simple_cycles(c, length_bound=c.number_of_nodes())
        cyclesLst = [*cycles]
        delete_common(c, listNodes, cyclesLst)
    return listNodes

def delete_common(c, listNodes, cyclesLst):
    # Find most common node(s) in cyclesLst (does not have to be in ALL cycles)
    counts = defaultdict(lambda: 0)                
    for cycle in cyclesLst:
        for node in cycle:
            counts[node] += 1
    maxCount = max(counts.values())
    commonNodes = [node for node, count in counts.items() if count == maxCount]
    # Remove the first of common nodes in cycles and go back to checking if SCC is DAG, and find cycles again
    c.remove_node(commonNodes[0])
    listNodes.append(commonNodes[0])
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
        delete_common(c, listNodes, cyclesLst2) # recurse

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