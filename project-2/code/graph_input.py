import networkx as nx
import sys

#with open(sys.argv[1], 'r') as file:


with open('file.txt') as file:
    nodes = file.readline()
    courses = file.readlines()

G = nx.DiGraph()

for i in range(len(courses)):
    course = courses[i].strip().split()
    course_num = i+1
    for j in range(1, int(course[0]) + 1):
        G.add_edge(course[j], course_num)

print(G.edges)

