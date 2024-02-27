import networkx as nx
from functools import reduce
from colorama import Fore
import sys
import random
import graph_input
 
def convert(lst):
    # using reduce function to cumulatively apply lambda function to each element
    # in the list and concatenate them with space
    lst_string = map(str, lst)
    return reduce(lambda x,y: x + ' ' + y, lst_string)

def write_graph_to_file(G):
    print("Writing graph to file " + filename + " with " + str(G.number_of_edges()) + " edges and " + str(G.number_of_nodes()) + " nodes")
    sys.stdout.flush()
    # Translate networkx graph into input file format

    if G.number_of_nodes() > maxNumNodes:
        print(Fore.RED + "WARNING, SADNESS: GENERATED INPUT EXCEEDED THE MAXIMUM NUMBER OF NODES WITH [" + G.number_of_nodes() + "] NODES")
        sys.stdout.flush()
        
    if G.number_of_edges() > maxNumEdges:
        print(Fore.RED + "WARNING, SADNESS: GENERATED INPUT EXCEEDED THE MAXIMUM NUMBER OF EDGES WITH [" + G.number_of_nodes() + "] EDGES")
        sys.stdout.flush()

    listsPrereqs = [[] for _ in range(G.number_of_nodes())]

    for edge in G.edges:
        # add 1 as networkx likes to label things starting from 0
        end_node = edge[1] + 1
        start_node = edge[0] + 1
        listsPrereqs[end_node-1].append(start_node)

    with open(filename, "w") as file:
        file.write(str(G.number_of_nodes()))
        file.write("\n")

        total_length = len(listsPrereqs)
        for i in range(total_length):
            inside_length = len(listsPrereqs[i])
            file.write(str(inside_length))
            if inside_length > 0:
                file.write(" ")
                file.write(convert(listsPrereqs[i]))
            if i < total_length-1:
                file.write("\n")

def combine_graphs(G, H, weaklyConnect):
    if G.number_of_nodes() == 0:
        return H
    
    if H.number_of_nodes() == 0:
        return G
    
    if not weaklyConnect:
        return nx.disjoint_union(G, H)

    I = nx.disjoint_union(G, H)
    I.add_edge(0, G.number_of_nodes())
    return I

def generate_graph():
    # random networkx stuffs
    G = combine_graphs(nx.to_directed(nx.ladder_graph(20)), nx.hexagonal_lattice_graph(5, 6, True, create_using=nx.DiGraph), False)
    G = combine_graphs(G, nx.to_directed(nx.turan_graph(100, 5)), False)
    G = combine_graphs(G, nx.to_directed(nx.full_rary_tree(3, 100)), True)
    G = combine_graphs(G, nx.to_directed(nx.wheel_graph(43)), True)
    G = combine_graphs(G, nx.to_directed(nx.hypercube_graph(7)), False)
    G = combine_graphs(G, nx.fast_gnp_random_graph(100, 0.5, directed=True), False)
    G = combine_graphs(G, nx.to_directed(nx.dense_gnm_random_graph(40, 200)), True)
    G = combine_graphs(G, nx.to_directed(nx.newman_watts_strogatz_graph(100, 3, 0.5)), True)
    G = combine_graphs(G, nx.to_directed(nx.random_regular_graph(4, 100)), True)
    G = combine_graphs(G, nx.to_directed(nx.barabasi_albert_graph(100, 3)), False)
    G = combine_graphs(G, nx.to_directed(nx.powerlaw_cluster_graph(100, 2, 0.5)), False)
    G = combine_graphs(G, nx.to_directed(nx.duplication_divergence_graph(100, 0.5)), False)
    G = combine_graphs(G, nx.DiGraph(nx.random_k_out_graph(100, 4, 0.5, False)), True)

    # random stuff not networkx
    G = combine_graphs(G, nx.to_directed(nx.dense_gnm_random_graph(40, 200)), False)
    line_with_random_back_edges(20, 0.5)

    # determined stuff
    G = combine_graphs(G, split_merge(8), True)
    G = combine_graphs(G, nx.reverse(split_merge(8)), True) #reverse edge direction of previous graph
    G = combine_graphs(G, split_merge_split_merge(8), True)
    G = combine_graphs(G, directed_wheel(20), True)
    G = combine_graphs(G, tutte_inspired(), True)

    # fill the rest with random crap
    G = combine_graphs(G, nx.to_directed(nx.bipartite.random_graph(maxNumGeneratedNodes - G.number_of_nodes(), maxNumGeneratedEdges - G.number_of_edges(), 0.5)), False)

    return G

