import networkx as nx
from functools import reduce
from colorama import Fore
import sys
 
def convert(lst):
    # using reduce function to cumulatively apply lambda function to each element
    # in the list and concatenate them with space
    lst_string = map(str, lst)
    return reduce(lambda x,y: x + ' ' + y, lst_string)

def write_graph_to_file(G):
    # Translate networkx graph into input file format
    maxNumNodes = 10000
    maxNumEdges = 100000

    if G.number_of_nodes() > maxNumNodes:
        print(Fore.RED + "WARNING, SADNESS: GENERATED INPUT EXCEEDED THE MAXIMUM NUMBER OF NODES WITH [" + G.number_of_nodes() + "] NODES")
        sys.stdout.flush()
        
    if G.number_of_edges() > maxNumEdges:
        print(Fore.RED + "WARNING, SADNESS: GENERATED INPUT EXCEEDED THE MAXIMUM NUMBER OF EDGES WITH [" + G.number_of_nodes() + "] EDGES")
        sys.stdout.flush()

    listsPrereqs = [[] for _ in range(G.number_of_nodes())]

    for edge in G.edges:
        end_node = edge[1]
        start_node = edge[0]
        listsPrereqs[end_node-1].append(start_node)

    with open(filename, "w") as file:
        file.write(str(num_nodes))
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
    if G.number_of_nodes == 0:
        return H
    
    if H.number_of_nodes == 0:
        return G
    
    if not weaklyConnect:
        return nx.disjoint_union(G, H)

    n1 = G.nodes()[0]
    n2 = H.nodes()[1]
    I = nx.disjoint_union(G, H)
    I.add_edge(n1, n2)
    return I

def generate_graph(num_nodes):
    # return nx.complete_graph(range(1,num_nodes+1), create_using=nx.DiGraph)

    G = nx.complete_graph(range(1,num_nodes+1), create_using=nx.DiGraph)
    H = nx.complete_graph(range(1,num_nodes+1), create_using=nx.DiGraph)
    return combine_graphs(G, H, False)

if __name__ == "__main__":
    # User inputs
    num_nodes = 316 # bound is 10^4 nodes, 10^5 edges
    debug = False
    filename = "inputs/finalinput.txt"

    # Use networkx to design your input graph (CAN BE MODIFIED)
    G = generate_graph(num_nodes)

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