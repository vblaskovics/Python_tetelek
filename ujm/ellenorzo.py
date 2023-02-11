import io
import os
import random
import time
from contextlib import redirect_stdout
from unittest.mock import patch
from statistics import mean


def readFile(fname):
    if (os.path.exists(fname)):
        return open(fname, mode="r", encoding="utf-8").read()
    return ""


def runCode(code):
    global state
    with redirect_stdout(io.StringIO()) as f:
        exec(code)
    state["out"] = f.getvalue()


def runFile(fname):
    code = readFile(fname)
    if (code):
        runCode(code)


# class textStyle:
#     TITLE = "\033[95m"
#     BOLD = "\033[1m"
#     OK = "\033[92m"
#     FAIL = "\033[91m"
#     ENDC = "\033[0m"
class textStyle:
    TITLE = ""
    BOLD = ""
    OK = ""
    FAIL = ""
    ENDC = ""


def printTitle(text):
    print(f"\n{textStyle.TITLE}{textStyle.BOLD}{text}{textStyle.ENDC}")


def printOk(text):
    global state
    print(f"✔ {textStyle.OK}{text}{textStyle.ENDC} ({state['valueSubtask']})")


def printFail(text):
    global state
    print(
        f"❌ {textStyle.FAIL}{text}{textStyle.ENDC} (0/{state['valueSubtask']})")


state = {
    "out": "",
    "taskName": "",
    "taskCount": 0,
    "subtaskName": "",
    "valueTask": 0,
    "valueSubtask": 0,
    "scoreTask": 0,
    "score": 0,
    "scoreMax": 0
}


def initNextTask(value):
    global state
    state["taskCount"] = int(state["taskCount"] + 1)
    state["taskName"] = f'{state["taskCount"]}. Feladat'
    state["valueTask"] = value
    state["scoreTask"] = 0
    state["scoreMax"] += state["valueTask"]
    printTitle(f"{state['taskName']} ({state['valueTask']})")


def initSubtask(name, value):
    global state
    state["subtaskName"] = name
    state["valueSubtask"] = value


def subtaskSuccess():
    global state
    printOk(state["subtaskName"])
    state["scoreTask"] += state["valueSubtask"]
    state["score"] += state["valueSubtask"]


def subtaskFail():
    global state
    printFail(state["subtaskName"])


def printTaskSummary():
    print(f"{state['scoreTask']}/{state['valueTask']}")


def readLastLineFromOut():
    global state
    outByLine = state["out"].split('\n')
    return outByLine[len(outByLine) - 2]


def assertValues(v1, v2):
    if (v1 == v2):
        subtaskSuccess()
    else:
        subtaskFail()


# Check the last number in the out to be equal with the given value
def assertIntOut(value):
    lastLine = readLastLineFromOut()
    assertValues(int(lastLine), value)


# Check the last float number in the out to be equal with the given value
def assertFloatOut(value):
    lastLine = readLastLineFromOut()
    assertValues(float(lastLine), value)


# Check the last line in the out to be equal with the given value
def assertStringOut(value):
    lastLine = readLastLineFromOut()
    assertValues(lastLine, value)


def assertCorrectFileName(fname):
    if (os.path.exists(fname)):
        subtaskSuccess()
    else:
        subtaskFail()
        return


def task_1():
    initNextTask(5)

    initSubtask("Helyes fájlnév", 1)
    assertCorrectFileName("01_feladat.py")

    initSubtask("Helyes eredmény", 2)
    try:
        runFile("01_feladat.py")
        assertIntOut(220)
    except:
        subtaskFail()

    initSubtask("Helyes eredmény módosított lista esetén", 2)
    try:
        code = readFile("01_feladat.py")
        originList = code.split('[')[1].split(']')[0]
        randomItem = random.randint(0, 100)
        newList = '10, 20, ' + str(randomItem)
        code = code.replace(originList, newList)
        runCode(code)
        assertIntOut(30 + randomItem)
    except:
        subtaskFail()


