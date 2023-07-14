"""
    Cver Shared
    Utils - Misc
    A bunch of misc tools to share between efforts.

"""


def strip_trailing_slash(the_string: str) -> str:
    """Strips trailing slashes if they exist."""
    if not the_string:
        return the_string
    if the_string[:-1] == "/":
        return the_string[:-1]
    return the_string

# End File: cver/src/shared/utils/misc.py
