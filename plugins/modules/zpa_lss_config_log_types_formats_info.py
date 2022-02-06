#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, William Guilherme <wguilherme@securitygeek.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
---
module: zpa_lss_config_log_types_formats_info
short_description: Retrieves LSS Log formats Information.
description:
  - This module will allow the retrieval of LSS (Log Streaming Services) Log formats information from the ZPA Cloud.
author: William Guilherme (@willguibr)
version_added: "1.0.0"
requirements:
  - supported starting from zpa_api >= 2.0
options:
  client_id:
    description: ""
    required: false
    type: str
  client_secret:
    description: ""
    required: false
    type: str
  customer_id:
    description: ""
    required: false
    type: str
  log_type:
    description:
      - Log type
    required: true
    choices: ["zpn_trans_log", "zpn_auth_log", "zpn_ast_auth_log", "zpn_http_trans_log", "zpn_audit_log", "zpn_ast_comprehensive_stats"]
    type: str
"""

EXAMPLES = """
    - name: Gather LSS Log types formats
      willguibr.zpacloud.zpa_lss_config_log_types_formats_info:
        log_type: zpn_trans_log
      register: log_types_formats
    - name: log_types_formats
      debug:
        msg: "{{ log_types_formats }}"
"""

RETURN = """
data:
    description: LSS Log formats
    returned: success
    elements: dict
    type: list
    sample: [
      {
            "csv": "...",
            "json": "...",
            "tsv": "..."
      }
    ]
"""

from re import T
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_lss_log_formats import LSSLogFormatsService
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import ZPAClientHelper
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc


def core(module):
    service = LSSLogFormatsService(module)
    log_type = module.params.get("log_type", None)
    lss_log_formats = service.getByLogType(log_type)
    module.exit_json(changed=False, data=lss_log_formats)


def main():
    argument_spec = ZPAClientHelper.zpa_argument_spec()
    argument_spec.update(
        log_type=dict(type="str", required=True, choices=[
                      'zpn_trans_log', 'zpn_auth_log', 'zpn_ast_auth_log',
                      'zpn_http_trans_log', 'zpn_audit_log', 'zpn_ast_comprehensive_stats']),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
