#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_idp_controller import IDPControllerService
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
      - Name of the browser certificate.
    required: false
    type: str
  id:
    description:
      - ID of the browser certificate.
    required: false
    type: str

"""

EXAMPLES = """
- name: browser certificate
  hosts: localhost
  tasks:
    - name: Gather information about all browser certificate
      willguibr.zpacloud_ansible.zpa_ba_certificate_info:
        #name: Corp-Trusted-Networks
        id: 216196257331282234
      register: certificates
    - name: certificates
      debug:
        msg: "{{ certificates }}"

"""

RETURN = r"""
data:
    description: Browser Certificate information
    returned: success
    elements: dict
    type: list
    data: [
            {
              "id": "12345",
              "name": "Root",
            },
            {
              "id": "12345",
              "name": "Client",
            },
            {
              "id": "1234567890",
              "name": "Connector",
            },
            {
              "id": "6574",
              "name": "Service Edge",
            },
            {
                "id": "10242",
                "name": "Isolation Client",
            }
    ]
"""


def core(module):
    idp_name = module.params.get("name", None)
    idp_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = IDPControllerService(module, customer_id)
    idp_controllers = []
    if idp_id is not None:
        idp_controller = service.getByID(idp_id)
        if idp_controller is None:
            module.fail_json(
                msg="Failed to retrieve IDP Controller ID: '%s'" % (id))
        idp_controllers = [idp_controller]
    elif idp_name is not None:
        idp_controller = service.getByName(idp_name)
        if idp_controller is None:
            module.fail_json(
                msg="Failed to retrieve IDP Controller Name: '%s'" % (idp_name))
        idp_controllers = [idp_controller]
    else:
        idp_controller = service.getAll()
    module.exit_json(changed=False, data=idp_controllers)


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
