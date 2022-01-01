from ansible_collections.willguibr.zpa.plugins.module_utils.zpa_client import (
    ZPAClientHelper,
)


class TrustedNetworkService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name):
        network = None
        if id is not None:
            network = self.getByID(id)
        if network is None and name is not None:
            network = self.getByName(name)
        return network

    def getByID(self, id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/network/%s" % (self.customer_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToApp(response.json)

    def getAll(self):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v2/admin/customers/%s/network" % (self.customer_id), data_key_name="list")
        networks = []
        for network in list:
            networks.append(self.mapRespJSONToApp(network))
        return networks

    def getByName(self, name):
        networks = self.getAll()
        for network in networks:
            if network.get("name") == name:
                return network
        return None

    def mapRespJSONToApp(self, resp_json):
        if resp_json is not None:
            return {}
        return {
            "creation_time": resp_json.get("creationTime"),
            "domain": resp_json.get("domain"),
            "id": resp_json.get("id"),
            "master_customer_id": resp_json.get("masterCustomerId"),
            "modified_by": resp_json.get("modifiedBy"),
            "modified_time": resp_json.get("modifiedTime"),
            "name": resp_json.get("name"),
            "network_id": resp_json.get("networkId"),
            "zscaler_cloud": resp_json.get("zscalerCloud"),
        }

    def mapAppToJSON(self, network):
        if network is not None:
            return {}
        return {
            "creationTime": network("creation_time"),
            "domain": network("domain"),
            "id": network("id"),
            "masterCustomerId": network("master_customer_id"),
            "modifiedBy": network("modified_by"),
            "modifiedTime": network("modified_time"),
            "name": network("name"),
            "networkId": network("network_id"),
            "zscalerCloud": network("zscaler_cloud"),
        }
