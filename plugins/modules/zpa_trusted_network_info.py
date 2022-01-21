#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_trusted_network import TrustedNetworkService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
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
- name: Get Information About All Trusted Networks
  willguibr.zpacloud.zpa_trusted_network_info:
  register: all_networks
  
- debug:
    msg: "{{ all_networks }}"
    
- name: Get information about Trusted Networks by Name
  willguibr.zpacloud.zpa_trusted_network_info:
    name: Corp-Trusted-Networks
  register: network_id
  
- debug:
    msg: "{{ network_id }}"

- name: Get information about Trusted Networks by ID
  willguibr.zpacloud.zpa_trusted_network_info:
    id: 216196257331282234
  register: network_id

- debug:
    msg: "{{ network_id }}"
"""

RETURN = """
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
    app_name = module.params.get("name", None)
    app_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = TrustedNetworkService(module, customer_id)
    apps = []
    if app_id is not None:
        app = service.getByID(app_id)
        if app is None:
            module.fail_json(
                msg="Failed to retrieve Trusted Network ID: '%s'" % (id))
        apps = [app]
    elif app_name is not None:
        app = service.getByName(app_name)
        if app is None:
            module.fail_json(
                msg="Failed to retrieve Trusted Network Name: '%s'" % (app_name))
        apps = [app]
    else:
        apps = service.getAll()
    module.exit_json(changed=False, data=apps)


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
