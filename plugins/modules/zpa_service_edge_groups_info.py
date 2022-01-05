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
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_service_edge_groups import ServiceEdgeGroupService
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = r"""
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

EXAMPLES = r'''
- name: App Connector Groups
  hosts: localhost
  tasks:
    - name: Gather information about all App Connector Groups
      willguibr.zpacloud_ansible.zpa_app_connector_groups_info:
        #name: "USA App Connector Group"
    - name: Gather information about all App Connector Groups
      willguibr.zpacloud_ansible.zpa_app_connector_groups_info:

    - name: Gather information about App Connector Group with given ID
      willguibr.zpacloud_ansible.zpa_app_connector_groups_info:
        id: "198288282"
      register: resp_out

    - name: Gather information about App Connector Group with given name
      willguibr.zpacloud_ansible.zpa_app_connector_groups_info:
        name: "example"
      register: resp_out
    - debug:
        msg: "{{ resp_out.name }}"
'''

RETURN = r"""
data:
    description: App Connector Group information
    returned: success
    elements: dict
    type: list
    sample: [
        {
          id                      = "82827282828",
          name                    = "Example",
          description             = "Example",
          enabled                 = true,
          city_country            = "California, US",
          country_code            = "US",
          latitude                = "37.3382082",
          longitude               = "-121.8863286",
          location                = "San Jose, CA, USA",
          upgrade_day             = "SUNDAY",
          upgrade_time_in_secs    = "66600",
          override_version_profile= true,
          version_profile_id      = 0,
          dns_query_type          = "IPV4"
        },
    ]
"""


def core(module):
    service_edge_name = module.params.get("name", None)
    service_edge_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = ServiceEdgeGroupService(module, customer_id)
    service_edges = []
    if service_edge_id is not None:
        service_edge = service.getByID(service_edge_id)
        if service_edge is None:
            module.fail_json(
                msg="Failed to retrieve Service Edge Group ID: '%s'" % (id))
        service_edges = [service_edge]
    elif service_edge_name is not None:
        service_edge = service.getByName(service_edge_name)
        if service_edge is None:
            module.fail_json(
                msg="Failed to retrieve Service Edge Group Name: '%s'" % (service_edge_name))
        service_edges = [service_edge]
    else:
        service_edges = service.getAll()
    module.exit_json(changed=False, data=service_edges)


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
