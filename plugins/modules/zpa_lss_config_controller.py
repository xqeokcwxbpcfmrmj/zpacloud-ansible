#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: zpa_lss_config_controller
short_description: Create a LSS CONFIG.
description:
  - This module create/update/delete a LSS CONFIG in the ZPA Cloud.
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
    type: str
    description: ""
  policy_rule_resource:
    type: dict
    description: ""
    required: False
    suboptions:
      description:
        description: ""
        type: str
        required: False
      priority:
        description: ""
        type: str
        required: False
      reauth_idle_timeout:
        description: ""
        type: str
        required: False
      policy_type:
        description: ""
        type: str
        required: False
      reauth_default_rule:
        description: ""
        type: bool
        required: False
      custom_msg:
        description: ""
        type: str
        required: False
      action_id:
        description: ""
        type: str
        required: False
      operator:
        description: ""
        type: str
        required: False
      bypass_default_rule:
        description: ""
        type: bool
        required: False
      policy_set_id:
        description: ""
        type: str
        required: False
      default_rule:
        description: ""
        type: bool
        required: False
      action:
        description: ""
        type: str
        required: False
      name:
        description: ""
        type: str
        required: True
      reauth_timeout:
        description: ""
        type: str
        required: False
      rule_order:
        description: ""
        type: str
        required: False
      id:
        description: ""
        type: str
      lss_default_rule:
        description: ""
        type: bool
        required: False
      conditions:
        description: ""
        type: list
        elements: dict
        required: False
        suboptions:
          negated:
            description: ""
            type: bool
            required: False
          operator:
            description: ""
            type: str
            required: True
          operands:
            description: ""
            type: list
            elements: dict
            required: False
            suboptions:
              values:
                description: ""
                type: list
                elements: str
                required: False
              object_type:
                description: ""
                type: str
                required: True
                choices: ["APP", "APP_GROUP", "CLIENT_TYPE"]
  connector_groups:
    type: list
    elements: dict
    required: False
    description: "App Connector Group(s) to be added to the LSS configuration"
    suboptions:
      name:
        required: false
        type: str
        description: ""
      id:
        required: true
        type: str
        description: ""
  config:
    type: dict
    required: False
    description: ""
    suboptions:
      format:
        description: ""
        type: str
        required: True
      id:
        description: ""
        type: str
      name:
        description: ""
        type: str
        required: True
      lss_port:
        description: ""
        type: str
        required: True
      use_tls:
        description: ""
        type: bool
        required: False
        default: False
      enabled:
        description: ""
        type: bool
        required: False
        default: True
      description:
        description: ""
        type: str
        required: False
      filter:
        description: ""
        type: list
        elements: str
        required: False
      lss_host:
        description: ""
        type: str
        required: True
      source_log_type:
        description: ""
        type: str
        required: True
        choices:
          - "zpn_trans_log"
          - "zpn_auth_log"
          - "zpn_ast_auth_log"
          - "zpn_http_trans_log"
          - "zpn_audit_log"
          - "zpn_sys_auth_log"
          - "zpn_http_insp"
          - "zpn_ast_comprehensive_stats"
      audit_message:
        description: ""
        type: str
        required: False
  state:
    description: "Whether the config should be present or absent."
    type: str
    choices:
      - present
      - absent
    default: present

"""
EXAMPLES = r'''
- name: LSS Controller
  hosts: localhost
  tasks:
    - name: Create a LSS Controller
      willguibr.zpacloud.zpa_lss_config_controller:
        state: present
        config:
          name: Status
          description: status
          enabled: true
          lss_host: 10.1.1.1
          lss_port: 20000
          format: "..."
          source_log_type: "zpn_ast_auth_log"
        connector_groups:
          - id: "11111"
            name: "Test"
      register: lss_controller
    - name: lss_controller
      debug:
        msg: "{{ lss_controller }}"
'''

RETURN = r'''
'''
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_lss_config_controller import LSSConfigControllerService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper


def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = LSSConfigControllerService(module, customer_id)
    lss_config = dict()
    params = [
        "id",
        "config",
        "connector_groups",
        "policy_rule_resource"
    ]
    for param_name in params:
        lss_config[param_name] = module.params.get(param_name, None)
    existing_lss_config = service.getByIDOrName(
        lss_config.get("id"), lss_config.get("config", {}).get("name"))
    if existing_lss_config is not None:
        id = existing_lss_config.get("id")
        existing_lss_config.update(lss_config)
        existing_lss_config["id"] = id
    if state == "present":
        if existing_lss_config is not None:
            """Update"""
            lss_config = service.update(existing_lss_config)
            module.exit_json(changed=True, data=lss_config)
        else:
            """Create"""
            lss_config = service.create(lss_config)
            module.exit_json(changed=False, data=lss_config)
    elif state == "absent":
        if existing_lss_config is not None:
            service.delete(existing_lss_config.get("id"))
            module.exit_json(changed=False, data=existing_lss_config)
    module.exit_json(changed=False, data={})


def main():
    """Main"""
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    id_name_spec = dict(type='list', elements='dict', options=dict(id=dict(
        type='str', required=True), name=dict(type='str', required=False)), required=False)
    argument_spec.update(
        id=dict(type='str'),
        policy_rule_resource=dict(
            type='dict',
            options=dict(
                priority=dict(
                    type='str', required=False
                ),
                reauth_idle_timeout=dict(
                    type='str', required=False
                ),
                policy_type=dict(
                    type='str', required=False
                ),
                reauth_default_rule=dict(
                    type='bool', required=False
                ),
                custom_msg=dict(
                    type='str', required=False
                ),
                action_id=dict(
                    type='str', required=False
                ),
                operator=dict(
                    type='str', required=False
                ),
                bypass_default_rule=dict(
                    type='bool', required=False
                ),
                policy_set_id=dict(
                    type='str', required=False
                ),
                default_rule=dict(
                    type='bool', required=False
                ),
                action=dict(
                    type='str', required=False
                ),
                conditions=dict(
                    type='list',
                    elements='dict',
                    options=dict(
                        negated=dict(type='bool', required=False),
                        operator=dict(type='str', required=True),
                        operands=dict(
                            type='list',
                            elements='dict',
                            options=dict(
                                values=dict(
                                    type='list', elements='str', required=False
                                ),
                                object_type=dict(
                                    type='str', required=True, choices=["APP", "APP_GROUP", "CLIENT_TYPE"]
                                ),
                            ),
                            required=False
                        ),
                    ), required=False),
                name=dict(type='str', required=True),
                reauth_timeout=dict(type='str', required=False),
                rule_order=dict(type='str', required=False),
                description=dict(type='str', required=False),
                id=dict(type='str'),
                lss_default_rule=dict(type='bool', required=False),
            ),
            required=False
        ),
        connector_groups=id_name_spec,
        config=dict(
            type='dict',
            options=dict(
                format=dict(type='str', required=True),
                id=dict(type='str'),
                name=dict(type='str', required=True),
                lss_port=dict(type='str', required=True),
                use_tls=dict(type='bool', required=False, default=False),
                enabled=dict(type='bool', required=False, default=True),
                description=dict(type='str', required=False),
                filter=dict(type='list', elements='str', required=False),
                lss_host=dict(type='str', required=True),
                source_log_type=dict(type='str', required=True, choices=["zpn_trans_log", "zpn_auth_log", "zpn_ast_auth_log",
                                     "zpn_http_trans_log", "zpn_audit_log", "zpn_sys_auth_log", "zpn_http_insp", "zpn_ast_comprehensive_stats", ]),
                audit_message=dict(type='str', required=False),
            ),
            required=False
        ),
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
