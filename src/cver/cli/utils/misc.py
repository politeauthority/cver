"""
    Cver Cli
    Utils
    Misc

"""


def get_filters(filters: str) -> dict:
    """Split command line filters into a usable dictionary of key values."""
    ret_filters = {}
    if not filters:
        return ret_filters
    if "," in filters:
        split_filters = filters.split(",")
        for split_filter in split_filters:
            key, value = _get_filter_key_value(split_filters)
            if key and value:
                ret_filters[key] = value
    else:
        key, value = _get_filter_key_value(filters)
        ret_filters[key] = value
    return ret_filters


def _get_filter_key_value(filter_eq):
    """Split the filter into a key value"""
    if "=" not in filter_eq:
        return None, None
    split = filter_eq.split("=")
    return split[0], split[1]


# End File: cver/src/cver/cli/utils/misc.py
