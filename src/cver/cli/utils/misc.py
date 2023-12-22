"""
    Cver Cli
    Utils
    Misc

"""


def collect_args(the_args) -> dict:
    """Collection Arguments. Parses and formats arguments for a collection query."""
    ret = {}
    if the_args.page:
        ret["page"] = the_args.page
    if the_args.order:
        order_by = parse_cli_eq(the_args.order)
        field_name = next(iter(order_by))
        ret["order_by"] = {
            "field": field_name,
            "direction": order_by[field_name]
        }
    return ret


def parse_cli_eq(the_arg) -> dict:
    """Parse a single argument into a key value.
    ex "--order cve_critical_int=desc" -> {"cve_critical_int": "desc"}
    """
    if "=" not in the_arg:
        return {}
    return {the_arg.split("=")[0]: the_arg.split("=")[1]}

# End File: cver/src/cver/cli/utils/misc.py
