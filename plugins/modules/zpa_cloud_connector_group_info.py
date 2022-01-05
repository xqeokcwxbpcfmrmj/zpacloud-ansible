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
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_cloud_connector_group import CloudConnectorGroupService
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = r"""
---
module: zpa_app_connector_groups_info
short_description: Gather information about cloud connector group(s)
description:
  - This module can be used to gather information about cloud connector group(s)
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  name:
    description:
      - Name of the Cloud Connector Group.
    required: false
    type: str
  id:
    description:
      - ID of the Cloud Connector Group.
    required: false
    type: str

"""

EXAMPLES = r'''
- name: Cloud Connector Group
  hosts: localhost
  tasks:
    - name: Gather information about specific Cloud Connector Group by name
      willguibr.zpacloud_ansible.zpa_cloud_connector_group_info:
        name: "zs-cc-vpc-096108eb5d9e68d71-ca-central-1a"
      register: connector_group
    - debug:
        msg: "{{ connector_group.name }}"

    - name: Gather information about specific Cloud Connector Group by ID
      willguibr.zpacloud_ansible.zpa_cloud_connector_group_info:
        id: "216196257331292018"
      register: connector_group
    - debug:
        msg: "{{ connector_group.id }}"

    - name: Gather information about all Cloud Connector Groups
      willguibr.zpacloud_ansible.zpa_cloud_connector_group_info:
      register: connector_group
    - debug:
        msg: "{{ connector_group }}"
'''

RETURN = r"""
data:
    description: Cloud Connector Group information
    returned: success
    elements: dict
    type: list
    sample: [
            {
                "cloud_connectors": [
                    {
                        "creationTime": "1639806553",
                        "enabled": true,
                        "fingerprint": "ami-0796fdf37518f905e_i-04ef329486bc7f2f4:=&gt;36788942",
                        "id": "216196257331292018",
                        "issuedCertId": "480193",
                        "modifiedBy": "3",
                        "modifiedTime": "1639806554",
                        "name": "zs-cc-vpc-096108eb5d9e68d71-ca-central-1aProvKey-1639806553869"
                    }
                ],
                "creation_time": "1639806438",
                "description": "Auto created from ami-0796fdf37518f905e_i-04ef329486bc7f2f4",
                "enabled": true,
                "geolocation_id": null,
                "id": "216196257331292017",
                "modified_by": "72057594037929625",
                "modified_time": null,
                "name": "zs-cc-vpc-096108eb5d9e68d71-ca-central-1a",
                "zia_cloud": "zscalerthree.net",
                "zia_org_id": "24326813"
            }
    ]
"""


def core(module):
    cloud_connector_name = module.params.get("name", None)
    cloud_connector_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = CloudConnectorGroupService(module, customer_id)
    connectors = []
    if cloud_connector_id is not None:
        connector = service.getByID(cloud_connector_id)
        if connector is None:
            module.fail_json(
                msg="Failed to retrieve App Connector Group ID: '%s'" % (id))
        connectors = [connector]
    elif cloud_connector_name is not None:
        connector = service.getByName(cloud_connector_name)
        if connector is None:
            module.fail_json(
                msg="Failed to retrieve App Connector Group Name: '%s'" % (cloud_connector_name))
        connectors = [connector]
    else:
        connectors = service.getAll()
    module.exit_json(changed=False, data=connectors)


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
