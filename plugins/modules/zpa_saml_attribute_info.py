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
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_saml_attribute import SamlAttributeService
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = r"""
---
author: William Guilherme (@willguibr)
description:
  - Provides details about a specific saml attributes from a given IDP
module: zpa_saml_attribute_info
short_description: Provides details about a specific saml attributes from a given IDP
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the saml attribute.
    required: false
    type: str
  id:
    description:
      - ID of the saml attribute.
    required: false
    type: str

"""

EXAMPLES = """
- name: saml attribute
  hosts: localhost
  tasks:
    - name: Gather information about saml attribute by attribute Name
      willguibr.zpacloud_ansible.zpa_saml_attribute_info:
        name: DepartmentName_User-Okta
      register: department_name
    - name: department_name
      debug:
        msg: "{{ department_name }}"
        
    - name: Gather information about saml attribute by attribute ID
      willguibr.zpacloud_ansible.zpa_saml_attribute_info:
        id: 216196257331285827
      register: attribute_id
    - name: attribute_id
      debug:
        msg: "{{ attribute_id }}"
        
    - name: Gather information about all saml attribute by attributes
      willguibr.zpacloud_ansible.zpa_saml_attribute_info:
      register: saml_attributes
    - name: saml_attributes
      debug:
        msg: "{{ saml_attributes }}"

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
    saml_attr_name = module.params.get("name", None)
    saml_attr_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = SamlAttributeService(module, customer_id)
    attributes = []
    if saml_attr_id is not None:
        attribute = service.getByID(saml_attr_id)
        if attribute is None:
            module.fail_json(
                msg="Failed to retrieve saml attribute ID: '%s'" % (id))
        attributes = [attribute]
    elif saml_attr_name is not None:
        attribute = service.getByName(saml_attr_name)
        if attribute is None:
            module.fail_json(
                msg="Failed to retrieve saml attribute Name: '%s'" % (saml_attr_name))
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
