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
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_segment_group import SegmentGroupService
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import ZPAClientHelper
__metaclass__ = type

DOCUMENTATION = '''
---
module: zpa_segment_group
short_description: Create a segment group
description:
  - This module will create, retrieve, update or delete a specific segment group
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  applications:
    type: list
    elements: str
    required: False
    description: "This field is a json array of segment_group-connector-id only.
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
  enabled:
    type: bool
    required: False
    description: "This field defines if the server group is enabled or disabled."
  name:
    type: str
    required: True
    description: "This field defines the name of the server group."
  policy_migrated:
    type: bool
    required: False
  tcp_keep_alive_enabled:
    type: str
    required: False
  id:
    type: str
    description: ""
  state:
    description: "Whether the server group should be present or absent."
    default: present
    choices: ["present", "absent"]
    type: str

'''

EXAMPLES = r'''
- name: segment group
  hosts: localhost
  tasks:
    - name: Create an Segment group
      willguibr.zpacloud_ansible.zpa_segment_group:
        state: absent
        name: "Example Test"
        description: "Example Test"
        enabled: false
      register: segment_group
    - name: segment group
      debug:
        msg: "{{ segment_group }}"

'''

RETURN = r"""
data:
    description: Segment Group
    returned: success
    type: dict
    sample: {
                "app_connector_groups": [
                    "216196257331291924"
                ],
                "applications": [
                    "216196257331291981"
                ],
                "config_space": "DEFAULT",
                "description": "Browser Access Apps",
                "dynamic_discovery": false,
                "enabled": true,
                "id": "216196257331291969",
                "ip_anchored": false,
                "name": "Browser Access Apps",
                "servers": [
                    "216196257331291921"
                ]
            }
"""

def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = SegmentGroupService(module, customer_id)
    segment_group = dict()
    params = [
        "applications",
        "config_space",
        "description",
        "enabled",
        "id",
        "name",
        "policy_migrated",
        "tcp_keep_alive_enabled",
    ]
    for param_name in params:
        segment_group[param_name] = module.params.get(param_name, None)
    existing_segment_group = service.getByIDOrName(
        segment_group.get("id"), segment_group.get("name"))
    if existing_segment_group is not None:
        id = existing_segment_group.get("id")
        existing_segment_group.update(segment_group)
        existing_segment_group["id"] = id
    if state == "present":
        if existing_segment_group is not None:
            """Update"""
            service.update(existing_segment_group)
            module.exit_json(changed=True, data=existing_segment_group)
        else:
            """Create"""
            segment_group = service.create(segment_group)
            module.exit_json(changed=False, data=segment_group)
    elif state == "absent":
        if existing_segment_group is not None:
            service.delete(existing_segment_group.get("id"))
            module.exit_json(changed=False, data=existing_segment_group)
    module.exit_json(changed=False, data={})
    
def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        applications=dict(type='list', elements='str', required=False),
        config_space=dict(type='str', required=False,
                          default="DEFAULT", choices=["DEFAULT", "SIEM"]),
        description=dict(type='str', required=False),
        enabled=dict(type='bool', required=False),
        id=dict(type='str'),
        name=dict(type='str', required=True),
        policy_migrated=dict(type='bool', required=False),
        tcp_keep_alive_enabled=dict(type='str', required=False),

    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
