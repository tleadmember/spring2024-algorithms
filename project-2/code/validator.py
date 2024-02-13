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
        print(valid)

    return valid

def validate_output_from_input(input, output, debug):
    return validate_output(graph_input.load_graph(input, debug), output, debug)