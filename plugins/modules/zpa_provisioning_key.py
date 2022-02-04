#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: zpa_provisioning_key
short_description: Create a Provisioning Key.
description:
  - This module will create/update/delete a specific Provisioning Key by association type (CONNECTOR_GRP or SERVICE_EDGE_GRP).
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
  app_connector_group_id:
    description: ""
    type: str
    required: False
  app_connector_group_name:
    description: ""
    type: str
    required: False
  creation_time:
    description: ""
    type: str
    required: False
  enabled:
    description: ""
    type: bool
    default: True
    required: False
  expiration_in_epoch_sec:
    description: ""
    type: str
    required: False
  id:
    description: ""
    type: str
    required: False
  ip_acl:
    description: ""
    type: str
    required: False
  max_usage:
    description: ""
    type: str
    required: True
  modified_by:
    description: ""
    type: str
    required: False
  modified_time:
    description: ""
    type: str
    required: False
  name:
    description: ""
    type: str
    required: True
  provisioning_key:
    description: ""
    type: str
    required: False
  enrollment_cert_id:
    description: ""
    type: str
    required: True
  enrollment_cert_name:
    description: ""
    type: str
    required: False
  ui_config:
    description: ""
    type: str
    required: False
  usage_count:
    description: ""
    type: str
    required: False
  zcomponent_id:
    description: ""
    type: str
    required: True
  zcomponent_name:
    description: ""
    type: str
    required: False
  association_type:
    description: ""
    type: str
    choices: ['CONNECTOR_GRP', 'SERVICE_EDGE_GRP']
    required: True
  state:
    description: ""
    type: str
    choices: ['present', 'absent']
    default: present
"""

EXAMPLES = r"""
- name: Get ID Information of a Service Edge Group Enrollment Certificate
  willguibr.zpacloud.zpa_enrollement_certificate_info:
    name: "Service Edge"
  register: enrollment_cert_service_edge

- name: Get ID Information of an Service Edge Group
  willguibr.zpacloud.zpa_service_edge_groups_info:
    name: "Example"
  register: service_edge_group
- name: "Create/Update/Delete App Connector Group Provisioning Key"
  willguibr.zpacloud.zpa_provisioning_key:
    name: "App Connector Group Provisioning Key"
    association_type: "CONNECTOR_GRP"
    max_usage: "10"
    enrollment_cert_id: "{{ enrollment_cert_service_edge.data[0].id }}"
    zcomponent_id: "{{ service_edge_group.data[0].id }}"
"""

RETURN = r"""
# The newly created app connector group or service edge group provisioning key resource record.
"""

from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_provisioning_key import ProvisioningKeyService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper


def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = ProvisioningKeyService(module, customer_id)
    provisioning_key = dict()
    params = [
        "app_connector_group_id",
        "app_connector_group_name",
        "creation_time",
        "enabled",
        "expiration_in_epoch_sec",
        "id",
        "ip_acl",
        "max_usage",
        "modified_by",
        "modified_time",
        "name",
        "provisioning_key",
        "enrollment_cert_id",
        "enrollment_cert_name",
        "ui_config",
        "usage_count",
        "zcomponent_id",
        "zcomponent_name",
        "association_type"
    ]
    association_type = module.params.get("association_type")
    for param_name in params:
        provisioning_key[param_name] = module.params.get(param_name, None)
    existing_key = service.getByIDOrName(
        provisioning_key.get("id"), provisioning_key.get("name"), association_type)
    if existing_key is not None:
        id = existing_key.get("id")
        existing_key.update(provisioning_key)
        existing_key["id"] = id
    if state == "present":
        if existing_key is not None:
            """Update"""
            existing_key = service.update(existing_key, association_type)
            module.exit_json(changed=True, data=existing_key)
        else:
            """Create"""
            provisioning_key = service.create(
                provisioning_key, association_type)
            module.exit_json(changed=False, data=provisioning_key)
    elif state == "absent":
        if existing_key is not None:
            service.delete(existing_key.get("id"), association_type)
            module.exit_json(changed=False, data=existing_key)
    module.exit_json(changed=False, data={})


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        app_connector_group_id=dict(type="str", required=False),
        app_connector_group_name=dict(type="str", required=False),
        creation_time=dict(type="str", required=False),
        enabled=dict(type="bool", default=True, required=False),
        expiration_in_epoch_sec=dict(type="str", required=False),
        id=dict(type="str", required=False),
        ip_acl=dict(type="str", required=False),
        max_usage=dict(type="str", required=True),
        modified_by=dict(type="str", required=False),
        modified_time=dict(type="str", required=False),
        name=dict(type="str", required=True),
        provisioning_key=dict(type="str", required=False, no_log=True,),
        enrollment_cert_id=dict(type="str", required=True),
        enrollment_cert_name=dict(type="str", required=False),
        ui_config=dict(type="str", required=False),
        usage_count=dict(type="str", required=False),
        zcomponent_id=dict(type="str", required=True),
        zcomponent_name=dict(type="str", required=False),
        association_type=dict(type="str", choices=[
                              "CONNECTOR_GRP", "SERVICE_EDGE_GRP"], required=True),
        state=dict(type="str", choices=[
                   "present", "absent"], default="present"),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
