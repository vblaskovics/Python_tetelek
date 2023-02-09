import io
import os
import random
import time
from contextlib import redirect_stdout
from unittest.mock import patch
from statistics import mean


def readFile(fname):
    if (os.path.exists(fname)):
        return open(fname).read()
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


class textStyle:
    TITLE = "\033[95m"
    BOLD = "\033[1m"
    OK = "\033[92m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"


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

    initSubtask("Hatékony keresés", 2)
    try:
        code = readFile("03_feladat.py")
        lines = code.split('\n')
        lines[0] = 'nevek = ["David"] + ["John"] * 99999'
        code = '\n'.join(lines)
        runCode(code)
        print(state["out"])
        assertStringOut("Benne van")
    except Exception as e:
        print(e)
        subtaskFail()


task_1()
printTaskSummary()
task_2()
printTaskSummary()
task_3()
printTaskSummary()

# Summary
printTitle("Összegzés:")
print(f"Pontok:{state['score']}/{state['scoreMax']}")
print(f"Eredmény:{int((state['score'] / state['scoreMax']) * 100)}%")
