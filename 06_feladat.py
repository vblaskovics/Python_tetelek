results = [42, 38, 50, 40, 44, 56, 30, 30, 46, 34, 42, 49]

print("Add meg a dobás eredményét!")
result = int(input())

i = 0
while i < len(results) and results[i] != result:
    i += 1

if i < len(results):
    print("Már volt")
else:
    print("Még nem volt")

results.append(result)

max = float('-inf')
maxInd = 0
i = 0
while i < len(results):
    if results[i] > max:
        max = results[i]
        maxInd = i
    i += 1

if max == result:
  print("Rekord!")
else:
  print(f"Jobb eredmény: {max} ({maxInd})")
