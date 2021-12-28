# (c) 2018 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
author:
    - William Guilherme (@willguibr)
httpapi : zpacollection
short_description: HttpApi plugin for Zscaler Private Access
description:
    - HttpApi plugin for Zscaler Private Access
version_added: '1.0.0'
options:
    api_key:
        type: str
        description:
            - Use API key for authentication instead of client_id and client_secret
        vars:
            - name: ansible_api_key
"""

import json

from ansible.module_utils.basic import to_text
from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.plugins.httpapi import HttpApiBase
from ansible.module_utils.connection import ConnectionError

BASE_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Ansible',
}


class HttpApi(HttpApiBase):
    def login(self, client_id, client_secret):
        payload = {}
        client_id = self.get_option('client_id')
        client_secret = self.get_option('client_secret')
        if client_id:
            payload['client_id'] = client_id
        if client_id and not client_secret:
            payload['client_id'] = client_id
            payload['client_secret'] = client_secret
        elif client_secret and not client_id:
            payload['client_secret'] = client_secret
        else:
            raise AnsibleConnectionFailure('[Client ID and Client Secret] are required for login')
        url = 'https://config.private.zscaler.com/signin'
        
        response, response_data = self.send_request(url, payload)

        try:
            self.connection._auth = {'X-chkp-sid': response_data['sid']}
            self.connection._session_uid = response_data['uid']
        except KeyError:
            raise ConnectionError(
                'Server returned response without token info during connection authentication: %s' % response)

    def get_session_uid(self):
        return self.connection._session_uid

    def send_request(self, path, body_params):
        data = json.dumps(body_params) if body_params else '{}'

        try:
            self._display_request()
            response, response_data = self.connection.send(path, data, method='POST', headers=BASE_HEADERS)
            value = self._get_response_value(response_data)

            return response.getcode(), self._response_to_json(value)
        except AnsibleConnectionFailure as e:
            return 404, e.message
        except HTTPError as e:
            error = json.loads(e.read())
            return e.code, error

    def _display_request(self):
        self.connection.queue_message('vvvv', 'Web Services: %s %s' % ('POST', self.connection._url))

    def _get_response_value(self, response_data):
        return to_text(response_data.getvalue())

    def _response_to_json(self, response_text):
        try:
            return json.loads(response_text) if response_text else {}
        # JSONDecodeError only available on Python 3.5+
        except ValueError:
            raise ConnectionError('Invalid JSON response: %s' % response_text)
