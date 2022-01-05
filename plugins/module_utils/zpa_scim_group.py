from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import (
    ZPAClientHelper,
)


class ScimGroupService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name):
        group = None
        if id is not None:
            group = self.getByID(id)
        if group is None and name is not None:
            group = self.getByName(name)
        return group

    def getByID(self, id):
        response = self.rest.get(
            "/userconfig/v1/customers/%s/scimgroup/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self, id):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/customers/%s/scimgroup/idp/%s" % (self.customer_id, id), data_key_name="list")
        groups = []
        for group in list:
            groups.append(self.mapRespJSONToApp(group))
        return groups

    def getByName(self, name):
        groups = self.getAll()
        for group in groups:
            if group.get("name") == name:
                return group
        return None

    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "creation_time": resp_json.get("creationTime"),
            "id": resp_json.get("id"),
            "idp_group_id": resp_json.get("idpGroupId"),
            "idp_id": resp_json.get("idpId"),
            "modified_time": resp_json.get("modifiedTime"),
            "name": resp_json.get("name"),
        }

    def mapAppToJSON(self, group):
        if group is None:
            return {}
        return {
            "creationTime": group.get("creation_time"),
            "id": group.get("id"),
            "idpGroupId": group.get("idp_group_id"),
            "idpId": group.get("idp_id"),
            "modifiedTime": group.get("modified_time"),
            "name": group.get("name"),
        }
