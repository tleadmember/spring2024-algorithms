import networkx as nx
from functools import reduce
 
def convert(lst):
    # using reduce function to cumulatively apply lambda function to each element
    # in the list and concatenate them with space
    lst_string = map(str, lst)
    return reduce(lambda x,y: x + ' ' + y, lst_string)


if __name__ == "__main__":
    # User inputs
    num_nodes = 316 # bound is 10^4 nodes, 10^5 edges
    debug = False
    filename = "inputs/complete316.txt"

    # Use networkx to design your input graph (CAN BE MODIFIED)
    G = nx.complete_graph(range(1,num_nodes+1), create_using=nx.DiGraph)

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


    # Translate networkx graph into input file format
    listsPrereqs = [[] for _ in range(num_nodes)]

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