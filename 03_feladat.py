nevek = ['Alice', "Bob", "Charlie", "David", "Emilio"]

# i = 0
# while i < len(nevek) and nevek[i] != "David":
#     i += 1

# if i < len(nevek):
#     print("Benne van")
# else:
#     print("Nincs benne")

talalat = False
print(len(nevek))
i = 0
while i < len(nevek):
    if nevek[i] == "David":
        talalat = True
    i += 1

if talalat:
    print("Benne van")
else:
    print("Nincs benne")