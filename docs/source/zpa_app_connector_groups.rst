.. _zpa_app_connector_groups
----------------------------

zpa_app_connector_groups -- Create/Update/Delete an App Connector Group.
========================================================================

.. contents::
   :local:
   :depth: 1



Synopsis
--------

Create/Update/Delete an App Connect Group.


Parameters
----------


Notes
-----

Examples
--------

.. code-block:: yaml+jinja

      willguibr.zpacloud.zpa_app_connector_groups:
        state: "absent"
        #id: "216196257331292046"
        name: "Example"
        description: "Example2"
        enabled: true
        city_country: "California, US"
        country_code: "US"
        latitude: "37.3382082"
        longitude: "-121.8863286"
        location: "San Jose, CA, USA"
        upgrade_day: "SUNDAY"
        upgrade_time_in_secs: "66600"
        override_version_profile: true
        version_profile_id: "0"
        dns_query_type: "IPV4"


Status
------



Authors
------

- William Guilherme (@willguibr)