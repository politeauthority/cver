"""
    Cver Cli
    Utils
    Pretty

"""
import logging
from rich.console import Console
from rich.table import Table


def entity(entity, fields: list = [], pad: int = 0) -> bool:
    """Formats a dict so it can be printed pretty.

    :example:
        ID:       37
        Name:     prometheus-operator/prometheus-operator
        Registry: quay.io
    """
    display_fields = _get_display_fields(entity, fields)
    longest_key = _get_longest_key(display_fields)
    padding = ""
    if pad > 0:
        for i in range(0, pad):
            padding += " "
    for field in display_fields:
        spaces = _get_spaces(field, longest_key, len(field))
        value = _get_display_value(entity, field)
        print(f"{padding}{field}:{spaces}{value}")
    return True


def entity_table(entity, fields: list = []) -> bool:
    """Print a single Cver Client entity in a table format."""
    rj = entity.response_last_json
    table = Table(title=rj["object_type"].title())
    table.add_column("Field", justify="right", style="cyan", no_wrap=True)
    table.add_column("Value", justify="right", style="green")
    for field_name, field_info in entity.field_map.items():
        value = getattr(entity, field_name)
        if field_info["type"] == "datetime":
            table.add_row(field_name, date_display(value))
        else:
            table.add_row(field_name, str(value))
    console = Console()
    console.print(table)
    return True


def entities(entities: list, fields: list = [], pad: int = 0) -> bool:
    """Formats a dict so it can be printed pretty.

    :example:
        ID:       37
        Name:     prometheus-operator/prometheus-operator
        Registry: quay.io
    """
    return None


def date_display(the_date) -> str:
    """Formats a dict so it can be printed pretty.
    """
    if not the_date:
        return ""
    local = the_date.to("US/Mountain")
    pretty_display = "%s (%s)" % (local.format("hh:mm:ss A"), the_date.humanize())
    return pretty_display


def print_pagination(page_info: dict) -> bool:
    print("\n")
    print("Info")
    print("\tTotal: %s" % page_info["total_objects"])
    print("\tPage: %s/%s" % (page_info["current_page"], page_info["last_page"]))
    print("\tPer Page: %s" % page_info["per_page"])
    return True


def _get_longest_key(display_fields: list) -> int:
    longest_key = 0
    for field in display_fields:
        if len(field) > longest_key:
            longest_key = len(field)
    return longest_key


def _get_spaces(field: str, longest_key: int, key_len: int) -> str:
    key_len = len(field)
    key_len_diff = longest_key - key_len
    spaces = " "
    for i in range(0, key_len_diff):
        spaces += " "
    return spaces


def _get_display_fields(entity, request_fields: list = []) -> list:
    all_fields = []
    display_fields = []
    request_field_len = len(request_fields)
    for field, f_info in entity.field_map.items():
        all_fields.append(field)
        if request_field_len > 0:
            if field in request_fields:
                display_fields.append(field)
            else:
                logging.warning("Field: %s does not exist in model %s field map" % field, entity)

    if request_field_len == 0:
        return all_fields

    return display_fields


def _get_display_value(entity, field):
    value = getattr(entity, field)
    if not value:
        return None
    if entity.field_map[field]["type"] == "datetime":
        value = date_display(value)

    return value


# End File: cver/src/cver/cli/utils/pretty.py
