results = [0] * 3
print("Add meg egyesével a jegyeket!")
results[0] = input()
results[1] = input()
results[2] = input()

sum = 0
i = 0
while i < len(results):
  sum += int(results[i])
  i += 1
atlag = sum / len(results)
print(atlag)