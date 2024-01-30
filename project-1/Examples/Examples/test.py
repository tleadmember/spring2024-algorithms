""" Reading inputs """
import sys

with open(sys.argv[1], 'r') as my_file:
    input = my_file.readline().strip()
    n,m = map(int, input.split())
    goal_room = n

    input = my_file.readline().strip()
    colors = list(input.split())

    input = my_file.readline().strip()
    captain_start,lucky_start = map(int, input.split())

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
# print(captain_start)
# print(lucky_start)
# print(type(corr_start))
# print(type(corr_end))
# print(type(corr_color))
# print(type(colors[0]))
# print(corr_starts)
# print(corr_ends)
# print(corr_colors)







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