#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_customer_version_profile import ProfileVersionService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
author: William Guilherme (@willguibr)
description:
  - Get details (ID and/or Name) of a customer version profile.
module: zpa_customer_version_profile_info
short_description: Get details (ID and/or Name) of a customer version profile.
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 2.0
options:
  name:
    description:
      - Name of the customer version profile.
    required: True
    type: str
  id:
    description:
      - ID of the customer version profile.
    required: false
    type: str
"""

EXAMPLES = """
- name: Gather Information Details of All Customer Version Profiles
  willguibr.zpacloud.zpa_customer_version_profile_info:
  register: all_customer_version_profiles

- debug:
    msg: "{{ all_customer_version_profiles }}"

- name: Gather Information Details of a Cloud Connector Group by Name
  willguibr.zpacloud.zpa_customer_version_profile_info:
    name: "New Release"
  register: version_profile_name

- debug:
    msg: "{{ version_profile_name }}"

- name: Gather Information Details of a Cloud Connector Group by ID
  willguibr.zpacloud.zpa_customer_version_profile_info:
    id: "2"
  register: version_profile_id

- debug:
    msg: "{{ version_profile_id }}"
"""

RETURN = """
# Returns information on a specified Customer Version Profile.
"""

def core(module):
    version_profile = module.params.get("name", None)
    version_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = ProfileVersionService(module, customer_id)
    version_profiles = []
    if version_id is not None:
        version_profile = service.getByID(version_id)
        if version_profile is None:
            module.fail_json(
                msg="Failed to retrieve Customer Version Profile ID: '%s'" % (id))
        version_profiles = [version_profile]
    elif version_profile is not None:
        version_profile = service.getByName(version_profile)
        if version_profile is None:
            module.fail_json(
                msg="Failed to retrieve Customer Version Profile Name: '%s'" % (version_profile))
        version_profiles = [version_profile]
    else:
        version_profiles = service.getAll()
    module.exit_json(changed=False, data=version_profiles)


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
