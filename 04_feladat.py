print("Írd be az egyik törpe nevét!")
torpe = input()
torpek = ["Tudor", "Vidor", "Morgó", "Szundi", "Szende", "Hapci", "Kuka"]

i = 0
while i < len(torpek) and torpek[i] != torpe:
    i += 1

if i < len(torpek):
    print("Talált!")
else:
    print("Nem talált!")