.. _zpa_app_connector_groups_info_module:


zpa_app_connector_groups_info -- Gather Details of All App Connector Groups
========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Gather information details (ID and/or Name) of a app connector group.

Requirements
------------

Parameters
----------

Notes
-----

.. note::


Examples
--------

.. code-block:: yaml+jinja

    - name: Gather Details of all App Connector Groups
      willguibr.zpacloud.zpa_app_connector_groups_info:
      register: all_app_connector

    - debug:
        msg: "{{ all_app_connector }}"

    - name: Gather Details of a Specific App Connector Groups by Name
      willguibr.zpacloud.zpa_app_connector_groups_info:
        name: "Example App Connector Group"
      register: app_connector_name

    - debug:
        msg: "{{ app_connector_name }}"

    - name: Gather Details of a Specific App Connector Groups by ID
      willguibr.zpacloud.zpa_app_connector_groups_info:
        id: "216196257331292046"
      register: app_connector_id

    - debug:
        msg: "{{ app_connector_id }}"