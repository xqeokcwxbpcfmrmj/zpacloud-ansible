# (Unofficial) Zscaler Private Access (ZPA) Ansible Collection

![Version on Galaxy](https://img.shields.io/badge/dynamic/json?style=flat&label=Ansible+Galaxy&prefix=v&url=https://galaxy.ansible.com/api/v2/collections/willguibr/zpacloud-ansible/&query=latest_version.version)

This collection contains modules and plugins to assist in automating the configuration and operational tasks on
Zscaler Private Access cloud, and API interactions with Ansible.

- Free software: Apache 2.0 License
- Documentation:
    <https://willguibr.github.io/zpacloud-ansible/>
- Repo:
    <https://github.com/willguibr/zpacloud-ansible>
- Example Playbooks:
    <https://github.com/willguibr/zpacloud-playbooks>

## Tested with Ansible

Tested with the current Ansible 2.9 and 2.10 releases and the current development version of Ansible. Ansible versions before 2.9.10 are not supported.

## Included content

- [zpa_app_connector_groups](https://securitygeek.github.io/zpacloud-ansible/modules/zpa_app_connector_groups.html) - Create/Update/Delete an app connector group.
- [zpa_app_connector_groups_info](https://securitygeek.github.io/zpacloud-ansible/modules/zpa_app_connector_groups_info.html) - Gather information details (ID and/or Name) of a app connector group.
- [zpa_application_segment](https://securitygeek.github.io/zpacloud-ansible/modules/application_segment.html) - Create/Update/Delete an application segment.
- [zpa_application_segment_info](https://securitygeek.github.io/zpacloud-ansible/modules/application_segment_info.html) - Gather information details (ID and/or Name) of a application segment.
- [zpa_application_server](https://securitygeek.github.io/zpacloud-ansible/modules/application_server.html) - Create/Update/Delete an Application Server.
- [zpa_application_server_info](https://securitygeek.github.io/zpacloud-ansible/modules/application_server_info.html) - Gather information details (ID and/or Name) of an application server.
- [zpa_ba_certificate_info](https://securitygeek.github.io/zpacloud-ansible/modules/ba_certificate_info.html) - Gather information details (ID and/or Name) of an browser access certificate.
- [zpa_cloud_connector_group_info](https://securitygeek.github.io/zpacloud-ansible/modules/cloud_connector_group_info.html) - Gather information details (ID and/or Name) of an cloud connector group.
- [zpa_customer_version_profile_info](https://securitygeek.github.io/zpacloud-ansible/modules/customer_version_profile_info.html) - Gather information details (ID and/or Name) of an customer version profile for use in app connector group resource in the `version_profile_id` parameter.
- [zpa_enrollment_cert_info](https://securitygeek.github.io/zpacloud-ansible/modules/enrollment_cert_info.html) - Gather information details (ID and/or Name) of an enrollment certificate for use when creating provisioning keys for connector groups or service edge groups.
- [zpa_idp_controller_info](https://securitygeek.github.io/zpacloud-ansible/modules/idp_controller_info.html) - Gather information details (ID and/or Name) of an identity provider (IdP) created in the ZPA tenant.
- [zpa_machine_group_info](https://securitygeek.github.io/zpacloud-ansible/modules/machine_group_info.html) - Gather information details (ID and/or Name) of an machine group for use in a policy access and/or forwarding rules.
- [zpa_policy_access_rule](https://securitygeek.github.io/zpacloud-ansible/modules/policy_access_rule.html) - Create/Update/Delete a policy access rule.
- [zpa_policy_access_rule_info](https://securitygeek.github.io/zpacloud-ansible/modules/policy_access_rule_info.html) - Gather information details (ID and/or Name) of a policy access rule.
- [zpa_policy_access_timeout_rule](https://securitygeek.github.io/zpacloud-ansible/modules/u.html) - Create/Update/Delete a policy access timeout rule.
- [zpa_policy_access_timeout_rule_info](https://securitygeek.github.io/zpacloud-ansible/modules/policy_access_timeout_rule_info.html) - Gather information details (ID and/or Name) of a policy access timeout rule.
- [zpa_policy_access_forwarding_rule](https://securitygeek.github.io/zpacloud-ansible/modules/policy_access_forwarding_rule.html) - Create/Update/Delete a policy access forwarding rule.
- [zpa_policy_access_forwarding_rule_info](https://securitygeek.github.io/zpacloud-ansible/modules/policy_access_forwarding_rule_info.html) - Gather information details (ID and/or Name) of a policy access forwarding rule.
- [zpa_posture_profile_info](https://securitygeek.github.io/zpacloud-ansible/modules/posture_profile_info.html) - Gather information details (ID and/or Name) of a posture profile to use in a policy access, timeout or forwarding rules.
- [zpa_provisioning_key](https://securitygeek.github.io/zpacloud-ansible/modules/provisioning_key.html) - Create/Update/Delete a provisioning key.
- [zpa_provisioning_key_info](https://securitygeek.github.io/zpacloud-ansible/modules/zpa_app_connector_groups.html) - Gather information details (ID and/or Name) of a provisioning key.
- [zpa_saml_attribute_info](https://securitygeek.github.io/zpacloud-ansible/modules/zpa_app_connector_groups.html) - Gather information details (ID and/or Name) of a saml attribute.
- [zpa_scim_attribute_header_info](https://securitygeek.github.io/zpacloud-ansible/modules/zpa_app_connector_groups.html) - Gather information details (ID and/or Name) of a scim attribute header.
- [zpa_scim_group_info](https://securitygeek.github.io/zpacloud-ansible/modules/zpa_app_connector_groups.html) - Gather information details (ID and/or Name) of a scim group.
- [zpa_segment_group](https://securitygeek.github.io/zpacloud-ansible/modules/zpa_app_connector_groups.html) - Create/Update/Delete a segment group.
- [zpa_segment_group_info](https://securitygeek.github.io/zpacloud-ansible/modules/zpa_app_connector_groups.html) - Gather information details (ID and/or Name) of a segment group.
- [zpa_server_group](https://securitygeek.github.io/zpacloud-ansible/modules/zpa_app_connector_groups.html) - Create/Update/Delete a segment group.
- [zpa_server_group_info](https://securitygeek.github.io/zpacloud-ansible/modules/zpa_app_connector_groups.html) - Gather information details (ID and/or Name) of a server group.
- [zpa_service_edge_group_info](https://securitygeek.github.io/zpacloud-ansible/modules/zpa_app_connector_groups.html) - Gather information details (ID and/or Name) of a service edge group.
- [zpa_service_edge_group](https://securitygeek.github.io/zpacloud-ansible/modules/zpa_app_connector_groups.html) - Create/Update/Delete an service edge group.
- [zpa_trusted_network_info](https://securitygeek.github.io/zpacloud-ansible/modules/zpa_app_connector_groups.html) - Gather information details (ID and/or Name) of a trusted network for use in a policy access and/or forwarding rules.

## Installation and Usage

### Installing the Collection from Ansible Galaxy

Before using the DigitalOcean collection, you need to install it with the Ansible Galaxy CLI:

    ansible-galaxy collection install willguibr.zpacloud

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: willguibr.zpacloud
```
