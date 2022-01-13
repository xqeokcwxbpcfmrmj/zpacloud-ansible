import re
from ansible_collections.willguibr.zpacloud.plugins.module_utils.zpa_client import (
    ZPAClientHelper,
)


class ApplicationServerService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name):
        application_server = None
        if id is not None:
            application_server = self.getByID(id)
        if application_server is None and name is not None:
            application_server = self.getByName(name)
        return application_server

    def getByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/server/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/server" % (self.customer_id), data_key_name="list")
        application_servers = []
        for application_server in list:
            application_servers.append(self.mapRespJSONToApp(application_server))
        return application_servers

    def getByName(self, name):
        application_servers = self.getAll()
        for application_server in application_servers:
            if application_server.get("name") == name:
                return application_server
        return None

    @staticmethod
    def camelcaseToSnakeCase(obj):
        new_obj = dict()
        for key, value in obj.items():
            if value is not None:
                new_obj[re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()] = value
        return new_obj

    def mapListJSONToList(self, entities):
        if entities is None:
            return []
        l = []
        for s in entities:
            l.append(self.camelcaseToSnakeCase(s))
        return l

    def mapListToJSONList(self, entities):
        if entities is None:
            return []
        l = []
        for e in entities:
            l.append(dict(id=e.get("id")))
        return l

    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "id": resp_json.get("id"),
            "address": resp_json.get("address"),
            "config_space": resp_json.get("configSpace"),
            "name": resp_json.get("name"),
            "description": resp_json.get("description"),
            "enabled": resp_json.get("enabled"),
            "app_server_group_ids": self.mapListJSONToList(resp_json.get("appServerGroupIds")),
        }

    def mapAppToJSON(self, application_server):
        if application_server is None:
            return {}
        return {
            "id": application_server.get("id"),
            "address": application_server.get("address"),
            "configSpace": application_server.get("config_space"),
            "name": application_server.get("name"),
            "description": application_server.get("description"),
            "enabled": application_server.get("enabled"),
            "appServerGroupIds": self.mapListToJSONList(application_server.get("app_server_group_ids")),
        }

    def create(self, application_server):
        """Create new Application Server"""
        ApplicationServerJson = self.mapAppToJSON(application_server)
        response = self.rest.post(
            "/mgmtconfig/v1/admin/customers/%s/server" % (self.customer_id), data=ApplicationServerJson)
        status_code = response.status_code
        if status_code > 299:
           return None
        return self.getByID(response.json.get("id"))

    def update(self, application_server):
        """update the Application Server"""
        ApplicationServerJson = self.mapAppToJSON(application_server)
        response = self.rest.put(
            "/mgmtconfig/v1/admin/customers/%s/server/%s" % (self.customer_id, ApplicationServerJson.get("id")), data=ApplicationServerJson)
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.getByID(ApplicationServerJson.get("id"))

    def delete(self, id):
        """delete the Application Server"""
        response = self.rest.delete(
            "/mgmtconfig/v1/admin/customers/%s/server/%s" % (self.customer_id, id))
        return response.status_code
