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
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_app_connector_group import AppConnectorGroupService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_app_connector_groups_info
short_description: Gather information about an app connector group
description:
  - This module can be used to gather information about an app connector group.
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  name:
    description:
      - Name of the App Connector Group.
    required: false
    type: str
  id:
    description:
      - ID of the App Connector Group.
    required: false
    type: str
"""

EXAMPLES = """
- name: Gather Details of all App Connector Groups
  willguibr.zpacloud.zpa_app_connector_groups_info:
  register: all_app_connector

- debug:
    msg: "{{ all_app_connector }}"

- name: Gather Details of a Specific App Connector Groups by Name
  willguibr.zpacloud.zpa_app_connector_groups_info:
    name: "Example App Connector Group"
  register: app_connector_name

- debug:
    msg: "{{ app_connector_name }}"

- name: Gather Details of a Specific App Connector Groups by ID
  willguibr.zpacloud.zpa_app_connector_groups_info:
    id: "216196257331292046"
  register: app_connector_id

- debug:
    msg: "{{ app_connector_id }}"   
"""

RETURN = """
# Default return values
"""


def core(module):
    app_name = module.params.get("name", None)
    app_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = AppConnectorGroupService(module, customer_id)
    apps = []
    if app_id is not None:
        app = service.getByID(app_id)
        if app is None:
            module.fail_json(
                msg="Failed to retrieve App Connector Group ID: '%s'" % (id))
        apps = [app]
    elif app_name is not None:
        app = service.getByName(app_name)
        if app is None:
            module.fail_json(
                msg="Failed to retrieve App Connector Group Name: '%s'" % (app_name))
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
