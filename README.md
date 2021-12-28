(Unofficial) Zscaler Private Access (ZPA) Ansible Collection
=========================

Ansible collection that automates the configuration and operational tasks on
Zscaler Private Access, using the the ZPA API.

-   Free software: Apache 2.0 License
-   Documentation:
    <https://willguibr.github.io/zpa-ansible/>
-   Repo:
    <https://github.com/willguibr/zpa-ansible>
-   Example Playbooks:
    <https://github.com/willguibr/zpa-playbooks>

Tested Ansible Versions
-----------------------

This collection is tested with the most current Ansible 2.9 and 2.10 releases.  Ansible versions
before 2.9.10 are **not supported**.

Installation
------------

Install this collection using the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install willguibr.zpacollection
```

Usage
-----

Either refer to modules by their full FQCN or use the `collections`
specification in your playbooks:

```yaml
  collections:
    - willguibr.zpacollection

  tasks:
  - name: Get the system info
    panos_op:
      provider: '{{ provider }}'
      cmd: 'show system info'
    register: res

  - debug:
      msg: '{{ res.stdout }}'
```

Python Compatibility
--------------------

As Ansible still wants to support python2, this collection will still work
under python2.

Support
-------
