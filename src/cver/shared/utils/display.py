"""
    Cver Shared
    Utils
    Display
        Utility for helping making pretty displays.

"""


def print_dict(the_dict: dict, pad: int = 0) -> bool:
    """Formats a dict so it can be printed pretty.

    :example:
        ID:       37
        Name:     prometheus-operator/prometheus-operator
        Registry: quay.io
    """
    longest_key = 0
    for key, value in the_dict.items():
        key_str = str(key)
        if len(key_str) > longest_key:
            longest_key = len(key_str)
    padding = ""
    if pad > 0:
        for i in range(0, pad):
            padding += " "
    for key, value in the_dict.items():
        key_str = str(key)
        key_len = len(key_str)
        key_len_diff = longest_key - key_len
        spaces = " "
        for i in range(0, key_len_diff):
            spaces += " "
        print(f"{padding}{key}:{spaces}{value}")
    return True


def print_pagination_info(response: dict) -> bool:
    """Display pagination info for a collection."""
    print("\n")
    print("\tTotal: %s" % (response["info"]["total_objects"]))
    print("\tPage: %s/%s" % (response["info"]["current_page"], response["info"]["last_page"]))
    print("\tPer Page: %s" % response["info"]["per_page"])
    return True

# End File: cver/src/cver/shared/utils/display.py
