import io
import os
from contextlib import redirect_stdout
from unittest.mock import patch
from contextlib import contextmanager


state = None


@contextmanager
def exam():
    global state
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
            "scoreMax": 0,
            "debug": True
        }
        yield

    except Exception as e:
        raise e

    finally:
        printSummary()


@contextmanager
def task(name=""):
    try:
        initNextTask(name)
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
        return runCode(code, input)


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


def initNextTask(name=""):
    global state
    state["taskCount"] = int(state["taskCount"] + 1)
    if name:
        state["taskName"] = name
    else:
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


def assertValueLesserThan(value1, value2):
    if (value1 < value2):
        subtaskSuccess()
    else:
        subtaskFail()


def assertValueGreaterThan(value1, value2):
    if (value1 > value2):
        subtaskSuccess()
    else:
        subtaskFail()


def assertLastLine(value):
    lastLine = readLastLineFromOut()
    if isinstance(value, int):
        assertValues(int(lastLine), value)
    elif isinstance(value, float):
        assertValues(float(lastLine), value)
    elif isinstance(value, bool):
        assertValues(bool(lastLine), value)
    else:
        assertValues(lastLine, value)


def assertFileName(fname):
    if (os.path.exists(fname)):
        subtaskSuccess()
    else:
        subtaskFail()
        return
