"""
    Cver Api
    Utils - Misc

"""
import traceback
import sys


def full_traceback() -> str:
    """Get the full traceback, useful for sending the traceback to the api if development."""
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    if exc is not None:
        del stack[-1]
    trc = 'Traceback (most recent call last):\n'
    stackstr = trc + ''.join(traceback.format_list(stack))
    if exc is not None:
        stackstr += '  ' + traceback.format_exc().lstrip(trc)
    return stackstr

# End File: cver/src/api/utils/misc.py
