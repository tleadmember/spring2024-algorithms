import networkx as nx
import graph_input
import sys
from os import listdir
from colorama import Fore

def validate_output(G, output, debug):
    H = G.copy()
    with open(output) as file:
        dumb = file.readline()
        removedCourses = file.readline().strip().split()
    
    for removedCourse in removedCourses:
        H.remove_node(int(removedCourse))

    valid = nx.is_directed_acyclic_graph(H)

    if debug:
        for edge in H.edges:
            start_node = str(edge[0]).replace(', ', "").replace(")", "").replace("(", "")
            end_node = str(edge[1]).replace(', ', "").replace(")", "").replace("(", "")
            print(str(start_node) + " -> " + str(end_node))
        print(valid)

    return valid

def validate_output_from_input(input, output, debug):
    return validate_output(graph_input.load_graph(input, debug), output, debug)

if __name__ == "__main__":
    debug = False
    filenames = []
    if len(sys.argv) > 1:
        filenames.append(sys.argv[1])
    else:
        filenames = listdir("inputs")

    for filename in filenames:
        print("Validating output for [" + filename + "]")
        sys.stdout.flush()
        if validate_output_from_input(filename, "outputs/" + filename + "_output", debug):
            print("Output was valid for [" + filename + "]")
        else:
            print(Fore.RED + "WARNING, SADNESS: OUTPUT WAS NOT VALID FOR [" + filename + "]")
            sys.stdout.flush()
