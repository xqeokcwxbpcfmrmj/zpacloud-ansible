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
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_posture_profile import PostureProfileService
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
author: William Guilherme (@willguibr)
description:
  - Provides details about an (ID and/or Name) of a posture profile resource.
module: zpa_posture_profile_info
short_description: Provides details about an (ID and/or Name) of a posture profile resource.
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
    - name: Gather Details of All Machine Groups
      willguibr.zpacloud.zpa_posture_profile_info:

    - name: Gather Details of a Specific Machine Group by Name
      willguibr.zpacloud.zpa_posture_profile_info:
        name: "Corp_Machine_Group"

    - name: Gather Details of a Specific Machine Group by ID
      willguibr.zpacloud.zpa_posture_profile_info:
        id: "216196257331282583"
"""

RETURN = """
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
    posture_name = module.params.get("name", None)
    posture_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = PostureProfileService(module, customer_id)
    postures = []
    if posture_id is not None:
        posture = service.getByID(posture_id)
        if posture is None:
            module.fail_json(
                msg="Failed to retrieve Posture Profile ID: '%s'" % (id))
        postures = [posture]
    elif posture_name is not None:
        posture = service.getByName(posture_name)
        if posture is None:
            module.fail_json(
                msg="Failed to retrieve Posture Profile Name: '%s'" % (posture_name))
        postures = [posture]
    else:
        postures = service.getAll()
    module.exit_json(changed=False, data=postures)


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
