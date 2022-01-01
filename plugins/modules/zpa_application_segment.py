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
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc
from ansible_collections.willguibr.zpa.plugins.module_utils.application_segment import ApplicationSegmentService
from ansible_collections.willguibr.zpa.plugins.module_utils.zpa_client import ZPAClientHelper
__metaclass__ = type

DOCUMENTATION = r"""
---
module: zpa_application_segment
short_description: Create an application segment
description:
  - This module will create, retrieve, update or delete a specific application segment
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  creation_time:
    type: str
    required: False
  modified_time:
    type: str
    required: False
  default_max_age:
    type: str
    required: False
    default: ""
  ip_anchored:
    type: bool
    required: False
  udp_port_range:
    type: list
    elements: dict
    required: False
    description:
      - udp port range
  id:
    type: str
  double_encrypt:
    type: bool
    required: False
    description:
      - Whether Double Encryption is enabled or disabled for the app.
  icmp_access_type:
    type: str
    required: False
    default: "NONE"
    choices: ["PING_TRACEROUTING", "PING", "NONE"]
  default_idle_timeout:
    type: str
    required: False
    default: ""
  modifiedby:
    type: str
    required: False
  passive_health_enabled:
    type: bool
    required: False
  bypass_type:
    type: str
    required: False
    description:
      - Indicates whether users can bypass ZPA to access applications.
    choices: ["ALWAYS", "NEVER", "ON_NET"]
  is_cname_enabled:
    type: bool
    required: False
    description:
      - Indicates if the Zscaler Client Connector (formerly Zscaler App or Z App) receives CNAME DNS records from the connectors.
  name:
    type: str
    required: True
    description:
      - Name of the application.
  config_space:
    type: str
    required: False
    default: "DEFAULT"
    choices: ["DEFAULT", "SIEM"]
  health_reporting:
    type: str
    required: False
    description:
      - Whether health reporting for the app is Continuous or On Access. Supported values: NONE, ON_ACCESS, CONTINUOUS.
    default: "NONE"
    choices: ["NONE", "ON_ACCESS", "CONTINUOUS"]
  log_features:
    type: str
    required: False
    choices: ["skip_discovery", "full_wildcard"]
  server_groups:
    type: list
    elements: str
    required: True
    description:
      - List of the server group IDs.
  segment_group_id:
    type: str
    required: True
  description:
    type: str
    required: False
    description:
      - Description of the application.
  health_check_type:
    type: str
  segment_group_name:
    type: str
    required: False
  tcp_port_range:
    type: list
    elements: dict
    required: False
    description:
      - tcp port range
  udp_port_ranges:
    type: list
    elements: str
    required: False
    description:
      - UDP port ranges used to access the app.
  tcp_port_ranges:
    type: list
    elements: str
    required: False
    description:
      - TCP port ranges used to access the app.
  enabled:
    type: bool
    required: False
    description:
      - Whether this application is enabled or not.
  domain_names:
    type: list
    elements: str
    required: True
    description:
      - List of domains and IPs.

"""


EXAMPLES = '''
- name: App segment
  hosts: localhost
  tasks:
    - name: Create an app segment
      willguibr.zpa.zpa_application_segment:
        state: absent
        name: Example Application
        description: Example Application Test
        enabled: true
        health_reporting: ON_ACCESS
        bypass_type: NEVER
        is_cname_enabled: true
        tcp_port_range:
          - from: "80"
            to: "80"
        domain_names:
          - crm.example.com
        segment_group_id: "216196257331291896"
        server_groups:
          #- "216196257331291969"
      register: app_segment
    - name: created/updated app segment
      debug:
        msg: "{{ app_segment }}"
'''
RETURN = r"""
"""


def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = ApplicationSegmentService(module, customer_id)
    app = dict()
    params = [
        "tcp_port_range",
        "enabled",
        "default_idle_timeout",
        "log_features",
        "bypass_type",
        "udp_port_range",
        "config_space",
        "health_reporting",
        "segment_group_id",
        "double_encrypt",
        "health_check_type",
        "default_max_age",
        "is_cname_enabled",
        "passive_health_enabled",
        "ip_anchored",
        "name",
        "description",
        "icmp_access_type",
        "creation_time",
        "modifiedby",
        "modified_time",
        "id",
        "server_groups",
        "segment_group_name",
        "domain_names",
    ]
    for param_name in params:
        app[param_name] = module.params.get(param_name)
    existing_app = service.getByIDOrName(app.get("id"), app.get("name"))
    if existing_app is not None:
        id = existing_app.get("id")
        existing_app.update(app)
        existing_app["id"] = id
    if state == "present":
        if existing_app is not None:
            """Update"""
            service.update(existing_app)
            module.exit_json(changed=True, data=existing_app)
        else:
            """Create"""
            app = service.create(app)
            module.exit_json(changed=False, data=app)
    elif state == "absent":
        if existing_app is not None:
            # first detach it from the segment group
            service.detach_from_segment_group(existing_app.get(
                "id"), existing_app.get("segment_group_id"))
            service.delete(existing_app.get("id"))
            module.exit_json(changed=False, data=existing_app)
    module.exit_json(changed=False, data={})


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    port_spec = dict(to=dict(type='str', required=False))
    port_spec["from"] = dict(type='str', required=False)
    argument_spec.update(
        tcp_port_range=dict(type='list', elements='dict',
                            options=port_spec, required=False),
        enabled=dict(type='bool', required=False),
        default_idle_timeout=dict(type='str', required=False, default=""),
        log_features=dict(type='str', required=False),
        bypass_type=dict(type='str', required=False),
        udp_port_range=dict(type='list', elements='dict',
                            options=port_spec, required=False),
        config_space=dict(type='str', required=False,
                          default="DEFAULT", choices=["DEFAULT", "SIEM"]),
        health_reporting=dict(type='str', required=False,
                              default="NONE", choices=["NONE", "ON_ACCESS", "CONTINUOUS"]),
        segment_group_id=dict(type='str', required=True),
        double_encrypt=dict(type='bool', required=False),
        health_check_type=dict(type='str'),
        default_max_age=dict(type='str', required=False, default=""),
        is_cname_enabled=dict(type='bool', required=False),
        passive_health_enabled=dict(type='bool', required=False),
        ip_anchored=dict(type='bool', required=False),
        name=dict(type='str', required=True),
        description=dict(type='str', required=False),
        icmp_access_type=dict(type='str', required=False,
                              default="NONE", choices=["PING_TRACEROUTING", "PING", "NONE"]),
        creation_time=dict(type='str', required=False),
        modifiedby=dict(type='str', required=False),
        modified_time=dict(type='str', required=False),
        id=dict(type='str'),
        server_groups=dict(type='list', elements='str', required=True),
        segment_group_name=dict(type='str', required=False),
        domain_names=dict(type='list', elements='str', required=True),
        state=dict(type="str", choices=[
                   "present", "absent"], default="present")
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
