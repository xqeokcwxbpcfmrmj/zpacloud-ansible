.. zpa_application_segment_module
----------------------------------

zpa_application_segment -- Create/Update/Delete an Application Segment.
========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Create/Update/Delete an Application Segment.

.. automodule:: zpa_application_segment
   :members:



Parameters
----------

  name: (required: type: str)
   Name of the application.


Notes
-----

Examples
--------

.. code-block:: yaml+jinja

    - name: Create an Application Segment
      willguibr.zpacloud_ansible.zpa_application_segment:
        state: absent
        name: Example Application
        description: Example Application Test
        enabled: true
        health_reporting: ON_ACCESS
        bypass_type: NEVER
        is_cname_enabled: true
        tcp_port_range:
          - from: "80"
            to: "80"
        domain_names:
          - crm1.example.com
          - crm2.example.com
        segment_group_id: "{{ segment_group_id.data.0.id }}"
        server_groups:
          - id: "{{ server_group_id.data.0.id }}"

Status
------





Authors
~~~~~~~

- William Guilherme (@willguibr)
