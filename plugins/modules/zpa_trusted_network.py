#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Ansible module to manage Zscaler Private Access (ZPA) 2022
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


DOCUMENTATION = """
author: William Guilherme (@willguibr)
description:
- Provides details about a specific trusted network created in the Zscaler Private Access Mobile Portal
module: zpa_trusted_network
short_description: Provides details about a specific trusted network created in the Zscaler Private Access Mobile Portal
version_added: '1.0.0'
requirements:
- supported starting from zpa_api >= 1.0
options:
    name:
        description: The name of the trusted network to be exported.
        required: Required
        type: str
    
    network_id:
        description: The network_id of the trusted network to be exported.
        required: False
        type: str
"""


EXAMPLES = """
- name: Retrieving the network_id for the Trusted Network
  zpa_trusted_network:
    "name": "Corp-Trusted-Networks"
"""


RETURN = """
trusted_network:
  "name": "Corp-Trusted-Networks"
  returned: always.
  type: dict
"""