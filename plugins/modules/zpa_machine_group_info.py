#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_machine_group import MachineGroupService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
author: William Guilherme (@willguibr)
description:
  - Provides details about (ID and/or Name) of a machine group resource.
module: zpa_trusted_network_info
short_description: Provides details about (ID and/or Name) of a machine group resource.
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the machine group.
    required: false
    type: str
  id:
    description:
      - ID of the machine group.
    required: false
    type: str

"""

EXAMPLES = """
- name: trusted network
  hosts: localhost
  tasks:
    - name: Gather information about all trusted network
      willguibr.zpacloud.zpa_trusted_network_info:
        #name: Corp-Trusted-Networks
        id: 216196257331282234
      register: networks
    - name: networks
      debug:
        msg: "{{ networks }}"

    - name: Gather Details of a Specific Machine Group by Name
      willguibr.zpacloud.zpa_machine_group_info:
        name: "Corp_Machine_Group"

    - name: Gather Details of a Specific Machine Group by ID
      willguibr.zpacloud.zpa_machine_group_info:
        id: "216196257331282583"
"""

RETURN = """
data:
    description: Machine Group Information
    returned: success
    elements: dict
    type: list
    "sample": [
        {
            "creation_time": "1638488366",
            "description": null,
            "enabled": true,
            "id": "216196257331291115",
            "modified_by": "216196257331281958",
            "modified_time": null,
            "name": "SGIO-MGR01"
        }
    ]
"""


def core(module):
    machine_group_name = module.params.get("name", None)
    machine_group_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = MachineGroupService(module, customer_id)
    machine_groups = []
    if machine_group_id is not None:
        machine_group = service.getByID(machine_group_id)
        if machine_group is None:
            module.fail_json(
                msg="Failed to retrieve Machine Group ID: '%s'" % (id))
        machine_groups = [machine_group]
    elif machine_group_name is not None:
        machine_group = service.getByName(machine_group_name)
        if machine_group is None:
            module.fail_json(
                msg="Failed to retrieve Machine Group Name: '%s'" % (machine_group_name))
        machine_groups = [machine_groups]
    else:
        machine_groups = service.getAll()
    module.exit_json(changed=False, data=machine_groups)


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=False),
        id=dict(type="str", required=False),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
