#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ansible.py

Created on 2015-06-01 by Djordje Stojanovic <djordje.stojanovic@shadow-inc.net>
"""
import json
from inventory import OpinionatedDict


class AnsibleInventory(object):
    SSH_HOST = 'ansible_ssh_host'
    SSH_PORT = 'ansible_ssh_port'
    SSH_USER = 'ansible_ssh_user'
    SSH_PASS = 'ansible_ssh_pass'
    SSH_PRIVATE_KEY_FILE = 'ansible_ssh_private_key_file'
    USE_SUDO = 'ansible_sudo'
    SUDO_PASS = 'ansible_sudo_pass'
    SUDO_EXE = 'ansible_sudo_exe'
    SHELL_TYPE = 'ansible_shell_type'
    CONNECTION = 'ansible_connection'
    GENERIC_INTERPETER = lambda interpreter: 'ansible_{0}_interpreter'.format(interpreter)
    PYTHON_INTERPRETER = GENERIC_INTERPETER('python')
    # re_fqdn = re.compile(r'(?=^.{4,255}$)(^((?!-)[a-zA-Z0-9-]{0,62}[a-zA-Z0-9]\.)+[a-zA-Z]{2,63}$)')
    INI_INVENTORY_SECTION = "[{0}]"
    INI_INVENTORY_VAR = "{key}={value}"

    def __init__(self):
        super(AnsibleInventory, self).__init__()
        self.inventory = OpinionatedDict()
        self.host_vars = OpinionatedDict()

    def add_host(self, hostname, host_vars=None, ip_address=None, groups=None):
        if not host_vars:
            host_vars = {}
        if not groups:
            groups = []
        if ip_address:
            host_vars.update({self.SSH_HOST: ip_address})
        self.set_host_vars(hostname, host_vars)
        for g in groups:
            self.add_group(g, hostname)
        return self

    def add_group(self, group, hostname=None):
        if hostname:
            self.inventory.getset(group).getset('hosts', []).append(hostname)
        return self

    def add_children(self, parent_group, child_group):
        self.inventory.getset(parent_group).getset('children', []).append(child_group)
        return self

    def set_host_vars(self, hostname, host_vars=None):
        if not host_vars:
            host_vars = {}
        self.host_vars.getset(hostname).update(host_vars)
        return self

    def set_group_vars(self, group, **group_vars):
        self.inventory.getset(group).getset('vars').update(group_vars)
        return self

    def set_global_vars(self, global_vars):
        self.inventory.getset('all').getset('vars').update(global_vars)
        return self

    def get_host_vars(self, hostname):
        return self.host_vars.get(hostname, None)

    def get_group_vars(self, group):
        return self.inventory.get(group, {}).get('vars', {})

    def get_group_hosts(self, group):
        return self.inventory.get(group, {}).get('hosts', [])

    def get_group_children(self, group):
        return self.inventory.get(group, {}).get('children', [])

    def get_global_vars(self):
        return self.inventory.get('all', {}).get('vars', {})

    def get_host_list(self):
        hosts = list(set(self.host_vars.keys()))
        return hosts

    def get_group_list(self):
        groups = list(set(self.inventory.keys()))
        return groups

    # def is_fqdn(self, hostname):
    #     hostname = hostname.encode('idna').lower()
    #     return bool(self.re_fqdn.match(hostname))

    def to_json(self, indent=2, sort_keys=True, *args, **kwargs):
        complete_inventory = dict()
        if self.host_vars:
            complete_inventory.update({'_meta': {'hostvars': self.host_vars}})
        complete_inventory.update(self.inventory)
        return json.dumps(complete_inventory, indent=indent, sort_keys=sort_keys, *args, **kwargs)

    def to_inventory(self, force=False):
        inventory = str()
        for group in self.get_group_list():
            hosts = self.get_group_hosts(group)
            if hosts:
                # Create new group section
                inventory += self.INI_INVENTORY_SECTION.format(group)
                for host in hosts:
                    inventory += "\n"+host
                    # Add host specific variables
                    for (k, v) in self.get_host_vars(host).iteritems():
                        inventory += " "+self.INI_INVENTORY_VAR.format(key=k, value=v)
            else:
                # Force return of incomplete inventory if no hosts exist for group ? WTF ?
                if not force:
                    return inventory
            children = self.get_group_children(group)
            if children:
                # Add group:children section
                inventory += "\n"+self.INI_INVENTORY_SECTION.format("{0}:children".format(group))
                for child in children:
                    inventory += "\n{0}".format(child)
            variables = self.get_group_vars(group)
            if variables:
                # Add group:vars section
                inventory += "\n"+self.INI_INVENTORY_SECTION.format("{0}:vars".format(group))
                for (k, v) in variables.iteritems():
                    inventory += "\n"+self.INI_INVENTORY_VAR.format(key=k, value=v)
            inventory += "\n\n"
        return inventory
