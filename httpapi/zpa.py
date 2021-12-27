# (c) 2018 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
author:
    - Michael Richardson (@mrichardson03)
httpapi : panos
short_description: HttpApi plugin for PAN-OS devices
description:
    - HttpApi plugin for PAN-OS devices
version_added: '1.0.0'
options:
    api_key:
        type: str
        description:
            - Use API key for authentication instead of username and password
        vars:
            - name: ansible_api_key
"""

import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from ansible.module_utils.basic import to_text
from ansible.module_utils.six.moves import urllib
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.plugins.httpapi import HttpApiBase
from ansible.utils.display import Display

display = Display()

# List of valid API error codes and names.
#
# Reference:
# https://help.zscaler.com/zpa/about-error-codes
_ZPA_API_ERROR_CODES = {
    "200": "Successful",
    "201": "Created",
    "204": "No Content",
    "400": "Bad Request",
    "401": "Unauthorized",
    "401": "Forbidden",
    "404": "Not Found",
    "429": "Exceeded the rate limit or quota",
    }