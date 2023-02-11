import random
import time
from statistics import mean

import py_corrector as pc


def task_1():
    pc.initNextTask(5)

    pc.initSubtask("Helyes fájlnév", 1)
    pc.assertCorrectFileName("01_feladat.py")

    pc.initSubtask("Helyes eredmény", 2)
    try:
        pc.runFile("01_feladat.py")
        pc.assertIntOut(220)
    except:
        pc.subtaskFail()

    pc.initSubtask("Helyes eredmény módosított lista esetén", 2)
    try:
        code = pc.readFile("01_feladat.py")
        originList = code.split('[')[1].split(']')[0]
        randomItem = random.randint(0, 100)
        newList = '10, 20, ' + str(randomItem)
        code = code.replace(originList, newList)
        pc.runCode(code)
        pc.assertIntOut(30 + randomItem)
    except Exception as e:
        print(e)
        pc.subtaskFail()


def task_2():
    pc.initNextTask(5)

    pc.initSubtask("Helyes fájlnév", 1)
    pc.assertCorrectFileName("01_feladat.py")

    pc.initSubtask("Helyes eredmény", 4)
    try:
        code = pc.readFile("02_feladat.py")
        testResults = random.sample(range(1, 5), 3)
        pc.runCode(code, testResults)
        pc.assertFloatOut(mean(testResults))
    except Exception as e:
        print(e)
        pc.subtaskFail()


def task_3():
    pc.initNextTask(6)

    pc.initSubtask("Helyes fájlnév", 1)
    pc.assertCorrectFileName("03_feladat.py")

    pc.initSubtask("nevek lista létrehozása", 1)
    try:
        code = pc.readFile("03_feladat.py")
        code += '\nif "nevek" in locals():'
        code += '\n   print(nevek == ["Alice", "Bob", "Charlie", "David", "Emilio"])\n'
        pc.runCode(code)
        pc.assertStringOut("True")
    except:
        pc.subtaskFail()

    pc.initSubtask("David megtalálása", 2)
    try:
        pc.runFile("03_feladat.py")
        pc.assertStringOut("Benne van")
    except:
        pc.subtaskFail()

    pc.initSubtask("Gyors futásidő", 2)
    try:
        code = pc.readFile("03_feladat.py")
        lines = code.split('\n')
        lines[0] = 'nevek = ["David"] + ["John"] * 999999'
        code = '\n'.join(lines)
        start = time.time()
        pc.runCode(code)
        end = time.time()
        if (end - start) > 0.1:
            pc.subtaskFail()
        else:
            pc.subtaskSuccess()
    except:
        pc.subtaskFail()


def task_4():
    pc.initNextTask(5)

    pc.initSubtask("Helyes fájlnév", 1)
    pc.assertCorrectFileName("04_feladat.py")

    pc.initSubtask("Törpe megtalálása", 2)
    try:
        pc.runFile("04_feladat.py", "Kuka")
        pc.assertStringOut("Talált!")
    except:
        pc.subtaskFail()

    pc.initSubtask("Rossz találat jelzése", 2)
    try:
        pc.runFile("04_feladat.py", "Huba")
        pc.assertStringOut("Nem talált!")
    except:
        pc.subtaskFail()


def task_5():
    pc.initNextTask(6)

    pc.initSubtask("Helyes fájlnév", 1)
    pc.assertCorrectFileName("05_feladat.py")

    pc.initSubtask("mylist lista létrehozása", 1)
    try:
        code = pc.readFile("05_feladat.py")
        code += '\nif "mylist" in locals():'
        code += '\n   print("mylist exist")\n'
        pc.runCode(code)
        pc.assertStringOut("mylist exist")
    except:
        pc.subtaskFail()

    pc.initSubtask("Helyes végrehajtás", 4)
    try:
        code = pc.readFile("05_feladat.py")
        part1 = code.split("mylist")
        part2 = part1[1].split("[")
        listValues = part2[1].split("]")[0]
        code = code.replace(listValues, "2, 6")
        pc.runCode(code)
        result = int(pc.readLastLineFromOut())
        pc.assertValues(result == 6 or result == 12, True)
    except:
        pc.subtaskFail()


def task_6():
    pc.initNextTask(8)

    pc.initSubtask("Helyes fájlnév", 1)
    pc.assertCorrectFileName("06_feladat.py")

    pc.initSubtask("Helyes eredmény - Rekord", 3)
    try:
        pc.runFile("06_feladat.py", 100)
        fullout = pc.state["out"]
        pc.assertValues("Rekord!" in fullout, True)
    except:
        pc.subtaskFail()

    pc.initSubtask("Helyes eredmény - Már volt", 4)
    try:
        pc.runFile("06_feladat.py", 42)
        fullout = pc.state["out"]
        pc.assertValues("Már volt" in fullout, True)
    except:
        pc.subtaskFail()


task_1()
pc.printTaskSummary()
task_2()
pc.printTaskSummary()
task_3()
pc.printTaskSummary()
task_4()
pc.printTaskSummary()
task_5()
pc.printTaskSummary()
task_6()
pc.printTaskSummary()


# Summary
pc.printTitle("Összegzés:")
