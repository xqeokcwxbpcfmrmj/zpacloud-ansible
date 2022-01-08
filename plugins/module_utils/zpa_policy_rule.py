from ansible_collections.willguibr.zpacloud_ansible.plugins.module_utils.zpa_client import (
    ZPAClientHelper,
)
import re


class PolicyRuleService:
    def __init__(self, module, customer_id):
        self.module = module
        self.customer_id = customer_id
        self.rest = ZPAClientHelper(module)

    def getByIDOrName(self, id, name, policy_set_id, policy_type):
        policy_rule = None
        if id is not None:
            policy_rule = self.getByID(id, policy_set_id)
        if policy_rule is None and name is not None:
            policy_rule = self.getByNameAndType(name, policy_type)
        return policy_rule

    def getByPolicyType(self, policyType):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/policySet/policyType/%s" % (self.customer_id, policyType))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.camelcaseToSnakeCase(response.json)

    def getByID(self, id, policy_set_id):
        response = self.rest.get(
            "/mgmtconfig/v1/admin/customers/%s/policySet/%s/rule/%s" % (self.customer_id, policy_set_id, id))
        status_code = response.status_code
        if status_code != 200:
            return None
        return self.mapRespJSONToPolicy(response.json)

    def getAllByPolicyType(self, policy_type):
        list = self.rest.get_paginated_data(
            base_url="/mgmtconfig/v1/admin/customers/%s/policySet/rules/policyType/%s" % (self.customer_id, policy_type), data_key_name="list")
        policy_rules = []
        for policy_rule in list:
            policy_rules.append(self.mapRespJSONToPolicy(policy_rule))
        return policy_rules

    @staticmethod
    def camelcaseToSnakeCase(obj):
        new_obj = dict()
        for key, value in obj.items():
            if value is not None:
                new_obj[re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()] = value
        return new_obj

    def getByNameAndType(self, name, type):
        policy_rules = self.getAllByPolicyType(type)
        for policy_rule in policy_rules:
            if policy_rule.get("name") == name:
                return policy_rule
        return None

    def mapListJSONToList(self, entities):
        if entities is None:
            return []
        l = []
        for s in entities:
            l.append(self.camelcaseToSnakeCase(s))
        return l

    def mapListToJSONObjList(self, entities):
        if entities is None:
            return []
        l = []
        for e in entities:
            l.append(dict(id=e.get("id")))
        return l

    def mapOperandsToList(self, operandsJSON):
        ops = []
        for op in operandsJSON:
            ops.append({
                "id": op.get("id"),
                "creation_time": op.get("creationTime"),
                "modified_by": op.get("modifiedBy"),
                "object_type": op.get("objectType"),
                "lhs": op.get("lhs"),
                "rhs": op.get("rhs"),
                "name": op.get("name"),
            })
        return ops

    def mapOperandsToListJSON(self, operandsJSON):
        ops = []
        for op in operandsJSON:
            ops.append({
                "objectType": op.get("object_type"),
                "lhs": op.get("lhs"),
                "rhs": op.get("rhs"),
                "name": op.get("name"),
            })
        return ops

    def mapConditionsToList(self, conditionsJSON):
        conds = []
        for cond in conditionsJSON:
            """"""
            conds.append({
                "id": cond.get("id"),
                "modified_time": cond.get("modifiedTime"),
                "creation_time": cond.get("creationTime"),
                "modified_by": cond.get("modifiedBy"),
                "operator": cond.get("operator"),
                "negated": cond.get("negated"),
                "operands": self.mapOperandsToList(cond.get("operands")),
            })
        return conds

    def mapConditionsToJSONList(self, conditions):
        conds = []
        for cond in conditions:
            """"""
            conds.append({
                "operator": cond.get("operator"),
                "negated": cond.get("negated"),
                "operands": self.mapOperandsToListJSON(cond.get("operands")),
            })
        return conds

    def mapRespJSONToPolicy(self, resp_json):
        if resp_json is None:
            return {}
        return {
            "default_rule": resp_json.get("defaultRule"),
            "description": resp_json.get("description"),
            "policy_type": resp_json.get("policyType"),
            "custom_msg": resp_json.get("customMsg"),
            "policy_set_id": resp_json.get("policySetId"),
            "id": resp_json.get("id"),
            "reauth_default_rule": resp_json.get("reauthDefaultRule"),
            "lss_default_rule": resp_json.get("lssDefaultRule"),
            "bypass_default_rule": resp_json.get("reauthDefaultRule"),
            "reauth_idle_timeout": resp_json.get("reauthIdleTimeout"),
            "reauth_timeout": resp_json.get("reauthTimeout"),
            "action_id": resp_json.get("actionId"),
            "name": resp_json.get("name"),
            "app_connector_groups":  self.mapListJSONToList(resp_json.get("appConnectorGroups")),
            "action": resp_json.get("action"),
            "priority": resp_json.get("priority"),
            "operator": resp_json.get("operator"),
            "rule_order": resp_json.get("ruleOrder"),
            "conditions": self.mapConditionsToList(resp_json.get("conditions")),
            "app_server_groups": self.mapListJSONToList(resp_json.get("appServerGroups")),
        }

    def mapAppToJSON(self, policy_rule):
        if policy_rule is None:
            return {}
        return self.delete_none({
            "defaultRule": policy_rule.get("default_rule"),
            "description": policy_rule.get("description"),
            "policyType": policy_rule.get("policy_type"),
            "customMsg": policy_rule.get("custom_msg"),
            "policySetId": policy_rule.get("policy_set_id"),
            "id": policy_rule.get("id"),
            "reauthDefaultRule": policy_rule.get("reauth_default_rule"),
            "lssDefaultRule": policy_rule.get("lss_default_rule"),
            "reauthDefaultRule": policy_rule.get("bypass_default_rule"),
            "reauthIdleTimeout": policy_rule.get("reauth_idle_timeout"),
            "reauthTimeout": policy_rule.get("reauth_timeout"),
            "actionId": policy_rule.get("action_id"),
            "name": policy_rule.get("name"),
            "action": policy_rule.get("action"),
            "priority": policy_rule.get("priority"),
            "operator": policy_rule.get("operator"),
            "ruleOrder": policy_rule.get("rule_order"),
            "conditions": self.mapConditionsToJSONList(policy_rule.get("conditions")),
            "appServerGroups": self.mapListToJSONObjList(policy_rule.get("app_server_groups")),
            "appConnectorGroups":  self.mapListToJSONObjList(policy_rule.get("app_connector_groups")),
        })

    @staticmethod
    def delete_none(_dict):
        """Delete None values recursively from all of the dictionaries, tuples, lists, sets"""
        if isinstance(_dict, dict):
            for key, value in list(_dict.items()):
                if isinstance(value, (list, dict, tuple, set)):
                    _dict[key] = PolicyRuleService.delete_none(value)
                elif value is None or key is None:
                    del _dict[key]
        elif isinstance(_dict, (list, set, tuple)):
            _dict = type(_dict)(PolicyRuleService.delete_none(item)
                                for item in _dict if item is not None)
        return _dict

    def create(self, policy_rule, policy_set_id):
        """Create new Policy rule"""
        segmentGroupJson = self.mapAppToJSON(policy_rule)
        response = self.rest.post(
            "/mgmtconfig/v1/admin/customers/%s/policySet/%s/rule" % (self.customer_id, policy_set_id), data=segmentGroupJson)
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.getByID(response.json.get("id"), policy_set_id)

    def update(self, policy_rule, policy_set_id):
        """update the Policy rule"""
        segmentGroupJson = self.mapAppToJSON(policy_rule)
        response = self.rest.put(
            "/mgmtconfig/v1/admin/customers/%s/policySet/%s/rule/%s" % (self.customer_id, policy_set_id, segmentGroupJson.get("id")), data=segmentGroupJson)
        status_code = response.status_code
        if status_code > 299:
            return None
        return self.getByID(segmentGroupJson.get("id"), policy_set_id)

    def delete(self, id, policy_set_id):
        """delete the Policy rule"""
        response = self.rest.delete(
            "/mgmtconfig/v1/admin/customers/%s/policySet/%s/rule/%s" % (self.customer_id, policy_set_id, id))
        return response.status_code