def task_2():
    initNextTask(5)

    initSubtask("Helyes fájlnév", 1)
    assertCorrectFileName("01_feladat.py")

    initSubtask("Helyes eredmény", 4)
    try:
        code = readFile("02_feladat.py")
        testResults = random.sample(range(1, 5), 3)
        with patch('builtins.input', side_effect=testResults):
            runCode(code)
        assertFloatOut(mean(testResults))
    except:
        subtaskFail()


def task_3():
    initNextTask(6)

    initSubtask("Helyes fájlnév", 1)
    assertCorrectFileName("03_feladat.py")

    initSubtask("nevek lista létrehozása", 1)
    try:
        code = readFile("03_feladat.py")
        code += '\nif "nevek" in locals():'
        code += '\n   print(nevek == ["Alice", "Bob", "Charlie", "David", "Emilio"])\n'
        runCode(code)
        assertStringOut("True")
    except:
        subtaskFail()

    initSubtask("David megtalálása", 2)
    try:
        runFile("03_feladat.py")
        assertStringOut("Benne van")
    except:
        subtaskFail()

    initSubtask("Gyors futásidő", 2)
    try:
        code = readFile("03_feladat.py")
        lines = code.split('\n')
        lines[0] = 'nevek = ["David"] + ["John"] * 999999'
        code = '\n'.join(lines)
        start = time.time()
        runCode(code)
        end = time.time()
        if (end - start) > 0.1:
            subtaskFail()
        else:
            subtaskSuccess()
    except Exception as e:
        print(e)
        subtaskFail()


def task_4():
    initNextTask(5)

    initSubtask("Helyes fájlnév", 1)
    assertCorrectFileName("04_feladat.py")

    initSubtask("Törpe megtalálása", 2)
    try:
        with patch('builtins.input', return_value="Kuka"):
            runFile("04_feladat.py")
        assertStringOut("Talált!")
    except:
        subtaskFail()

    initSubtask("Rossz találat jelzése", 2)
    try:
        with patch('builtins.input', return_value="Huba"):
            runFile("04_feladat.py")
        assertStringOut("Nem talált!")
    except:
        subtaskFail()

def task_5():
    initNextTask(6)

    initSubtask("Helyes fájlnév", 1)
    assertCorrectFileName("05_feladat.py")

    initSubtask("mylist lista létrehozása", 1)
    try:
        code = readFile("05_feladat.py")
        code += '\nif "mylist" in locals():'
        code += '\n   print("mylist exist")\n'
        runCode(code)
        assertStringOut("mylist exist")
    except:
        subtaskFail()

    initSubtask("Helyes végrehajtás", 4)
    try:
        code = readFile("05_feladat.py")
        part1 = code.split("mylist")
        part2 = part1[1].split("[")
        listValues = part2[1].split("]")[0]
        code = code.replace(listValues, "2, 6")
        runCode(code)
        result = int(readLastLineFromOut())
        assertValues(result == 6 or result == 12, True)
    except Exception as e:
        print(e)
        subtaskFail()

def task_6():
    initNextTask(8)

    initSubtask("Helyes fájlnév", 1)
    assertCorrectFileName("06_feladat.py")

    initSubtask("Helyes eredmény - Rekord", 3)
    try:
        code = readFile("06_feladat.py")
        with patch('builtins.input', return_value=100):
            runCode(code)
        fullout = state["out"]
        assertValues("Rekord!" in fullout, True)
    except:
        subtaskFail()

    initSubtask("Helyes eredmény - Már volt", 4)
    try:
        code = readFile("06_feladat.py")
        with patch('builtins.input', return_value=42):
            runCode(code)
        fullout = state["out"]
        assertValues("Már volt" in fullout, True)
    except:
        subtaskFail()
task_1()
printTaskSummary()
task_2()
printTaskSummary()
task_3()
printTaskSummary()
task_4()
printTaskSummary()
task_5()
printTaskSummary()
task_6()
printTaskSummary()



# Summary
printTitle("Összegzés:")
print(f"Pontok:{state['score']}/{state['scoreMax']}")
print(f"Eredmény:{int((state['score'] / state['scoreMax']) * 100)}%")
