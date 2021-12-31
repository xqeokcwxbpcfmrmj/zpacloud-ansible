from ansible_collections.willguibr.zpa.plugins.module_utils.zpa_client import (
    ZPAClientHelper,
)

class AppConnectorGroupService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name):
        app = None
        if id is not None:
            app = self.getByID(id)
        if app is None and name is not None:
            app = self.getByName(name)
        return app

    def getByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/appConnectorGroup/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/appConnectorGroup" % (self.customer_id), data_key_name="list")
        apps = []
        for app in list:
            apps.append(self.mapRespJSONToApp(app))
        return apps

    def getByName(self, name):
        apps = self.getAll()
        for app in apps:
            if app["name"] == name:
                return app
        return None

    def mapRespJSONToApp(self, resp_json):
        return {
            "id": resp_json["id"],
            "name": resp_json["name"],
            "description": resp_json["description"],
            "enabled": resp_json["enabled"],
            "city_country": resp_json["cityCountry"],
            "country_code": resp_json["countryCode"],
            "latitude": resp_json["latitude"],
            "longitude": resp_json["longitude"],
            "location": resp_json["location"],
            "upgrade_day": resp_json["upgradeDay"],
            "upgrade_time_in_secs": resp_json["upgradeTimeInSecs"],
            "override_version_profile": resp_json["overrideVersionProfile"],
            "version_profile_id": resp_json["versionProfileId"],
            "dns_query_type": resp_json["dnsQueryType"],
        }

    def mapAppToJSON(self, app):
        return {
            "id": app["id"],
            "name": app["name"],
            "description": app["description"],
            "enabled": app["enabled"],
            "cityCountry": app["city_country"],
            "countryCode": app["country_code"],
            "latitude": app["latitude"],
            "longitude": app["longitude"],
            "location": app["location"],
            "upgradeDay": app["upgrade_day"],
            "upgradeTimeInSecs": app["upgrade_time_in_secs"],
            "overrideVersionProfile": app["override_version_profile"],
            "versionProfileId": app["version_profile_id"],
            "dnsQueryType": app["dns_query_type"],
        }

    def create(self, app):
        """Create new AppConnectorGroup"""
        appJSON = self.mapAppToJSON(app)
        response = self.rest.post(
            "/mgmtconfig/v1/admin/customers/%s/appConnectorGroup" % (self.customer_id), data=appJSON)
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.mapRespJSONToApp(response.json)

    def update(self, app):
        """update the AppConnectorGroup"""
        appJSON = self.mapAppToJSON(app)
        response = self.rest.put(
            "/mgmtconfig/v1/admin/customers/%s/appConnectorGroup/%s" % (self.customer_id, appJSON["id"]), data=appJSON)
        status_code = response.status_code
        if status_code > 299:
            return None
        return app

    def delete(self, id):
        """delete the AppConnectorGroup"""
        response = self.rest.delete(
            "/mgmtconfig/v1/admin/customers/%s/appConnectorGroup/%s" % (self.customer_id, id))
        return response.status_code
