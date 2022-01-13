#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_machine_group import MachineGroupService
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = r"""
---
author: William Guilherme (@willguibr)
description:
  - Provides details about a specific trusted network created in the Zscaler Private Access Mobile Portal
module: zpa_trusted_network_info
short_description: Provides details about a specific trusted network created in the Zscaler Private Access Mobile Portal
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the trusted network.
    required: false
    type: str
  id:
    description:
      - ID of the trusted network.
    required: false
    type: str

"""

EXAMPLES = """
- name: trusted network
  hosts: localhost
  tasks:
    - name: Gather information about all trusted network
      willguibr.zpacloud_ansible.zpa_trusted_network_info:
        #name: Corp-Trusted-Networks
        id: 216196257331282234
      register: networks
    - name: networks
      debug:
        msg: "{{ networks }}"

"""

RETURN = r"""
data:
    description: Trusted Network information
    returned: success
    elements: dict
    type: list
    sample: [
      {
          "id": "216196257331282234",
          "modified_time": "1631935891",
          "creation_time": "1625992655",
          "modified_by": "72057594037928115",
          "name": "Corp-Trusted-Networks",
          "network_id": "869fbea4-799d-422a-984f-d40fbe53bc02",
          "zscaler_cloud": "zscalerthree"
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
