from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
import time
from functools import reduce

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection, ConnectionError