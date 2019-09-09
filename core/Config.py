import os

def getValue(param):
    """ Returns the value from configuration """
    return os.environ.get("A4_" + param)

def getRawValue(param):
    return os.environ.get(param)