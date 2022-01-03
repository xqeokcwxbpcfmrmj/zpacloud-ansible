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
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.trusted_network import TrustedNetworkService
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
      willguibr.zpa.zpa_trusted_network_info:
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
