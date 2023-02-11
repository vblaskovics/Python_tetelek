import random

mylist = [23, 41, 11, 62, 53, 13, 22, 16]

randIndex = random.randint(0, len(mylist)-1)
mylist[randIndex] = mylist[randIndex] * 2

max = float('-inf')
i = 0
while i < len(mylist):
    if mylist[i] > max:
        max = mylist[i]
    i += 1

print(max)
