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
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_server_group import ServerGroupService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_server_group
short_description: Create/Update/Delete a Server Group.
description:
    - This module will Create/Update/Delete a Server Group.
author:
    - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
    applications:
      type: list
      elements: str
      required: False
      description: "This field is a json array of server_group-connector-id objects only."
    enabled:
      type: bool
      required: False
      description: "This field defines if the server group is enabled or disabled."
    dynamic_discovery:
      type: bool
      required: False
      description: "This field controls dynamic discovery of the servers."
    name:
      type: str
      required: True
      description: "This field defines the name of the server group."
    servers:
      type: list
      elements: str
      required: False
      description: "This field is a list of servers objects that are applicable only when dynamic discovery is disabled. Server name is required only in cases where the new servers need to be created in this API. For existing servers, pass only the serverId."
    app_connector_groups:
      type: list
      elements: str
      required: False
      description: "List of server_group-connector ID objects."
    config_space:
      type: str
      required: False
      description: ""
      default: "DEFAULT"
      choices: ["DEFAULT", "SIEM"]
    description:
      type: str
      required: False
      description: "This field is the description of the server group."
    id:
      type: str
      description: ""
    ip_anchored:
      type: bool
      required: False
      description: ""
    state:
      description: "Whether the server group should be present or absent."
      default: present
      choices: ["present", "absent"]
      type: str
"""

EXAMPLES = """
- name: Create/Update/Delete a Server Group
  willguibr.zpacloud.zpa_server_group:
    name: "All Other Services"
    description: "All Other Services"
    enabled: false
    dynamic_discovery: true
    app_connector_groups:
      - id: "216196257331291924"
    servers:
      - id: "216196257331291921"
    applications:
      - id: "216196257331291981"
"""

RETURN = """
data:
    description: App Connector Group
    returned: success
    type: dict
    sample: {
                "app_connector_groups": [
                    {"id": "216196257331291924", "name":"XXX"}
                ],
                "config_space": "DEFAULT",
                "description": "All Other Services",
                "dynamic_discovery": true,
                "enabled": true,
                "id": "216196257331291969",
                "ip_anchored": false,
                "name": "Browser Access Apps",
            }
"""


def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = ServerGroupService(module, customer_id)
    server_group = dict()
    params = [
        "id",
        "ip_anchored",
        "name",
        "config_space",
        "enabled",
        "description",
        "dynamic_discovery",
        "servers",
        "applications",
        "app_connector_groups",
    ]
    for param_name in params:
        server_group[param_name] = module.params.get(param_name, None)
    existing_server_group = service.getByIDOrName(
        server_group.get("id"), server_group.get("name"))
    if existing_server_group is not None:
        id = existing_server_group.get("id")
        existing_server_group.update(server_group)
        existing_server_group["id"] = id
    if state == "present":
        if existing_server_group is not None:
            """Update"""
            server_group = service.update(existing_server_group)
            module.exit_json(changed=True, data=server_group)
        else:
            """Create"""
            server_group = service.create(server_group)
            module.exit_json(changed=False, data=server_group)
    elif state == "absent":
        if existing_server_group is not None:
            service.delete(existing_server_group.get("id"))
            module.exit_json(changed=False, data=existing_server_group)
    module.exit_json(changed=False, data={})


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    id_name_spec = dict(type='list', elements='dict', options=dict(id=dict(
        type='str', required=True), name=dict(type='str', required=False)), required=False)
    argument_spec.update(
        id=dict(type='str'),
        ip_anchored=dict(type='bool', required=False),
        name=dict(type='str', required=True),
        config_space=dict(type='str', required=False,
                          default="DEFAULT", choices=["DEFAULT", "SIEM"]),
        enabled=dict(type='bool', required=False),
        description=dict(type='str', required=False),
        dynamic_discovery=dict(type='bool', required=False),
        servers=id_name_spec,
        applications=id_name_spec,
        app_connector_groups=id_name_spec,
        state=dict(type="str", choices=[
                   "present", "absent"], default="present"),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
