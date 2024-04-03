import random

"""
Generate random input files
"""
for n in range(200, 2001, 200):
    x = n//200
    file_name = "sample--" + str(x) + ".txt"
    with open(file_name, "w") as file:
        file.write(str(n))
        file.write("\n")
        for _ in range(n):
            rand_num = random.randrange(1,1000)
            file.write(str(rand_num))
            file.write(" ")