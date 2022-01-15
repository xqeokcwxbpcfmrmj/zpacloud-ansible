#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc
<<<<<<< HEAD
<<<<<<< HEAD
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_app_connector_group import AppConnectorGroupService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
=======
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_app_connector_group import AppConnectorGroupService
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import ZPAClientHelper
>>>>>>> master
=======
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_app_connector_group import AppConnectorGroupService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
>>>>>>> master

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_app_connector_groups
short_description: Create/Update/Delete an App Connector Group.
description:
  - This module will Create/Update/Delete an App Connector Group.
author:
  - William Guilherme (@willguibr)
version_added: "1.0.0"
options:
  name:
    description: "Name of the App Connector Group."
    required: True
    type: str
  description:
    description: "Description of the App Connector Group."
    required: False
    type: str
  id:
    description: "ID of the App Connector Group."
    required: False
    type: str
  city_country:
    description: "City Country of the App Connector Group."
    required: True
    type: str
  country_code:
    description: "Country code of the App Connector Group."
    required: True
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
    required: True
    type: str
  location:
    description: "Location of the App Connector Group."
    required: True
    type: str
  longitude:
    description: "Longitude of the App Connector Group. Integer or decimal. With values in the range of -180 to 180."
    required: True
    type: str
  lss_app_connector_group:
    description: "LSS app connector group."
    required: False
    type: bool
  upgrade_day:
    description: "App Connectors in this group will attempt to update to a newer version of the software during this specified day. List of valid days (i.e., Sunday, Monday)."
    required: False
    default: SUNDAY
   type: str
  upgrade_time_in_secs:
    description: "App Connectors in this group will attempt to update to a newer version of the software during this specified time. Integer in seconds (i.e., -66600). The integer should be greater than or equal to 0 and less than 86400, in 15 minute intervals."
    default: 66600
    required: False
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
    required: False
    type: str
  version_profile_name:
    description: "Name of the version profile."
    required: False
    type: str
  state:
    description: "Whether the app connector group should be present or absent."
    required: False
    default: present
    choices: ["present", "absent"]
    type: str
"""

EXAMPLES = """
- name: Create/update/delete an app connector group
  willguibr.zpacloud.zpa_app_connector_groups:
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
"""

RETURN = """
# The newly created app connector group resource record.
"""


def core(module):
    state = module.params.get("state", None)
    customer_id = module.params.get("customer_id", None)
    service = AppConnectorGroupService(module, customer_id)
    app = dict()
    params = [
        "id",
        "name",
        "description",
        "enabled",
        "city_country",
        "country_code",
        "latitude",
        "longitude",
        "location",
        "upgrade_day",
        "upgrade_time_in_secs",
        "override_version_profile",
        "version_profile_id",
        "dns_query_type",
    ]
    for param_name in params:
        app[param_name] = module.params.get(param_name, None)
    existing_app = service.getByIDOrName(app.get("id"), app.get("name"))
    if existing_app is not None:
        id = existing_app.get("id")
        existing_app.update(app)
        existing_app["id"] = id
    if state == "present":
        if existing_app is not None:
            """Update"""
            service.update(existing_app)
            module.exit_json(changed=True, data=existing_app)
        else:
            """Create"""
            app = service.create(app)
            module.exit_json(changed=False, data=app)
    elif state == "absent":
        if existing_app is not None:
            service.delete(existing_app.get("id"))
            module.exit_json(changed=False, data=existing_app)
    module.exit_json(changed=False, data={})


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    id_name_spec = dict(type='list', elements='dict', options=dict(id=dict(
        type='str', required=False), name=dict(type='str', required=False)), required=False)
    argument_spec.update(
        connectors=id_name_spec,
        name=dict(type="str", required=True),
        id=dict(type="str", required=False),
        city_country=dict(type="str", required=False),
        country_code=dict(type="str", required=False),
        description=dict(type="str", required=False),
        dns_query_type=dict(type="str", choices=[
                            'IPV4_IPV6', 'IPV4', 'IPV6'], required=False, default="IPV4_IPV6"),
        enabled=dict(type="bool", default=True, required=False),
        latitude=dict(type="str", required=False),
        location=dict(type="str", required=False),
        longitude=dict(type="str", required=False),
        lss_app_connector_group=dict(type="str", required=False),
        upgrade_day=dict(type="str", default="SUNDAY", required=False),
        upgrade_time_in_secs=dict(type="str", default=66600, required=False),
        override_version_profile=dict(
            type="bool", default=False, required=False),
        version_profile_id=dict(type="str", default="0", choices=[
                                '0', '1', '2'], required=False),
        version_profile_name=dict(type="str", required=False),
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