def line_with_random_back_edges(n, p):
    G = nx.DiGraph()
    G.add_node(0)
    for i in range(1, n):
        G.add_node(i)
        G.add_edge(i - 1, i)

        for j in range(0, i):
            if random.random() > p:
                G.add_edge(i, j)
    
    return G

def split_merge(num_splits):
    #num_splits must be in the 2^n sequence to work (2,4,8,16,32...etc.)
    G = nx.DiGraph()
    start_node = 1 #start node in split sequence
    for i in range(start_node, num_splits + start_node):
        G.add_edge(0,i)
    
    merge_node = num_splits
    while num_splits != 1:
        for i in range (start_node, num_splits + start_node):
            if i % 2 != 0:
                merge_node += 1
            G.add_edge(i, merge_node)
        start_node = num_splits + start_node
        num_splits = int(num_splits / 2)
    
    # add cycle
    curr_node = start_node
    G.add_edge(curr_node, curr_node + 1)
    G.add_edge(curr_node + 1, 0)
    G.add_edge(curr_node + 1, curr_node + 2)
    G.add_edge(curr_node + 2, curr_node + 1)

    return G

def split_merge_split_merge(num_splits):
    G = nx.DiGraph()
    center_node = 0
    for i in range(1, num_splits + 1):
        G.add_edge(center_node, i)
        G.add_edge(i, num_splits + 1)
    center_node = num_splits + 1
    for i in range(center_node + 1, center_node + num_splits + 1):
        G.add_edge(center_node, i)
        G.add_edge(i, center_node + num_splits + 1)
    center_node += (num_splits + 1)
    #add cycle
    G.add_edge(center_node, center_node + 1)
    G.add_edge(center_node + 1, 0)
    G.add_edge(center_node + 1, center_node + 2)
    G.add_edge(center_node + 2, center_node + 1)

    return G
    
def directed_wheel(circumference): #circumference is the number of nodes surrounding center node
    G = nx.DiGraph()
    #create circle
    for i in range(1, circumference): 
        G.add_edge(i-1, i)
    G.add_edge(0, circumference - 1) #closes circle
    
    center_node = circumference #next number name for node
    for i in range(0, circumference - 1):
        G.add_edge(center_node, i)
    G.add_edge(circumference - 1, center_node) #single reverse edge
    return G

def tutte_inspired():
    G = graph_input.load_graph("inputs/inputBill.txt", False)
    return G


if __name__ == "__main__":
    # User inputs
    num_nodes = 10 # bound is 10^4 nodes, 10^5 edges
    maxNumNodes = 10000
    maxNumEdges = 100000
    maxNumGeneratedNodes = 5000
    maxNumGeneratedEdges = 50000
    debug = False
    filename = "inputs/finalinput.txt"

    # Use networkx to design your input graph (CAN BE MODIFIED)
    G = generate_graph()

    # Print out edges for debug
    if debug:
        for edge in G.edges:
            start_node = str(edge[0]).replace(', ', "").replace(")", "").replace("(", "")
            end_node = str(edge[1]).replace(', ', "").replace(")", "").replace("(", "")
            print(str(start_node) + " -> " + str(end_node))
    
    # # Convert from NetworkX graph to Graphviz graph (linux only, apparently)
    # A = nx.nx_agraph.to_agraph(G)
    # # Set graph layout style and draw
    # A.layout('dot')
    # A.draw('networkx_graph2.png')
            
    write_graph_to_file(G)