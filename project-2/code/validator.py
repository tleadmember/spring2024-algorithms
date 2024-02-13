import networkx as nx

#with open(sys.argv[1], 'r') as file:
with open('file.txt') as file:
    nodes = file.readline()
    courses = file.readlines()

G = nx.DiGraph()

for i in range(len(courses)):
    course = courses[i].strip().split()
    course_num = i+1
    for j in range(1, int(course[0]) + 1):
        G.add_edge(int(course[j]), course_num)

for edge in G.edges:
    start_node = str(edge[0]).replace(', ', "").replace(")", "").replace("(", "")
    end_node = str(edge[1]).replace(', ', "").replace(")", "").replace("(", "")
    print(str(start_node) + " -> " + str(end_node))

print(nx.is_directed_acyclic_graph(G))

