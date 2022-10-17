# (Unofficial) Zscaler Private Access (ZPA) Ansible Collection

![Version on Galaxy](https://img.shields.io/badge/dynamic/json?style=flat&label=Ansible+Galaxy&prefix=v&url=https://galaxy.ansible.com/api/v2/collections/willguibr/zpacloud/&query=latest_version.version)
[![sanity](https://github.com/zscaler/zpacloud-ansible/actions/workflows/ansible-test-sanity.yml/badge.svg?branch=master)](https://github.com/zscaler/zpacloud-ansible/actions/workflows/ansible-test-sanity.yml)
[![integration](https://github.com/zscaler/zpacloud-ansible/actions/workflows/ansible-test-integration.yml/badge.svg?branch=master)](https://github.com/zscaler/zpacloud-ansible/actions/workflows/ansible-test-integration.yml)
[![CI](https://github.com/zscaler/zpacloud-ansible/actions/workflows/CI.yml/badge.svg)](https://github.com/willguibr/zpacloud-ansible/actions/workflows/CI.yml)

This collection contains modules and plugins to assist in automating the configuration and operational tasks on Zscaler Private Access cloud, and API interactions with Ansible.

- Free software: Apache 2.0 License
- Documentation:
    <https://zscaler.github.io/zpacloud-ansible/>
- Repo:
    <https://github.com/zscaler/zpacloud-ansible>
- Example Playbooks:
    <https://github.com/willguibr/zpacloud-playbooks>

## Tested Ansible Versions

This collection is tested with the most current Ansible 2.9 and 2.10 releases. Ansible versions
before 2.9.10 are **not supported**.

## Included content

- [zpa_app_connector_groups](https://zscaler.github.io/zpacloud-ansible/modules/zpa_app_connector_groups.html) - Create/Update/Delete an app connector group.
- [zpa_app_connector_groups_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_app_connector_groups_info.html) - Gather information details (ID and/or Name) of a app connector group.
- [zpa_application_segment](https://zscaler.github.io/zpacloud-ansible/modules/zpa_application_segment.html) - Create/Update/Delete an application segment.
- [zpa_application_segment_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_application_segment_info.html) - Gather information details (ID and/or Name) of a application segment.
- [zpa_application_server](https://zscaler.github.io/zpacloud-ansible/modules/zpa_application_server.html) - Create/Update/Delete an Application Server.
- [zpa_application_server_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_application_server_info.html) - Gather information details (ID and/or Name) of an application server.
- [zpa_ba_certificate_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_ba_certificate_info.html) - Gather information details (ID and/or Name) of an browser access certificate.
- [zpa_cloud_connector_group_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_cloud_connector_group_info.html) - Gather information details (ID and/or Name) of an cloud connector group.
- [zpa_customer_version_profile_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_customer_version_profile_info.html) - Gather information details (ID and/or Name) of an customer version profile for use in app connector group resource in the `version_profile_id` parameter.
- [zpa_enrollment_cert_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_enrollment_cert_info.html) - Gather information details (ID and/or Name) of an enrollment certificate for use when creating provisioning keys for connector groups or service edge groups.
- [zpa_idp_controller_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_idp_controller_info.html) - Gather information details (ID and/or Name) of an identity provider (IdP) created in the ZPA tenant.
- [zpa_machine_group_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_machine_group_info.html) - Gather information details (ID and/or Name) of an machine group for use in a policy access and/or forwarding rules.
- [zpa_policy_access_rule](https://zscaler.github.io/zpacloud-ansible/modules/zpa_policy_access_rule.html) - Create/Update/Delete a policy access rule.
- [zpa_policy_access_rule_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_policy_access_rule_info.html) - Gather information details (ID and/or Name) of a policy access rule.
- [zpa_policy_timeout_rule](https://zscaler.github.io/zpacloud-ansible/modules/zpa_policy_timeout_rule.html) - Create/Update/Delete a policy access timeout rule.
- [zpa_policy_timeout_rule_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_policy_timeout_rule_info.html) - Gather information details (ID and/or Name) of a policy access timeout rule.
- [zpa_policy_forwarding_rule](https://zscaler.github.io/zpacloud-ansible/modules/zpa_policy_forwarding_rule.html) - Create/Update/Delete a policy access forwarding rule.
- [zpa_policy_forwarding_rule_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_policy_forwarding_rule_info.html) - Gather information details (ID and/or Name) of a policy access forwarding rule.
- [zpa_posture_profile_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_posture_profile_info.html) - Gather information details (ID and/or Name) of a posture profile to use in a policy access, timeout or forwarding rules.
- [zpa_provisioning_key](https://zscaler.github.io/zpacloud-ansible/modules/zpa_provisioning_key.html) - Create/Update/Delete a provisioning key.
- [zpa_provisioning_key_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_provisioning_key_info.html) - Gather information details (ID and/or Name) of a provisioning key.
- [zpa_saml_attribute_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_saml_attribute_info.html) - Gather information details (ID and/or Name) of a saml attribute.
- [zpa_scim_attribute_header_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_scim_attribute_header_info.html) - Gather information details (ID and/or Name) of a scim attribute header.
- [zpa_scim_group_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_scim_group_info.html) - Gather information details (ID and/or Name) of a scim group.
- [zpa_segment_group](https://zscaler.github.io/zpacloud-ansible/modules/zpa_segment_group.html) - Create/Update/Delete a segment group.
- [zpa_segment_group_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_segment_group_info.html) - Gather information details (ID and/or Name) of a segment group.
- [zpa_server_group](https://zscaler.github.io/zpacloud-ansible/modules/zpa_server_group.html) - Create/Update/Delete a segment group.
- [zpa_server_group_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_server_group_info.html) - Gather information details (ID and/or Name) of a server group.
- [zpa_service_edge_group_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_service_edge_group_info.html) - Gather information details (ID and/or Name) of a service edge group.
- [zpa_service_edge_group](https://zscaler.github.io/zpacloud-ansible/modules/zpa_service_edge_group.html) - Create/Update/Delete an service edge group.
- [zpa_trusted_network_info](https://zscaler.github.io/zpacloud-ansible/modules/zpa_trusted_network_info.html) - Gather information details (ID and/or Name) of a trusted network for use in a policy access and/or forwarding rules.

## Installation and Usage

Before using the ZPACloud collection, you need to install it with the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install willguibr.zpacloud
```

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
  collections:
    - willguibr.zpacloud
```

### Using modules from the ZPACloud Collection in your playbooks

It's preferable to use content in this collection using their Fully Qualified Collection Namespace (FQCN), for example `willguibr.zpacloud.zpa_app_connector_groups`:

```yaml
---
- hosts: localhost
  gather_facts: false
  connection: local

  tasks:
    - name: Get Information Details of All Customer Version Profiles
      willguibr.zpacloud.zpa_customer_version_profile_info:
      register: version_profile_id

    - name: Create App Connector Group Example
      willguibr.zpacloud.zpa_app_connector_groups:
        name: "Example"
        description: "Example"
        enabled: true
        city_country: "California, US"
        country_code: "US"
        latitude: "37.3382082"
        longitude: "-121.8863286"
        location: "San Jose, CA, USA"
        upgrade_day: "SUNDAY"
        upgrade_time_in_secs: "66600"
        override_version_profile: true
        version_profile_id: "{{ version_profile_id.data[0].id }}"
        dns_query_type: "IPV4"
```

If you are using versions prior to Ansible 2.10 and this collection's existence, you can also define `collections` in your play and refer to this collection's modules as you did in Ansible 2.9 and below, as in this example:

```yaml
---
- hosts: localhost
  gather_facts: false
  connection: local

  collections:
    - zscaler.zpacloud

  tasks:
    - name: Get Information Details of All Customer Version Profiles
      zpa_customer_version_profile_info:
      register: version_profile_id

    - name: Create App Connector Group Example
      zpa_app_connector_groups:
        name: "Example"
        description: "Example"
        enabled: true
        city_country: "California, US"
        country_code: "US"
        latitude: "37.3382082"
        longitude: "-121.8863286"
        location: "San Jose, CA, USA"
        upgrade_day: "SUNDAY"
        upgrade_time_in_secs: "66600"
        override_version_profile: true
        version_profile_id: "{{ version_profile_id.data[0].id }}"
        dns_query_type: "IPV4"
        ...
```

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](http://www.apache.org/licenses/) to see the full text.
