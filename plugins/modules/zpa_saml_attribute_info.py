#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_saml_attribute import SamlAttributeService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
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

    - name: Gather information about all saml attribute by attributes
      willguibr.zpacloud.zpa_saml_attribute_info:
      
    - name: Gather information about saml attribute by attribute Name
      willguibr.zpacloud.zpa_saml_attribute_info:
        name: DepartmentName_User-Okta
      register: department_name
    - name: department_name
      debug:
        msg: "{{ department_name }}"
        
    - name: Gather information about saml attribute by attribute ID
      willguibr.zpacloud.zpa_saml_attribute_info:
        id: 216196257331285827
      register: attribute_id
    - name: attribute_id
      debug:
        msg: "{{ attribute_id }}"
        
    - name: Gather information about all saml attribute by attributes
      willguibr.zpacloud.zpa_saml_attribute_info:
      register: saml_attributes
    - name: saml_attributes
      debug:
        msg: "{{ saml_attributes }}"

"""

RETURN = """
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
