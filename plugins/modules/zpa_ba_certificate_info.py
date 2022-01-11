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
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_browser_certificate import BrowserCertificateService
from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc

__metaclass__ = type

DOCUMENTATION = r"""
---
module: zpa_ba_certificate_info
short_description: This module can be used to gather information about a browser access certificate.
description:
  - Returns information on a specified Browser Access certificate.
author: William Guilherme (@willguibr)
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 1.0
options:
  name:
    description:
      - Name of the browser certificate.
    required: True
    type: str
  id:
    description:
      - ID of the browser certificate.
    required: false
    type: str
"""

EXAMPLES = """
- name: Gather Details of All Browser Certificates
  willguibr.zpacloud.zpa_ba_certificate_info:

- name: Gather Details of a Specific Browser Certificates by Name
  willguibr.zpacloud.zpa_ba_certificate_info:
    name: crm.acme.com

- name: Gather Details of a Specific Browser Certificates by ID
  willguibr.zpacloud.zpa_ba_certificate_info:
    id: "216196257331282583"
    
"""

RETURN = """
# Returns information on a specified Browser Access certificate.
"""

def core(module):
    certificate_name = module.params.get("name", None)
    certificate_id = module.params.get("id", None)
    customer_id = module.params.get("customer_id", None)
    service = BrowserCertificateService(module, customer_id)
    certificates = []
    if certificate_id is not None:
        certificate = service.getByID(certificate_id)
        if certificate is None:
            module.fail_json(
                msg="Failed to retrieve Browser Certificate ID: '%s'" % (id))
        certificates = [certificate]
    elif certificate_name is not None:
        certificate = service.getByName(certificate_name)
        if certificate is None:
            module.fail_json(
                msg="Failed to retrieve Browser Certificate Name: '%s'" % (certificate_name))
        certificates = [certificate]
    else:
        certificates = service.getAll()
    module.exit_json(changed=False, data=certificates)


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
