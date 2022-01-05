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
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_scim_group import ScimGroupService
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = r"""
---
author: William Guilherme (@willguibr)
description:
  - Provides details about a specific scim attributes from a given IDP
module: zpa_scim_attribute_header_info
short_description: Provides details about a specific scim attributes from a given IDP
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the scim attribute.
    required: false
    type: str
  id:
    description:
      - ID of the scim attribute.
    required: false
    type: str

"""

EXAMPLES = """
- name: scim attribute
  hosts: localhost
  tasks:
    - name: Gather information about scim attribute by attribute Name
      willguibr.zpacloud_ansible.zpa_scim_attribute_header_info:
        name: DepartmentName_User-Okta
      register: department_name
    - name: department_name
      debug:
        msg: "{{ department_name }}"
        
    - name: Gather information about scim attribute by attribute ID
      willguibr.zpacloud_ansible.zpa_scim_attribute_header_info:
        id: 216196257331285827
      register: attribute_id
    - name: attribute_id
      debug:
        msg: "{{ attribute_id }}"
        
    - name: Gather information about all scim attribute by attributes
      willguibr.zpacloud_ansible.zpa_scim_attribute_header_info:
      register: scim_attribute_header
    - name: scim_attribute_header
      debug:
        msg: "{{ scim_attribute_header }}"

"""

RETURN = r"""
data:
    description: saml attribute information
    returned: success
    elements: dict
    type: list
    data: [
            {
              "creation_time": "1631718008",
              "id": "216196257331285827",
              "idp_id": "216196257331285825",
              "idp_name": "User-Okta",
              "modified_by": "216196257331281958",
              "modified_time": null,
              "name": "DepartmentName-User-Okta",
              "saml_name": "DepartmentName",
              "user_attribute": false
            },
    ]
"""


def core(module):
    scim_name = module.params.get("name", None)
    scim_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = ScimGroupService(module, customer_id)
    attributes = []
    if scim_id is not None:
        attribute = service.getByID(scim_id)
        if attribute is None:
            module.fail_json(
                msg="Failed to retrieve scim group ID: '%s'" % (id))
        attributes = [attribute]
    elif scim_name is not None:
        attribute = service.getByName(scim_name)
        if attribute is None:
            module.fail_json(
                msg="Failed to retrieve scim group Name: '%s'" % (scim_name))
        attributes = [attribute]
    else:
        attributes = service.getAll()
    module.exit_json(changed=False, data=attributes)


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
