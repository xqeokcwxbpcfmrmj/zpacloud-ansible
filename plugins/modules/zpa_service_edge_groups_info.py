#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_service_edge_groups import ServiceEdgeGroupService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_app_connector_groups_info
short_description: Get details (ID and/or Name) of a Service Edge Group.
description:
  - This module can be used to Get details (ID and/or Name) of a Service Edge Group.
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  name:
    description:
      - Name of the Service Edge Group..
    required: false
    type: str
  id:
    description:
      - ID of the Service Edge Group..
    required: false
    type: str

"""

<<<<<<< HEAD
EXAMPLES = """
- name: Gather information about all Service Edge Groups
  willguibr.zpacloud.zpa_service_edge_groups_info:
    
- name: Gather information about all Service Edge Groups by Name
  willguibr.zpacloud.zpa_service_edge_groups_info:
    name: "Example Service Edge Group"
    
- name: Gather information about all Service Edge Groups by ID
  willguibr.zpacloud.zpa_service_edge_groups_info:
    id: "216196257331292046"
"""
=======
EXAMPLES = r'''
- name: App Connector Groups
  hosts: localhost
  tasks:
    - name: Gather information about all App Connector Groups
      willguibr.zpacloud.zpa_app_connector_groups_info:
        #name: "USA App Connector Group"
    - name: Gather information about all App Connector Groups
      willguibr.zpacloud.zpa_app_connector_groups_info:

    - name: Gather information about App Connector Group with given ID
      willguibr.zpacloud.zpa_app_connector_groups_info:
        id: "198288282"
      register: resp_out

    - name: Gather information about App Connector Group with given name
      willguibr.zpacloud.zpa_app_connector_groups_info:
        name: "example"
      register: resp_out
    - debug:
        msg: "{{ resp_out.name }}"
'''
>>>>>>> master

RETURN = """
data:
    description: App Connector Group information
    returned: success
    elements: dict
    type: list
    sample: [
            {
              "city_country": "Langley, CA",
              "country_code": "CA",
              "description": "Canada Service Edge Group",
              "enabled": true,
              "geolocation_id": null,
              "id": "216196257331291917",
              "is_public": "FALSE",
              "latitude": "49.1041779",
              "location": "Langley City, BC, Canada",
              "longitude": "-122.6603519",
              "name": "Canada Service Edge Group",
              "override_version_profile": true,
              "service_edges": [],
              "trusted_networks": [
                  {
                      "creation_time": "1625992655",
                      "id": "216196257331282234",
                      "modified_by": "72057594037928115",
                      "modified_time": "1631935891",
                      "name": "Corp-Trusted-Networks",
                      "network_id": "869fbea4-799d-422a-984f-d40fbe53bc02",
                      "zscaler_cloud": "zscalerthree"
                  }
              ],
              "upgrade_day": "SUNDAY",
              "upgrade_time_in_secs": "66600",
              "version_profile_id": "2",
              "version_profile_name": "New Release",
              "version_profile_visibility_scope": "ALL"
            }
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
