import sys
import networkx as nx
import matplotlib.pyplot as plt

""" 
Reading inputs 
"""
with open(sys.argv[1], 'r') as my_file:
    input = my_file.readline().strip()
    n,m = map(int, input.split())
    goal_room = n

    input = my_file.readline().strip()
    colors = list(input.split())

    input = my_file.readline().strip()
    cptn_start,lucky_start = map(int, input.split())
    source_node = (cptn_start,lucky_start)

    corr_starts = []
    corr_ends = []
    corr_colors = []
    for _ in range(m):
        input = my_file.readline().strip()
        corr_start,corr_end,corr_color = input.split()
        corr_start = int(corr_start)
        corr_end = int(corr_end)
        corr_starts.append(corr_start)
        corr_ends.append(corr_end)
        corr_colors.append(corr_color)
    
# print(n)
# print(m)
# print(colors)
# print(cptn_start)
# print(lucky_start)
# print(type(corr_start))
# print(type(corr_end))
# print(type(corr_color))
# print(type(colors[0]))
# print(corr_starts)
# print(corr_ends)
# print(corr_colors)


"""
Create all nodes (cptn_room,lucky_room)
"""
G = nx.DiGraph()
for i in range(n):
    for j in range(n):
        tuple = (i+1,j+1)
        G.add_node(tuple)


""" 
Create edges based on game corridors
"""
for k in range(m):
    for j in range(n-1): # n-1 because last room (goal room) has no color
        if colors[j] == corr_colors[k]:
            # add 2 edges on model graph
            G.add_edge((corr_starts[k],j+1) , (corr_ends[k],j+1))
            G.add_edge((j+1,corr_starts[k]) , (j+1,corr_ends[k]))


"""
Create edges from each potential winning state to a common goal node
"""
goal_node = (-1,-1) # (-1,-1) is used as the goal node
G.add_node(goal_node) 
for j in range(n-1):
    G.add_edge((goal_room,j+1) , goal_node)
    G.add_edge((j+1,goal_room) , goal_node)


# print(list(G.edges))
# print("Total # nodes:", G.number_of_nodes())
# print("Total # edges:", G.number_of_edges())


"""
Run traverse algorithm
"""
try:
    paths = nx.all_shortest_paths(G, source=source_node, target=goal_node, weight=None, method='dijkstra')
    """ Translate graph shortest paths to game paths"""
    translated_paths = ""

    for p in paths:
        translated_p = ""
        for i in range(len(p)-2):
            if p[i][0] == p[i+1][0]:    # Captain didn't move. Lucky moved
                translated_p += "L" + str(p[i+1][1])
            else:                       # Captain moved
                translated_p += "R" + str(p[i+1][0])
        translated_paths += " " + translated_p

    """ Find the lexicographically first path """
    split_paths = translated_paths.split()
    split_paths.sort()
    print(split_paths[0])

    # for i in split_paths:
    #     print(i)

    # f = open("4-lex_out.txt", "r")
    # print(f.read())
    # if f.read() == split_paths[0]:
    #     print("pass")
    # else:
    #     print("FAIL")

except nx.NetworkXNoPath:
    print("NO PATH")
    # f = open("1-no_path_out.txt", "r")
    # if f.read() == "NO PATH":
    #     print("pass")
    # else:
    #     print("FAIL")


"""
Plot
"""
# val_map = {(1,1):0.0}
# values = [val_map.get(node, 0.25) for node in G.nodes()]
# pos = nx.spring_layout(G)
# nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), 
#                        node_color = values, node_size = 500)
# nx.draw_networkx_labels(G, pos)
# nx.draw_networkx_edges(G, pos, edgelist=list(G.edges), edge_color='b', arrows=True)
# plt.show()

# nx.draw(G, with_labels=True, font_weight='bold')
# plt.show()

# pos = nx.nx_agraph.graphviz_layout(G, prog="neato")
# nx.draw_networkx_nodes(G, pos, node_color = 'yellow', node_size = 500)
# nx.draw_networkx_labels(G, pos)
# nx.draw_networkx_edges(G, pos, edgelist=list(G.edges), edge_color='black', arrows=True)
# plt.show()

# pos = nx.nx_agraph.graphviz_layout(G)
# nx.draw_networkx(G, pos)
# plt.show()
# plt.savefig('networkx_graph.png')


# Convert from NetworkX graph to Graphviz graph
A = nx.nx_agraph.to_agraph(G)
# Formatting start node in the given example
A.get_node((1,2)).attr['style'] = 'filled'
A.get_node((1,2)).attr['fillcolor'] = 'yellow'
A.get_node((1,2)).attr['shape'] = 'square'
# Formatting goal node in the given example
A.get_node((-1,-1)).attr['style'] = 'filled'
A.get_node((-1,-1)).attr['fillcolor'] = 'violet'
A.get_node((-1,-1)).attr['shape'] = 'star'
# Formatting the nodes along the shortest path
A.get_node((1,1)).attr['style'] = 'filled'
A.get_node((1,1)).attr['fillcolor'] = 'orange'
A.get_node((1,3)).attr['style'] = 'filled'
A.get_node((1,3)).attr['fillcolor'] = 'orange'
A.get_node((3,3)).attr['style'] = 'filled'
A.get_node((3,3)).attr['fillcolor'] = 'orange'
A.get_node((3,5)).attr['style'] = 'filled'
A.get_node((3,5)).attr['fillcolor'] = 'orange'
A.get_node((6,5)).attr['style'] = 'filled'
A.get_node((6,5)).attr['fillcolor'] = 'orange'
A.get_node((6,8)).attr['style'] = 'filled'
A.get_node((6,8)).attr['fillcolor'] = 'orange'
# Formatting the edges along the shortest path
A.get_edge(*((1,2) , (1,1))).attr['color'] = 'green'
A.get_edge(*((1,1) , (1,3))).attr['color'] = 'green'
A.get_edge(*((1,3) , (3,3))).attr['color'] = 'green'
A.get_edge(*((3,3) , (3,5))).attr['color'] = 'green'
A.get_edge(*((3,5) , (6,5))).attr['color'] = 'red'
A.get_edge(*((6,5) , (6,8))).attr['color'] = 'red'
A.get_edge(*((6,8) , (-1,-1))).attr['color'] = 'violet'
# Set graph layout style and draw
A.layout('dot')
A.draw('networkx_graph.png')