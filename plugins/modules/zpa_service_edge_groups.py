#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_service_edge_groups
short_description: Create a Service Edge Group.
description:
  - This module create/update/delete a Service Edge Group resource in the ZPA Cloud.
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  client_id:
    description: ""
    required: false
    type: str
  client_secret:
    description: ""
    required: false
    type: str
  customer_id:
    description: ""
    required: false
    type: str
  city_country:
    description: ""
    type: str
    required: False
  country_code:
    description: ""
    type: str
    required: False
  description:
    description: ""
    type: str
    required: False
  enabled:
    description: ""
    type: bool
    default: True
    required: False
  geolocation_id:
    description: ""
    type: str
    required: False
  id:
    description: ""
    type: str
    required: False
  is_public:
    description: ""
    type: str
    required: False
  latitude:
    description: ""
    type: str
    required: False
  location:
    description: ""
    type: str
    required: False
  longitude:
    description: ""
    type: str
    required: False
  name:
    description: ""
    type: str
    required: True
  override_version_profile:
    description: ""
    type: bool
    default: False
    required: False
  upgrade_day:
    description: ""
    type: str
    default: SUNDAY
    required: False
  upgrade_time_in_secs:
    description: ""
    type: str
    default: 66600
    required: False
  version_profile_id:
    description: ""
    type: str
    required: False
  version_profile_name:
    description: ""
    type: str
    required: False
  version_profile_visibility_scope:
    description: ""
    type: str
    default: NONE
    choices: ['ALL', 'NONE', 'CUSTOM']
    required: False
  service_edges:
    description: ""
    type: list
    elements: dict
    required: False
    suboptions:
      id:
        description: ""
        type: str
        required: False
      name:
        description: ""
        type: str
        required: False
  trusted_networks:
    description: ""
    type: list
    elements: dict
    required: False
    suboptions:
      id:
        description: ""
        type: str
        required: False
      name:
        description: ""
        type: str
        required: False
  state:
    description: ""
    type: str
    choices: ['present', 'absent']
    default: present
"""

EXAMPLES = """
- name: Create/Update/Delete a Service Edge Group
  willguibr.zpacloud.zpa_service_edge_groups:
    name: "Example"
    description: "Example2"
    enabled: true
    city_country: "California, US"
    country_code: "US"
    latitude: "37.3382082"
    longitude: "-121.8863286"
    location: "San Jose, CA, USA"
    upgrade_day: "SUNDAY"
    upgrade_time_in_secs: "66600"
    override_version_profile: true
    version_profile_id: "0"
    dns_query_type: "IPV4"
"""

RETURN = """
# The newly created service edge group resource record.
"""

from traceback import format_exc

from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper,
)
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_service_edge_groups import (
    ServiceEdgeGroupService,
)


def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = ServiceEdgeGroupService(module, customer_id)
    service_edge = dict()
    params = [
        "city_country",
        "country_code",
        "description",
        "enabled",
        "gelocation_id",
        "id",
        "is_public",
        "latitude",
        "location",
        "longitude",
        "name",
        "override_version_profile",
        "upgrade_day",
        "upgrade_time_in_secs",
        "version_profile_id",
        "version_profile_name",
        "version_profile_visibility_scope",
    ]
    for param_name in params:
        service_edge[param_name] = module.params.get(param_name, None)
    existing_edge = service.getByIDOrName(
        service_edge.get("id"), service_edge.get("name")
    )
    if existing_edge is not None:
        id = existing_edge.get("id")
        existing_edge.update(service_edge)
        existing_edge["id"] = id
    if state == "present":
        if existing_edge is not None:
            """Update"""
            service.update(existing_edge)
            module.exit_json(changed=True, data=existing_edge)
        else:
            """Create"""
            service_edge = service.create(service_edge)
            module.exit_json(changed=False, data=service_edge)
    elif state == "absent":
        if existing_edge is not None:
            service.delete(existing_edge.get("id"))
            module.exit_json(changed=False, data=existing_edge)
    module.exit_json(changed=False, data={})


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    id_name_spec = dict(
        type="list",
        elements="dict",
        options=dict(
            id=dict(type="str", required=False), name=dict(type="str", required=False)
        ),
        required=False,
    )
    argument_spec.update(
        city_country=dict(type="str", required=False),
        country_code=dict(type="str", required=False),
        description=dict(type="str", required=False),
        enabled=dict(type="bool", default=True, required=False),
        geolocation_id=dict(type="str", required=False),
        id=dict(type="str", required=False),
        is_public=dict(type="str", required=False),
        latitude=dict(type="str", required=False),
        location=dict(type="str", required=False),
        longitude=dict(type="str", required=False),
        name=dict(type="str", required=True),
        override_version_profile=dict(type="bool", default=False, required=False),
        upgrade_day=dict(type="str", default="SUNDAY", required=False),
        upgrade_time_in_secs=dict(type="str", default=66600, required=False),
        version_profile_id=dict(type="str", required=False),
        version_profile_name=dict(type="str", required=False),
        version_profile_visibility_scope=dict(
            type="str",
            default="NONE",
            choices=["ALL", "NONE", "CUSTOM"],
            required=False,
        ),
        service_edges=id_name_spec,
        trusted_networks=id_name_spec,
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
