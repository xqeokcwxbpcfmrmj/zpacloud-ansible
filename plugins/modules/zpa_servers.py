#!/usr/bin/python
# (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: zpa_servers
short_description: Create server objects in the ZPA portal
description:
    - Create server group objects in the ZPA portal
author:
    - William Guilherme (@willguibr)
version_added: '1.0.0'
options:
    name:
        description:
            - This field defines the name of the server to create.
        required: true
        type: str
    app_server_group_ids:
        description:
            - This field defines the list of server groups IDs.
        required: false
        type: list
        elements: str
    enabled:
        description:
            - This field defines the status of the server, true or false.
        required: false
        type: bool
    description:
        description:
            - This field defines the description of the server to create.
        required: false
        type: str
    config_space:
        description:
            - This field defines the type of the server, DEFAULT or SIEM.
        required: false
        type: str
        elements: str
"""

EXAMPLES = """
# Create a server object
  - name: example_server
    zpa_server:
      name: "example"
      description: "example"
      enable: true
      app_server_group_ids: ['']
"""

RETURN = """
# Default return values
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.zscaler.zpa.plugins.module_utils.zpa import (
    get_connection,
)