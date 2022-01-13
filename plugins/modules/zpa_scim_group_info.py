#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
      - Name of the scim group.
    required: false
    type: str
  idp_name:
    description:
      - Name of the IDP.
    required: false
    type: str
  id:
    description:
      - ID of the scim group.
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
        idp_name: "SGIO-User-Okta"
      register: department_name
    - name: department_name
      debug:
        msg: "{{ department_name }}"
        
    - name: Gather information about scim attribute by attribute ID
      willguibr.zpacloud_ansible.zpa_scim_attribute_header_info:
        id: 216196257331285827
        idp_name: "SGIO-User-Okta"
      register: attribute_id
    - name: attribute_id
      debug:
        msg: "{{ attribute_id }}"
        
    - name: Gather information about all scim attribute by attributes
      willguibr.zpacloud_ansible.zpa_scim_attribute_header_info:
        idp_name: "SGIO-User-Okta"
      register: scim_attribute_header
    - name: scim_attribute_header
      debug:
        msg: "{{ scim_attribute_header }}"

"""

RETURN = r"""
data:
    description: scim group information
    returned: success
    elements: dict
    type: list
    data: [
  {
                "creation_time": 1631718444,
                "id": 293479,
                "idp_group_id": null,
                "idp_id": 216196257331285825,
                "modified_time": 1639601338,
                "name": "Executives"
            },
            {
                "creation_time": 1631718391,
                "id": 293478,
                "idp_group_id": null,
                "idp_id": 216196257331285825,
                "modified_time": 1639601336,
                "name": "Finance"
            },
            {
                "creation_time": 1631718383,
                "id": 293477,
                "idp_group_id": null,
                "idp_id": 216196257331285825,
                "modified_time": 1639601333,
                "name": "Sales"
            }
    ]
"""


def core(module):
    scim_name = module.params.get("name", None)
    scim_id = module.params.get("id", None)
    idp_name = module.params.get("idp_name", None)
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
        attribute = service.getByName(scim_name, idp_name)
        if attribute is None:
            module.fail_json(
                msg="Failed to retrieve scim group Name: '%s'" % (scim_name))
        attributes = [attribute]
    else:
        attributes = service.getAllByIDPName(idp_name)
    module.exit_json(changed=False, data=attributes)


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=False),
        id=dict(type="str", required=False),
        idp_name=dict(type="str", required=True),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
