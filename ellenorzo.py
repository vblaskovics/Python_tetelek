import io
import os
from contextlib import redirect_stdout


def runCode(code):
    global state
    with redirect_stdout(io.StringIO()) as f:
        exec(code)
    state["out"] = f.getvalue()


def runFile(fname):
    runCode(open(fname).read())


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
    print(
        f"✔ {textStyle.OK}{text}{textStyle.ENDC} ({state['valueSubtask']})")


def printFail(text):
    global state
    print(f"❌ {textStyle.FAIL}{text}{textStyle.ENDC} (0/{state['valueTask']})")


state = {
    "out": "",
    "taskName": "",
    "subtaskName": "",
    "valueTask": 0,
    "valueSubtask": 0,
    "scoreTask": 0,
    "score": 0,
    "scoreMax": 0
}


def initTask(name, value):
    global state
    state["taskName"] = name
    state["valueTask"] = value
    state["scoreMax"] += state["valueTask"]
    printTitle(f"1. Feladat ({state['valueTask']})")


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


def isOutNumberEqual(value):
    global state
    return int(state["out"]) == value 


def task_1():
    initTask("1. Feladat", 4)
    
    initSubtask("Helyes fájlnév", 1)
    if (os.path.exists("01_feladat.py")):
        subtaskSuccess()
    else:
        subtaskFail()
        return
    
    initSubtask("Helyes eredmény", 3)
    runFile("01_feladat.py")
    if(isOutNumberEqual(220)):
        subtaskSuccess()
    else:
        subtaskFail()
    
    printTaskSummary()


task_1()




# Summary

printTitle("Összegzés:")
print(f"Pontok:{state['score']}/{state['scoreMax']}")
