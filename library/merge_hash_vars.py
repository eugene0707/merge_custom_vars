#!/usr/bin/python

# (c) 2016, Evgeniy Kondrashov <eugene0707@gmail.com>
#
# This file is part of merge_custom_vars,
#
# merge_custom_vars is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# merge_custom_vars is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with merge_custom_vars.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

DOCUMENTATION = '''
---
module: merge_hash_vars
short_description: Load vars files (yaml, yml, json), deep merge hashes and save to temp folder
description:
author: "Evgeniy Kondrashov"
'''

from ansible.utils.vars import *
from ansible.parsing.dataloader import DataLoader
import yaml
import tempfile

def merge_files(files2include):
    loader = DataLoader()
    filenames = build_files_list(loader, files2include)
    results = dict()

    for filename in filenames:
        raw_hash = loader.load_from_file(filename)
        results = merge_hash(results, raw_hash)

    tempfd, merged_hash_file = tempfile.mkstemp(suffix='.yml')
    yaml.dump(results, open(merged_hash_file, 'w'), default_flow_style=False)
    os.chown(merged_hash_file, int(os.environ.get('SUDO_UID')), int(os.environ.get('SUDO_GID')))

    results.update(merged_hash_file = merged_hash_file)

    return results

def build_files_list(loader, paths):
    VALID_FILE_EXTENSIONS = ['yaml', 'yml', 'json']

    results = list()
    for filename in paths:
        if not loader.path_exists(filename):
            continue
        if loader.is_file(filename):
            if os.path.splitext(filename)[1][1:] in VALID_FILE_EXTENSIONS:
                results.append(filename)
            else:
                continue
        else:
            results.extend(build_files_list(loader, map((lambda fn: os.path.join(filename, fn)), loader.list_directory(filename))))

    return results


def main():
    module = AnsibleModule(
        argument_spec = dict(
            files = dict(required=False, default=None, type='list'),
        )
    )

    try:
        files2include = module.params.get('files')
        if not files2include:
            files2include = module.params.get('_raw_params')

        module.exit_json(changed=False, ansible_facts=merge_files(files2include))
    except Exception as e:
        module.fail_json(changed=False, msg=repr(e))

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
