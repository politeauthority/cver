"""
    Cver Api
    Utilities
    SQL Tools

"""
from datetime import datetime
import logging
import json

from sqlescapy import sqlescape


def sql_safe(query_item):
    """Covert any item to a sql safe value where possible.
    """
    if not query_item:
        return query_item
    if isinstance(query_item, str) and query_item.isdigit():
        return query_item
    elif isinstance(query_item, datetime):
        return query_item
    elif isinstance(query_item, int):
        return query_item
    elif isinstance(query_item, dict):
        logging.warning("sql_safe cannot translate dict objects")
        query_item = json.dumps(query_item)
        return query_item
    elif isinstance(query_item, list):
        cleaned = []
        for item in query_item:
            cleaned.append(sqlescape(item))
        return ", ".join(cleaned)
    else:
        return sqlescape(query_item)


# End File: cver/src/api/utils/sql_tools.py
