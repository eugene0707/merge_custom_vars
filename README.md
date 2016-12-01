merge_custom_vars
=================

Load vars files with customizable precedence and deep merge hashes within. 
By default vars files loaded from rpi_vars folder in roles included at playbook, overriding by rpi_vars from playbook dir and highest priority have inventory rpi_vars.
You can set your own list of vars files/folders to merge and their precedence.

Requirements
------------

No special requirements.

Role Variables
--------------

rpi_dir: name of vars folder to merge. By default is rpi_vars.

rpi_files: var files or folders to merge. Order of elements in array is means their precedence. 
By default:
* "{{ rpi_role_dirs }}" # rpi_vars folder from roles included in playbook. Roles can be placed inside playbook (local) or another place defined in roles_path config variable ("shared" in my case). 
* "{{ rpi_playbook_dirs }}" # rpi_vars folder in playbook
* "{{ rpi_inventory_dirs }}" # rpi_vars folder in inventory folder. If your inventories placed in their own folders (my case).

So this role do two main things:
1. All hashes contained in rpi_files (yaml, json) merges deeply and writes to tmp folder.
2. Resulting yml with merged variables loads by include_vars task.

Dependencies
------------

Ansible 2+

Example Playbook
----------------

Main concept of this role besides merging hashes is to make common variables, that can be used cross roles, with more precise on playbook and inventory level.
Include this role at first position in playbook, if you use it.

While I have not figured out how to get the vault password from custom module, encrypted variables can be imported into merging "basket" through a lookup plugin, for example:
```
---

secret:
  key: "{{ lookup('file', '{{ playbook_dir }}/files/vault.encrypted.key.txt') }}"

```

License
-------

GPLv2

Author Information
------------------

Evgeniy Kondrashov https://github.com/eugene0707
