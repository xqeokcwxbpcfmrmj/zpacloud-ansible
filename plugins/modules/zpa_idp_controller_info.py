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
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_idp_controller import IDPControllerService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
author: William Guilherme (@willguibr)
description:
  - Provides details about the (ID and/or Name) of an idp controller resource.
module: zpa_trusted_network_info
short_description: Provides details about the (ID and/or Name) of an idp controller resource.
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the Identity Provider.
    required: false
    type: str
  id:
    description:
      - ID of the of the Identity Provider.
    required: false
    type: str

"""

EXAMPLES = """
    - name: Gather Details of All IdP Controllers
      willguibr.zpacloud.zpa_idp_controller_info:

    - name: Gather Details of a Specific IdP Controller by Name
      willguibr.zpacloud.zpa_idp_controller_info:
        name: User_IdP_Name

    - name: Gather Details of a Specific IdP Controller by ID
      willguibr.zpacloud.zpa_idp_controller_info:
        id: "216196257331282583"

"""

RETURN = """
data:
    description: List of Identity Providers
    returned: success
    elements: dict
    type: list
        "data": [
            {
                "id": "216196257331285825",
                "name": "IdP_Name"
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
