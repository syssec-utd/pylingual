"""
description: this module provides the function get fail response.
"""
from pistar_echo_agent.utilities.constants.response import RESPONSE

def get_fail_response(code, message):
    return (code, {RESPONSE.ERROR_CODE: code, RESPONSE.ERROR_MSG: message})