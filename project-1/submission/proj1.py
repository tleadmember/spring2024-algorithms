import sys
input = lambda: sys.stdin.readline().strip()





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