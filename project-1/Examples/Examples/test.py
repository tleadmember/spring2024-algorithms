import sys
import networkx as nx
# import matplotlib.pyplot as plt

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
Create all edges 
"""
for k in range(m):
    for j in range(n-1): # n-1 because last room (goal room) has no color
        if colors[j] == corr_colors[k]:
            # add 2 edges on model graph
            G.add_edge((corr_starts[k],j+1) , (corr_ends[k],j+1))
            G.add_edge((j+1,corr_starts[k]) , (j+1,corr_ends[k]))

# print(list(G.edges))
# print("Total # nodes:", G.number_of_nodes())
# print("Total # edges:", G.number_of_edges())


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


"""
Run algorithms
"""






# input = lambda: sys.stdin.readline().strip()

# a,b,c = map(int,input().split())
# a = list(map(int, input().split()))
# output = []
# print(output, sep='\n')

# for _ in range(int(input())):
#     sols = []
#     n = int(input())
#     u = list(map(int, input().split()))
#     s = list(map(int, input().split()))
    
#     obj = [[] for _ in range(n)]
#     for i in range(n):
#         school = u[i]
#         obj[school-1].append(s[i])
    
#     for i in range(n):
#         obj[i].sort(reverse=True)
#         #obj[i] = [0] + obj[i]
#         for j in range(1,len(obj[i])):
#             obj[i][j] += obj[i][j-1]

#     obj.sort(key=len, reverse=True)
    
#     for k in range(1,n+1):
#         ans = 0
#         for i in range(n): # loop over each school
#             maxdiv = len(obj[i]) // k
#             if maxdiv == 0:
#                 break
#             maxi = maxdiv*k - 1
#             ans += obj[i][maxi]
#         sols.append(str(ans))
        
#     print(' '.join(sols))