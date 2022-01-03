from ansible_collections.willguibr.zpa.plugins.module_utils.zpa_client import (
    ZPAClientHelper,
)


class ApplicationSegmentService:
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
            "/mgmtconfig/v1/admin/customers/%s/application/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/application" % (self.customer_id), data_key_name="list")
        apps = []
        for app in list:
            apps.append(self.mapRespJSONToApp(app))
        return apps

    def getByName(self, name):
        apps = self.getAll()
        for app in apps:
            if app.get("name") == name:
                return app
        return None

    def mapServerGroupsRespJSONToListID(self, serverGroups):
        if serverGroups is None:
            return []
        l = []
        for s in serverGroups:
            l.append(s.get("id"))
        return l

    def mapServerGroupsToJSON(self, serverGroups):
        if serverGroups is None:
            return []
        l = []
        for id in serverGroups:
            l.append(dict(id=id))
        return l

    def mapRespJSONToApp(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "tcp_port_range": resp_json.get("tcpPortRange"),
            "enabled": resp_json.get("enabled"),
            "bypass_type": resp_json.get("bypassType"),
            "udp_port_range": resp_json.get("udpPortRange"),
            "config_space": resp_json.get("configSpace"),
            "health_reporting": resp_json.get("healthReporting"),
            "segment_group_id": resp_json.get("segmentGroupId"),
            "double_encrypt": resp_json.get("doubleEncrypt"),
            "health_check_type": resp_json.get("healthCheckType"),
            "is_cname_enabled": resp_json.get("isCnameEnabled"),
            "passive_health_enabled": resp_json.get("passiveHealthEnabled"),
            "ip_anchored": resp_json.get("ipAnchored"),
            "name": resp_json.get("name"),
            "description": resp_json.get("description"),
            "icmp_access_type": resp_json.get("icmpAccessType"),
            "creation_time": resp_json.get("creationTime"),
            "modifiedby": resp_json.get("modifiedBy"),
            "id": resp_json.get("id"),
            "server_groups": self.mapServerGroupsRespJSONToListID(resp_json.get("serverGroups")),
            "segment_group_name": resp_json.get("segmentGroupName"),
            "domain_names": resp_json.get("domainNames"),
        }

    def mapAppToJSON(self, app):
        if app is None:
            return {}
        return {
            "tcpPortRange": app.get("tcp_port_range"),
            "enabled": app.get("enabled"),
            "bypassType": app.get("bypass_type"),
            "udpPortRange": app.get("udp_port_range"),
            "configSpace": app.get("config_space"),
            "healthReporting": app.get("health_reporting"),
            "segmentGroupId": app.get("segment_group_id"),
            "doubleEncrypt": app.get("double_encrypt"),
            "healthCheckType": app.get("health_check_type"),
            "isCnameEnabled": app.get("is_cname_enabled"),
            "passiveHealthEnabled": app.get("passive_health_enabled"),
            "ipAnchored": app.get("ip_anchored"),
            "name": app.get("name"),
            "description": app.get("description"),
            "icmpAccessType": app.get("icmp_access_type"),
            "creationTime": app.get("creation_time"),
            "modifiedBy": app.get("modifiedby"),
            "id": app.get("id"),
            "serverGroups": self.mapServerGroupsToJSON(app.get("server_groups")),
            "segmentGroupName": app.get("segment_group_name"),
            "domainNames": app.get("domain_names"),
        }

    def create(self, app):
        """Create new application"""
        appJSON = self.mapAppToJSON(app)
        response = self.rest.post(
            "/mgmtconfig/v1/admin/customers/%s/application" % (self.customer_id), data=appJSON)
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.mapRespJSONToApp(response.json)

    def update(self, app):
        """update the application"""
        appJSON = self.mapAppToJSON(app)
        response = self.rest.put(
            "/mgmtconfig/v1/admin/customers/%s/application/%s" % (self.customer_id, appJSON.get("id")), data=appJSON)
        status_code = response.status_code
        if status_code > 299:
            return None
        return app

    def detach_from_segment_group(self, app_id, seg_group_id):
        seg_group = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/segmentGroup/%s" % (self.customer_id, seg_group_id))
        if seg_group.status_code > 299:
            return None
        data = seg_group.json
        apps = data.get("applications", [])
        addaptedApps = []
        for app in apps:
            if app.get("id") != app_id:
                addaptedApps.append(app)
        data["applications"] = addaptedApps
        self.rest.put(
            "/mgmtconfig/v1/admin/customers/%s/segmentGroup/%s" % (self.customer_id, seg_group_id), data=data)

    def delete(self, id):
        """delete the application"""
        response = self.rest.delete(
            "/mgmtconfig/v1/admin/customers/%s/application/%s" % (self.customer_id, id))
        return response.status_code
