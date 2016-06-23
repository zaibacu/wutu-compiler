import os
import inspect
import tempfile
from logbook import Logger
from contextlib import contextmanager
modules = set()

from typing import List, Dict, TypeVar, Any, Callable
T = TypeVar("T")


def get_logger(name: str) -> Logger:
    """
    Returns a logging provider
    :param name: name for logger
    :return: logger
    """
    return Logger(name)

log = get_logger("util")


def location(directory: str) -> str:
    """
    :param directory: Directory in usual unix convention
    :return: OS-specialized
    """
    return os.path.join(*directory.split("/"))


def current(*directory: List[str]) -> str:
    """
    Locator service
    :param directory: what to look for
    :return: formed directory
    """
    return os.path.join(os.getcwd(), *directory)


def class_factory(name: str, base: T, **kwargs: Dict[str, Any]) -> object:
    """
    Dynamic class generator
    :param name: class name
    :param base: parent class
    :param: kwargs: optional params
    :return:
    """
    def __init__(self, **options):
        for key, val in options.items():
            setattr(self, key, val)
        self.__name__ = endpoint_name(name)
        base.__init__(self)

    struct = {"__init__": __init__}
    struct.update(kwargs)
    ctr = type(name, (base,), struct)
    return ctr


def endpoint_name(name: str) -> str:
    """
    Converts string from CameCase to under_score_case
    :param name: regular name
    :return:
    """
    LState = class_factory("LState", object)
    UState = class_factory("UState", object)

    state = UState
    words = []
    cur = []
    for l in name:
        if state == UState and l.isupper():
            cur.append(l.lower())
        elif state == UState and l.islower():
            state = LState
            cur.append(l)
        elif state == LState and l.isupper():
            words.append("".join(cur))
            cur = [l.lower()]
            state = UState
        else:
            cur.append(l)

    words.append("".join(cur))
    return "_".join(words)


def camel_case_name(name: str) -> str:
    """
    Converts string to CamelCase
    :param name: input string
    :return: CamelCased string
    """
    return "".join([words[0].upper() + words[1:] for words in name.split("_")])


def load_js(file: str, locator: Callable=current) -> str:
    """
    Loads JavaScript into memory
    :param file: javascript file
    :param locator: function which tells where to look for it
    :return: javascript as a string
    """
    with open(locator(file)) as f:
        raw = f.read()

    return raw


def get_request_args() -> tuple:
    """
    Returns arguments passed to request
    :return:
    """
    return request.args


def get_request_json() -> dict:
    """
    Returns json arguments passed to request
    :return:
    """
    import json

    def first_non_empty(arr):
        for obj in arr:
            if len(obj.keys()) > 0:
                return obj

        return {}

    return first_non_empty([request.get_json(), json.loads(request.data.decode("utf-8"))])


def is_stub(method: Callable) -> bool:
    """
    Checks if method is stub
    :param method:
    :return:
    """
    return hasattr(method, "__stub__")


@contextmanager
def temp_file():
    """
    Creates a temp file and deletes it afterwards
    :return:
    """
    temp = tempfile.NamedTemporaryFile(delete=False)
    try:
        yield temp
    finally:
        temp.close()
        os.unlink(temp.name)


@contextmanager
def timer(title: str) -> None:
    """
    Measures time elapsed in current block
    :param title: Name of block to be visible in output
    :return:
    """
    from time import perf_counter as pc
    start = pc()
    try:
        yield
    finally:
        timediff = (pc() - start) * 1000
        log.debug("It took {0} ms to execute block '{1}'".format(timediff, title))
