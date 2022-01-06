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
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_provisioning_key import ProvisioningKeyService
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = r"""
---
author: William Guilherme (@willguibr)
description:
  - Provides details about a specific posture profile created in the Zscaler Private Access Mobile Portal
module: zpa_posture_profile_info
short_description: Provides details about a specific posture profile created in the Zscaler Private Access Mobile Portal
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the posture profile.
    required: false
    type: str
  id:
    description:
      - ID of the posture profile.
    required: false
    type: str

"""

EXAMPLES = """
- name: posture profile
  hosts: localhost
  tasks:
    - name: Gather information about all posture profile
      willguibr.zpacloud_ansible.zpa_posture_profile_info:
        #name: CrowdStrike_ZPA_Pre-ZTA
        id: 216196257331282234
      register: postures
    - name: postures
      debug:
        msg: "{{ postures }}"

"""

RETURN = r"""
data:
    description: Posture Profile information
    returned: success
    elements: dict
    type: list
    sample: [
      {
        "creation_time": "1638237193",
        "domain": null,
        "id": "216196257331291092",
        "master_customer_id": null,
        "modified_by": "72057594037928115",
        "modified_time": "1638237193",
        "name": "Microsoft Windows Defender",
        "posture_udid": "e7ac7e3f-2098-42fc-a659-030bdca2c4a7",
        "zscaler_cloud": "zscalerthree",
        "zscaler_customer_id": null
      }
    ]
"""


def core(module):
    provisioning_key_name = module.params.get("name", None)
    provisioning_key_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = ProvisioningKeyService(module, customer_id)
    provisioning_keys = []
    if provisioning_key_id is not None:
        provisioning_key = service.getByID(provisioning_key_id)
        if provisioning_key is None:
            module.fail_json(
                msg="Failed to retrieve Provisioning Key ID: '%s'" % (id))
        provisioning_keys = [provisioning_key]
    elif provisioning_key_name is not None:
        provisioning_key = service.getByName(provisioning_key_name)
        if provisioning_key is None:
            module.fail_json(
                msg="Failed to retrieve Provisioning Key Name: '%s'" % (provisioning_key_name))
        provisioning_keys = [provisioning_key]
    else:
        postures = service.getAll()
    module.exit_json(changed=False, data=provisioning_keys)


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
