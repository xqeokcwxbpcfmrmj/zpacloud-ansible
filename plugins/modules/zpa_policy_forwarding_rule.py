#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_policy_forwarding_rule
short_description: Create a Policy Forwarding Rule.
description:
  - This module will create, update or delete a specific Policy Forwarding Rule
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
  id:
    description: ""
    type: str
  name:
    description: ""
    type: str
    required: True
  description:
    description: ""
    type: str
    required: False
  action:
    description: ""
    type: str
    required: False
    choices: ["INTERCEPT", "INTERCEPT_ACCESSIBLE", "BYPASS"]
    default: INTERCEPT
  action_id:
    description: ""
    type: str
    required: False
  default_rule:
    description: ""
    type: bool
    required: False
  default_rule_name:
    description: ""
    type: str
    required: False
  custom_msg:
    description: ""
    type: str
    required: False
  bypass_default_rule:
    description: ""
    type: bool
    required: False
  operator:
    description: ""
    type: str
    required: False
    choices: ["AND", "OR"]
  policy_type:
    description: ""
    type: str
    required: False
  priority:
    description: ""
    type: str
    required: False
  rule_order:
    description: ""
    type: str
    required: False
  conditions:
    description: ""
    type: list
    elements: dict
    required: False
    suboptions:
      id:
        description: ""
        type: str
      negated:
        description: ""
        type: bool
        required: False
      operator:
        description: ""
        type: str
        required: True
        choices: ["AND", "OR"]
      operands:
        description: ""
        type: list
        elements: dict
        required: False
        suboptions:
          id:
            description: ""
            type: str
          idp_id:
            description: ""
            type: str
            required: False
          name:
            description: ""
            type: str
            required: False
          lhs:
            description: ""
            type: str
            required: True
          rhs:
            description: ""
            type: str
            required: False
          rhs_list:
            description: ""
            type: list
            elements: str
            required: False
          object_type:
            description: ""
            type: str
            required: True
            choices:
              [
                "APP",
                "APP_GROUP",
                "BYPASS",
                "SAML",
                "IDP",
                "CLIENT_TYPE",
                "TRUSTED_NETWORK",
                "MACHINE_GRP",
                "POSTURE",
                "SCIM",
                "SCIM_GROUP",
                "EDGE_CONNECTOR_GROUP",
              ]
  state:
    description: ""
    type: str
    choices: ["present", "absent"]
    default: present
"""

EXAMPLES = """
- name: Policy Forwarding Rule - Example
  willguibr.zpacloud.zpa_policy_forwarding_rule:
    name: "Policy Forwarding Rule - Example"
    description: "Policy Forwarding Rule - Example"
    action: "BYPASS"
    rule_order: 1
    operator: "AND"
    conditions:
      - negated: false
        operator: "OR"
        operands:
          - name: "app_segment"
            object_type: "APP"
            lhs: "id"
            rhs: "216196257331292105"
      - negated: false
        operator: "OR"
        operands:
          - name: "segment_group"
            object_type: "APP_GROUP"
            lhs: "id"
            rhs: "216196257331292103"
      - negated: false
        operator: "OR"
        operands:
          - name: "zpn_client_type_exporter"
            object_type: "CLIENT_TYPE"
            lhs: "id"
            rhs: "zpn_client_type_exporter"
          - name: "zpn_client_type_browser_isolation"
            object_type: "CLIENT_TYPE"
            lhs: "id"
            rhs: "zpn_client_type_browser_isolation"
          - name: "zpn_client_type_zapp"
            object_type: "CLIENT_TYPE"
            lhs: "id"
            rhs: "zpn_client_type_zapp"
      - negated: false
        operator: "OR"
        operands:
          - name: "CrowdStrike_ZPA_ZTA_80"
            object_type: "POSTURE"
            lhs: "{{ postures.data[0].posture_udid }}"
            rhs: "false"
"""

RETURN = """
# The newly created access client forwarding policy rule resource record.
"""

from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_policy_forwarding_rule import PolicyForwardingRuleService
from traceback import format_exc
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native


def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = PolicyForwardingRuleService(module, customer_id)
    global_policy_set = service.getByPolicyType("BYPASS_POLICY")
    if global_policy_set is None or global_policy_set.get("id") is None:
        module.fail_json(msg="Unable to get global policy set")
    policy_set_id = global_policy_set.get("id")
    policy = dict()
    params = [
        "id",
        "name",
        "description",
        "action",
        "action_id",
        "default_rule",
        "default_rule_name",
        "bypass_default_rule",
        "policy_type",
        "policy_set_id",
        "custom_msg",
        "priority",
        "operator",
        "rule_order",
        "conditions",
    ]
    for param_name in params:
        policy[param_name] = module.params.get(param_name, None)
    existing_policy = service.getByIDOrName(
        policy.get("id"), policy.get("name"), policy_set_id, "BYPASS_POLICY")
    if existing_policy is not None:
        id = existing_policy.get("id")
        existing_policy.update(policy)
        existing_policy["id"] = id
    if state == "present":
        if existing_policy is not None:
            """Update"""
            existing_policy = service.update(existing_policy, policy_set_id)
            module.exit_json(changed=True, data=existing_policy)
        else:
            """Create"""
            policy = service.create(policy, policy_set_id)
            module.exit_json(changed=False, data=policy)
    elif state == "absent":
        if existing_policy is not None:
            service.delete(existing_policy.get("id"), policy_set_id)
            module.exit_json(changed=False, data=existing_policy)
    module.exit_json(changed=False, data={})


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        id=dict(type='str'),
        name=dict(type='str', required=True),
        description=dict(type='str', required=False),
        action=dict(type='str', required=False, choices=[
                    "INTERCEPT", "INTERCEPT_ACCESSIBLE", "BYPASS"], default="INTERCEPT"),
        action_id=dict(type='str', required=False),
        default_rule=dict(type='bool', required=False),
        default_rule_name=dict(type='str', required=False),
        custom_msg=dict(type='str', required=False),
        bypass_default_rule=dict(type='bool', required=False),
        operator=dict(type='str', required=False, choices=['AND', 'OR']),
        policy_type=dict(type='str', required=False),
        priority=dict(type='str', required=False),
        rule_order=dict(type='str', required=False),
        conditions=dict(type='list', elements='dict', options=dict(id=dict(type='str'),
                                                                   negated=dict(
                                                                       type='bool', required=False),
                                                                   operator=dict(
                                                                       type='str', required=True, choices=['AND', 'OR']),
                                                                   operands=dict(type='list', elements='dict', options=dict(id=dict(type='str'),
                                                                                                                            idp_id=dict(
                                                                                                                                type='str', required=False),
                                                                                                                            name=dict(
                                                                                                                                type='str', required=False),
                                                                                                                            lhs=dict(
                                                                                                                                type='str', required=True),
                                                                                                                            rhs=dict(
                                                                                                                                type='str', required=False),
                                                                                                                            rhs_list=dict(
                                                                       type='list', elements='str', required=False),
                                                                       object_type=dict(
                                                                           type='str',
                                                                           required=True,
                                                                           choices=['APP', 'APP_GROUP', 'BYPASS', 'SAML',
                                                                                    'IDP', 'CLIENT_TYPE',
                                                                                    'TRUSTED_NETWORK', 'MACHINE_GRP',
                                                                                    'POSTURE', 'SCIM', 'SCIM_GROUP',
                                                                                    'EDGE_CONNECTOR_GROUP']),
                                                                   ), required=False),
                                                                   ), required=False),
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
