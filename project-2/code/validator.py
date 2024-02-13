import networkx as nx
import graph_input

def validate_output(G, output, debug):
    with open(output) as file:
        dumb = file.readline()
        removedCourses = file.readline().strip().split()
    
    for removedCourse in removedCourses:
        G.remove_node(int(removedCourse))

    valid = nx.is_directed_acyclic_graph(G)

    if debug:
        for edge in G.edges:
            start_node = str(edge[0]).replace(', ', "").replace(")", "").replace("(", "")
            end_node = str(edge[1]).replace(', ', "").replace(")", "").replace("(", "")
            print(str(start_node) + " -> " + str(end_node))
        print(valid)

    return valid

def validate_output_from_input(input, output, debug):
    return validate_output(graph_input.load_graph(input, debug), output, debug)