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
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_provisioning_key import ProvisioningKeyService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = """
---
author: William Guilherme (@willguibr)
description:
  - Provides details about a specific (ID and/or Name) of a Provisioning Key by association type (CONNECTOR_GRP or SERVICE_EDGE_GRP).
module: zpa_provisioning_key_info
short_description: Provides details about a specific (ID and/or Name) of a Provisioning Key by association type (CONNECTOR_GRP or SERVICE_EDGE_GRP).
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the provisioning key.
    required: false
    type: str
  id:
    description:
      - ID of the provisioning key.
    required: false
    type: str
  association_type:
    type: str
    required: True
    description: "Specifies the provisioning key type for App Connectors or ZPA Private Service Edges. The supported values are CONNECTOR_GRP and SERVICE_EDGE_GRP."
"""

EXAMPLES = """
    - name: Gather Details of All CONNECTOR_GRP Provisioning Keys
      willguibr.zpacloud.zpa_provisioning_key_info:
        association_type: "CONNECTOR_GRP"

    - name: Gather Details of All CONNECTOR_GRP Provisioning Keys by Name
      willguibr.zpacloud.zpa_provisioning_key_info:
        name: "Example App Connector Group"
        association_type: "CONNECTOR_GRP"

    - name: Gather Details of All CONNECTOR_GRP Provisioning Keys by ID
      willguibr.zpacloud.zpa_provisioning_key_info:
        id: "8691"
        association_type: "CONNECTOR_GRP"
        
    - name: Gather Details of All SERVICE_EDGE_GRP Provisioning Keys
      willguibr.zpacloud.zpa_provisioning_key_info:
        association_type: "SERVICE_EDGE_GRP"

    - name: Gather Details of All SERVICE_EDGE_GRP Provisioning Keys by Name
      willguibr.zpacloud.zpa_provisioning_key_info:
        name: "Example App Connector Group"
        association_type: "SERVICE_EDGE_GRP"

    - name: Gather Details of All SERVICE_EDGE_GRP Provisioning Keys by ID
      willguibr.zpacloud.zpa_provisioning_key_info:
        id: "8691"
        association_type: "SERVICE_EDGE_GRP"
"""

RETURN = """
data:
    description: Provisioning Key Information
    returned: success
    elements: dict
    type: list
    sample:
        [
          {
            "app_connector_group_id": null,
            "app_connector_group_name": "Canada LSS App Connector Group",
            "creation_time": "1641586556",
            "enabled": true,
            "enrollment_cert_id": "6573",
            "enrollment_cert_name": "Connector",
            "expiration_in_epoch_sec": null,
            "id": "9003",
            "ip_acl": null,
            "max_usage": "10",
            "modified_by": "216196257331282070",
            "modified_time": null,
            "name": "New York Provisioning Key",
            "provisioning_key": "3|api.private.zscaler.com|297XDkU9fv6G/d7s9WS...",
            "ui_config": null,
            "usage_count": "0",
            "zcomponent_id": "216196257331291903",
            "zcomponent_name": "Canada LSS App Connector Group",
          },
          {
            "app_connector_group_id": null,
            "app_connector_group_name": "USA App Connector Group",
            "creation_time": "1639693617",
            "enabled": true,
            "enrollment_cert_id": "6573",
            "enrollment_cert_name": "Connector",
            "expiration_in_epoch_sec": null,
            "id": "8691",
            "ip_acl": null,
            "max_usage": "2",
            "modified_by": "216196257331282070",
            "modified_time": null,
            "name": "USA App Connector Group",
            "provisioning_key": "3|api.private.zscaler.com|Wy3HzPKWJr88i6u...",
            "ui_config": null,
            "usage_count": "0",
            "zcomponent_id": "216196257331291906",
            "zcomponent_name": "USA App Connector Group",
          },
      ]
"""

def core(module):
    provisioning_key_name = module.params.get("name", None)
    provisioning_key_id = module.params.get("id", None)
    association_type = module.params.get("association_type", None)
    customer_id = module.params.get("customer_id", None)
    service = ProvisioningKeyService(module, customer_id)
    provisioning_keys = []
    if provisioning_key_id is not None:
        provisioning_key = service.getByID(
            provisioning_key_id, association_type)
        if provisioning_key is None:
            module.fail_json(
                msg="Failed to retrieve Provisioning Key ID: '%s'" % (id))
        provisioning_keys = [provisioning_key]
    elif provisioning_key_name is not None:
        provisioning_key = service.getByName(
            provisioning_key_name, association_type)
        if provisioning_key is None:
            module.fail_json(
                msg="Failed to retrieve Provisioning Key Name: '%s'" % (provisioning_key_name))
        provisioning_keys = [provisioning_key]
    else:
        provisioning_keys = service.getAll(association_type)
    module.exit_json(changed=False, data=provisioning_keys)


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=False),
        id=dict(type="str", required=False),
        association_type=dict(type="str", choices=[
                              "CONNECTOR_GRP", "SERVICE_EDGE_GRP"], required=True),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
