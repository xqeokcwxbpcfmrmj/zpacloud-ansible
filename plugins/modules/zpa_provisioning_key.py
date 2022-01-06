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
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_provisioning_key import ProvisioningKeyService
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import ZPAClientHelper
__metaclass__ = type

DOCUMENTATION = r"""
---
module: zpa_app_connector_groups
short_description: Create/ an app connector group
description:
  - This module will create, retrieve, update or delete a specific app connector group
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  name:
    description: "Name of the App Connector Group."
    required: True
    type: str
  id:
    description: "ID of the App Connector Group."
    type: str
  city_country:
    description: "City Country of the App Connector Group."
    type: str
  country_code:
    description: "Country code of the App Connector Group."
    type: str
  description:
    description: "Description of the App Connector Group."
    type: str
  dns_query_type:
    description: "Whether to enable IPv4 or IPv6, or both, for DNS resolution of all applications in the App Connector Group."
    default: IPV4_IPV6
    choices: ["IPV4_IPV6", "IPV4", "IPV6"]
    type: str
  enabled:
    description: "Whether this App Connector Group is enabled or not."
    required: False
    default: True
    type: bool
  latitude:
    description: "Latitude of the App Connector Group. Integer or decimal. With values in the range of -90 to 90."
    type: str
  location:
    description: "Location of the App Connector Group."
    type: str
  longitude:
    description: "Longitude of the App Connector Group. Integer or decimal. With values in the range of -180 to 180."
    type: str
  lss_app_connector_group:
    description: "LSS app connector group."
    required: False
    type: bool
  upgrade_day:
    description: "App Connectors in this group will attempt to update to a newer version of the software during this specified day. List of valid days (i.e., Sunday, Monday)."
    default: SUNDAY
    type: str
  upgrade_time_in_secs:
    description: "App Connectors in this group will attempt to update to a newer version of the software during this specified time. Integer in seconds (i.e., -66600). The integer should be greater than or equal to 0 and less than 86400, in 15 minute intervals."
    default: 66600
    type: str
  override_version_profile:
    description: "Whether the default version profile of the App Connector Group is applied or overridden. Supported values: true, false."
    required: False
    default: False
    type: bool
  version_profile_id:
    description: "ID of the version profile. To learn more, see Version Profile Use Cases. This value is required, if the value for overrideVersionProfile is set to true."
    default: 0
    choices: ["0", "1", "2"]
    type: str
  version_profile_name:
    description: "Name of the version profile."
    type: str
  state:
    description: "Whether the app connector group should be present or absent."
    default: present
    choices: ["present", "absent"]
    type: str
"""

EXAMPLES = '''
- name: App Connector Groups
  hosts: localhost
  tasks:
    - name: Create/update/delete an app connector group
      willguibr.zpacloud_ansible.zpa_app_connector_groups:
        state: "absent"
        #id: "216196257331292046"
        name: "Example"
        description: "Example2"
        enabled: true
        city_country: "California, US"
        country_code: "US"
        latitude: "37.3382082"
        longitude: "-121.8863286"
        location: "San Jose, CA, USA"
        upgrade_day: "SUNDAY"
        upgrade_time_in_secs: "66600"
        override_version_profile: true
        version_profile_id: "0"
        dns_query_type: "IPV4"
      register: appconnectorg
    - name: created appconnector group
      debug:
        msg: "{{ appconnectorg }}"

'''

RETURN = r"""
data:
    description: App Connector Group
    returned: success
    type: dict
    sample: [
        {
          id                      = "82827282828",
          name                    = "Example",
          description             = "Example",
          enabled                 = true,
          city_country            = "California, US",
          country_code            = "US",
          latitude                = "37.3382082",
          longitude               = "-121.8863286",
          location                = "San Jose, CA, USA",
          upgrade_day             = "SUNDAY",
          upgrade_time_in_secs    = "66600",
          override_version_profile= true,
          version_profile_id      = 0,
          dns_query_type          = "IPV4"
        },
    ]
"""


def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = ProvisioningKeyService(module, customer_id)
    provisioning_key = dict()
    params = [
        "app_connector_group_id",
        "app_connector_group_name",
        "creation_time",
        "enabled",
        "expiration_in_epoch_sec",
        "id",
        "ip_acl",
        "max_usage",
        "modified_by",
        "modified_time",
        "name",
        "provisioning_key",
        "enrollment_cert_id",
        "enrollment_cert_name",
        "ui_config",
        "usage_count",
        "zcomponent_id",
        "zcomponent_name",
    ]
    for param_name in params:
        provisioning_key[param_name] = module.params.get(param_name, None)
    existing_key = service.getByIDOrName(provisioning_key.get("id"), provisioning_key.get("name"))
    if existing_key is not None:
        id = existing_key.get("id")
        existing_key.update(provisioning_key)
        existing_key["id"] = id
    if state == "present":
        if existing_key is not None:
            """Update"""
            service.update(existing_key)
            module.exit_json(changed=True, data=existing_key)
        else:
            """Create"""
            provisioning_key = service.create(provisioning_key)
            module.exit_json(changed=False, data=provisioning_key)
    elif state == "absent":
        if existing_key is not None:
            service.delete(existing_key.get("id"))
            module.exit_json(changed=False, data=existing_key)
    module.exit_json(changed=False, data={})


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        app_connector_group_id=dict(type="str", required=False),
        app_connector_group_name=dict(type="str", required=False),
        creation_time=dict(type="str", required=False),
        enabled=dict(type="bool", default=True, required=False),
        expiration_in_epoch_sec=dict(type="str", required=False),
        id=dict(type="str", required=False),
        ip_acl=dict(type="str", required=False),
        max_usage=dict(type="str", required=False),
        modified_by=dict(type="str", required=False),
        modified_time=dict(type="str", required=False),
        name=dict(type="str", required=True),
        provisioning_key=dict(type="str", required=False),
        enrollment_cert_id=dict(type="str", required=False),
        enrollment_cert_name=dict(type="str", required=False),
        ui_config=dict(type="str", required=False),
        usage_count=dict(type="str", required=False),
        zcomponent_id=dict(type="str", required=False),
        zcomponent_name=dict(type="str", required=False),
        state=dict(type="str", choices=[
                   "present", "absent"], default="present"),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
