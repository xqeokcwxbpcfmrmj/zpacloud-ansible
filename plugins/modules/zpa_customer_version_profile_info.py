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
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_customer_version_profile import ProfileVersionService
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = r"""
---
author: William Guilherme (@willguibr)
description:
  - Retrieves details of a customer version profile in the Zscaler Private Access portal.
module: zpa_customer_version_profile_info
short_description: Retrieves details of a customer version profile in the Zscaler Private Access portal.
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 2.0
options:
  name:
    description:
      - Name of the customer version profile.
    required: false
    type: str
  id:
    description:
      - ID of the customer version profile.
    required: false
    type: str

"""

EXAMPLES = """
- name: customer version profile
  hosts: localhost
  tasks:
    - name: Gather information about all customer version profile
      willguibr.zpacloud_ansible.zpa_customer_version_profile_info:
        name: Default
      register: version_profile
    - name: version_profile
      debug:
        msg: "{{ version_profile }}"
"""

"""
- name: customer version profile
  hosts: localhost
  tasks:
    - name: Gather information about all customer version profile
      willguibr.zpacloud_ansible.zpa_customer_version_profile_info:
        name: Previous Default
      register: version_profile
    - name: version_profile
      debug:
        msg: "{{ version_profile }}"
"""


"""
- name: customer version profile
  hosts: localhost
  tasks:
    - name: Gather information about all customer version profile
      willguibr.zpacloud_ansible.zpa_customer_version_profile_info:
        name: New Release
      register: version_profile
    - name: version_profile
      debug:
        msg: "{{ version_profile }}"
"""

RETURN = r"""
data:
    description: Customer Profile New Release
    returned: success
    elements: dict
    type: list
    sample: [
    {
        "creation_time": "1475127781",
        "custome_id": "72057594037927936",
        "description": null,
        "id": "0",
        "modified_by": "72057594037928193",
        "modified_time": "1634285282",
        "name": "Default",
        "upgrade_priority": "WEEK",
        "visibility_scope": "ALL"
    },
    {
        "creation_time": "1631577657",
        "custome_id": "72057594037927936",
        "description": null,
        "id": "1",
        "modified_by": "72057594037928193",
        "modified_time": "1634285256",
        "name": "Previous Default",
        "upgrade_priority": "DAY",
        "visibility_scope": "ALL"
    },
    {
        "creation_time": "1631577657",
        "custome_id": "72057594037927936",
        "description": null,
        "id": "2",
        "modified_by": "72057594037928193",
        "modified_time": "1633764547",
        "name": "New Release",
        "upgrade_priority": "DAY",
        "visibility_scope": "ALL"
    }
    ]
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
