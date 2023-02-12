import io
import os
from contextlib import redirect_stdout
from unittest.mock import patch
from contextlib import contextmanager


state = None


@contextmanager
def exam():
    try:
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
        yield

    except Exception as e:
        raise e

    finally:
        printSummary()


@contextmanager
def task():
    try:
        initNextTask()
        yield

    except Exception as e:
        raise e

    finally:
        closeTask()


@contextmanager
def subtask(name, value):
    try:
        initSubtask(name, value)
        yield

    except Exception as e:
        catchError(e)


class PyCorrector:
    def __init__(self):
        self.state = {
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


def readFile(fname):
    if (os.path.exists(fname)):
        return open(fname, mode="r", encoding="utf-8").read()
    return ""


def execCode(code):
    global state
    with redirect_stdout(io.StringIO()) as f:
        exec(code)
    state["out"] = f.getvalue()


def runCode(code, input=None):
    if input is None:
        execCode(code)
    elif type(input) is list:
        with patch('builtins.input', side_effect=input):
            execCode(code)
    else:
        with patch('builtins.input', return_value=input):
            execCode(code)


def runFile(fname, input=None):
    code = readFile(fname)
    if code:
        runCode(code, input)


def printTitle(text):
    print(f"\n{text}")
    print("".join(["="]*30))


def printOk(text):
    global state
    print(f"✔ {text} ({state['valueSubtask']})")


def printFail(text):
    global state
    print(
        f"❌ {text} (0/{state['valueSubtask']})")


def printSummary():
    printTitle("Összegzés:")
    print(f"Pontok:{state['score']}/{state['scoreMax']}")
    print(f"Eredmény:{int((state['score'] / state['scoreMax']) * 100)}%")


state = {
    "debug": False,
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


def initNextTask():
    global state
    state["taskCount"] = int(state["taskCount"] + 1)
    state["taskName"] = f'{state["taskCount"]}. Feladat'
    state["valueTask"] = 0
    state["scoreTask"] = 0
    printTitle(state['taskName'])


def initSubtask(name, value):
    global state
    state["subtaskName"] = name
    state["valueSubtask"] = value
    state["valueTask"] += state["valueSubtask"]


def catchError(e):
    if state["debug"]:
        print(e)
    subtaskFail()


def subtaskSuccess():
    global state
    printOk(state["subtaskName"])
    state["scoreTask"] += state["valueSubtask"]
    state["score"] += state["valueSubtask"]


def subtaskFail():
    global state
    printFail(state["subtaskName"])


def closeTask():
    state["scoreMax"] += state["valueTask"]
    printTaskSummary()


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
