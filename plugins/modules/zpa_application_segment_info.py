#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_application_segment import ApplicationSegmentService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_application_segment_info
short_description: "Gather details of all or specific Application Segments"
description: "This module can be used to gather information about all or specific application segment."
author: "William Guilherme (@willguibr)"
version_added: "1.0.0"
options:
  name:
    description: "Name of the application segment."
    required: True
    type: str
  id:
    description: "ID of the application segment."
    required: False
    type: str
"""

EXAMPLES = """"
- name: Gather Details of All Application Segments
  willguibr.zpacloud.zpa_application_segment_info:
  register: all_app_segments

- debug:
    msg: "{{ all_app_segments }}"

- name: Gather Details of a Specific Application Segments by Name
  willguibr.zpacloud.zpa_application_segment_info:
    name: "Example Application Segment"
  register: app_segment_name
  
- debug:
    msg: "{{ app_segment_name }}"

- name: Gather Details of a Specific Application Segments by ID
  willguibr.zpacloud.zpa_application_segment_info:
    id: "216196257331291981"
  register: app_segment_id
  
- debug:
    msg: "{{ app_segment_id }}"
"""

RETURN = """
# Default return values
"""


def core(module):
    app_name = module.params.get("name", None)
    app_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = ApplicationSegmentService(module, customer_id)
    apps = []
    if app_id is not None:
        app = service.getByID(app_id)
        if app is None:
            module.fail_json(
                msg="Failed to retrieve application segment ID: '%s'" % (id))
        apps = [app]
    elif app_name is not None:
        app = service.getByName(app_name)
        if app is None:
            module.fail_json(
                msg="Failed to retrieve application segment Name: '%s'" % (app_name))
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
