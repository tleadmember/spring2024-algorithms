from os import listdir
import os
from timeit import default_timer as timer

if __name__ == "__main__":
    files = listdir("outputs")
    for file in files:
        num = file[19:22]
        os.rename("outputs/" + file, "outputs/input_group" + num + ".txt_output")