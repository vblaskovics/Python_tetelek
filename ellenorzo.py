import random
import time
from statistics import mean

import njit_corrector as nc

with nc.exam():

    with nc.task():

        with nc.subtask("Helyes fájlnév", 1):
            nc.assertCorrectFileName("01_feladat.py")

        with nc.subtask("Helyes eredmény", 2):
            nc.runFile("01_feladat.py")
            nc.assertIntOut(220)

        with nc.subtask("Helyes eredmény módosított lista esetén", 2):
            code = nc.readFile("01_feladat.py")
            originList = code.split('[')[1].split(']')[0]
            randomItem = random.randint(0, 100)
            newList = '10, 20, ' + str(randomItem)
            code = code.replace(originList, newList)
            nc.runCode(code)
            nc.assertIntOut(30 + randomItem)

    with nc.task():

        with nc.subtask("Helyes fájlnév", 1):
            nc.assertCorrectFileName("01_feladat.py")

        with nc.subtask("Helyes eredmény", 4):
            code = nc.readFile("02_feladat.py")
            testResults = random.sample(range(1, 5), 3)
            nc.runCode(code, testResults)
            nc.assertFloatOut(mean(testResults))

    with nc.task():

        with nc.subtask("Helyes fájlnév", 1):
            nc.assertCorrectFileName("03_feladat.py")

        with nc.subtask("nevek lista létrehozása", 1):
            code = nc.readFile("03_feladat.py")
            code += '\nif "nevek" in locals():'
            code += '\n   print(nevek == ["Alice", "Bob", "Charlie", "David", "Emilio"])\n'
            nc.runCode(code)
            nc.assertStringOut("True")

        with nc.subtask("David megtalálása", 2):
            nc.runFile("03_feladat.py")
            nc.assertStringOut("Benne van")

        with nc.subtask("Gyors futásidő", 2):
            code = nc.readFile("03_feladat.py")
            lines = code.split('\n')
            lines[0] = 'nevek = ["David"] + ["John"] * 999999'
            code = '\n'.join(lines)
            start = time.time()
            nc.runCode(code)
            end = time.time()
            if (end - start) > 0.1:
                nc.subtaskFail()
            else:
                nc.subtaskSuccess()

    with nc.task():

        with nc.subtask("Helyes fájlnév", 1):
            nc.assertCorrectFileName("04_feladat.py")

        with nc.subtask("Törpe megtalálása", 2):
            nc.runFile("04_feladat.py", "Kuka")
            nc.assertStringOut("Talált!")

        with nc.subtask("Rossz találat jelzése", 2):
            nc.runFile("04_feladat.py", "Huba")
            nc.assertStringOut("Nem talált!")

    with nc.task():

        with nc.subtask("Helyes fájlnév", 1):
            nc.assertCorrectFileName("05_feladat.py")

        with nc.subtask("mylist lista létrehozása", 1):
            code = nc.readFile("05_feladat.py")
            code += '\nif "mylist" in locals():'
            code += '\n   print("mylist exist")\n'
            nc.runCode(code)
            nc.assertStringOut("mylist exist")

        with nc.subtask("Helyes végrehajtás", 4):
            code = nc.readFile("05_feladat.py")
            part1 = code.split("mylist")
            part2 = part1[1].split("[")
            listValues = part2[1].split("]")[0]
            code = code.replace(listValues, "2, 6")
            nc.runCode(code)
            result = int(nc.readLastLineFromOut())
            nc.assertValues(result == 6 or result == 12, True)

    with nc.task():

        with nc.subtask("Helyes fájlnév", 1):
            nc.assertCorrectFileName("06_feladat.py")

        with nc.subtask("Helyes eredmény - Rekord", 3):
            nc.runFile("06_feladat.py", 100)
            fullout = nc.state["out"]
            nc.assertValues("Rekord!" in fullout, True)

        with nc.subtask("Helyes eredmény - Már volt", 4):
            nc.runFile("06_feladat.py", 42)
            fullout = nc.state["out"]
            nc.assertValues("Már volt" in fullout, True)
