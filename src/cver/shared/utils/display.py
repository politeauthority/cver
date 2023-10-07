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
        if len(key) > longest_key:
            longest_key = len(key)
    padding = ""
    if pad > 0:
        for i in range(0, pad):
            padding += " "
    for key, value in the_dict.items():
        key_len = len(key)
        key_len_diff = longest_key - key_len
        spaces = " "
        for i in range(0, key_len_diff):
            spaces += " "
        print(f"{padding}{key}:{spaces}{value}")
    return True
