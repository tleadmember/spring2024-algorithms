import graph_input
import validator
import algorithm
import sys
from colorama import Fore
from os import listdir
import os
from timeit import default_timer as timer


if __name__ == "__main__":
    debug = False

    filenames = []
    if len(sys.argv) > 1:
        filenames.append(sys.argv[1])
    else:
        '''
        #for sephia because her cwd is weird
        os.chdir(os.path.dirname(os.path.abspath(__file__))) #changes current working directory to the one running the script
        '''
        filenames = listdir("inputs")

    for filename in filenames:
        start = timer()
        print("Loading graph for [" + filename + "]")
        G = graph_input.load_graph("inputs/" + filename, debug)
        print("Running the incredible (hopefully) algorithm...")
        algorithm.create_output(G, "outputs/" + filename + "_output")
        print("Validating the output...")
        if not validator.validate_output(G, "outputs/" + filename + "_output", debug):
            print(Fore.RED + "WARNING, SADNESS: OUTPUT WAS NOT VALID FOR [" + filename + "]")
            
        end = timer()
        msg = "Time elapsed: {} seconds."
        formatted_msg = msg.format(end-start)
        print(formatted_msg)