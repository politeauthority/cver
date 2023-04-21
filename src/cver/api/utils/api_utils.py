"""
"""
from flask import request

def get_params():
    args = request.args
    return args