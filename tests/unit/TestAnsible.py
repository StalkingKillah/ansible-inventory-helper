#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TestAnsible.py

Created on 2015-06-10 by Djordje Stojanovic <djordje.stojanovic@shadow-inc.net>
"""
from .. import unittest
import json
import textwrap
from inventory.ansible import AnsibleInventory


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.inventory = AnsibleInventory().add_host('testera-banana',
                                                     host_vars={
                                                         AnsibleInventory.SSH_USER: 'root'
                                                     },
                                                     ip_address='10.1.1.50',
                                                     groups=[
                                                         'droplets', 'image_ubuntu-14-04-x64', 'region_fra1',
                                                         'size_512mb', 'status_new']
                                                     )

    def test_to_json(self):
        """
        {
          "_meta": {
            "hostvars": {
              "testera-banana": {
                "ansible_ssh_host": "10.1.1.50",
                "ansible_ssh_user": "root"
              }
            }
          },
          "droplets": {
            "hosts": [
              "testera-banana"
            ]
          },
          "image_ubuntu-14-04-x64": {
            "hosts": [
              "testera-banana"
            ]
          },
          "region_fra1": {
            "hosts": [
              "testera-banana"
            ]
          },
          "size_512mb": {
            "hosts": [
              "testera-banana"
            ]
          },
          "status_new": {
            "hosts": [
              "testera-banana"
            ]
          }
        }
        """
        self.assertEqual(self.inventory.to_json(indent=None, sort_keys=True),
                         json.dumps(json.loads(self.test_to_json.__doc__), sort_keys=True))

    def test_to_inventory(self):
        """
        [droplets]
        testera-banana ansible_ssh_host=10.1.1.50 ansible_ssh_user=root

        [image_ubuntu-14-04-x64]
        testera-banana ansible_ssh_host=10.1.1.50 ansible_ssh_user=root

        [size_512mb]
        testera-banana ansible_ssh_host=10.1.1.50 ansible_ssh_user=root

        [region_fra1]
        testera-banana ansible_ssh_host=10.1.1.50 ansible_ssh_user=root

        [status_new]
        testera-banana ansible_ssh_host=10.1.1.50 ansible_ssh_user=root

        """
        self.assertEqual(self.inventory.to_inventory(), textwrap.dedent(self.test_to_inventory.__doc__).lstrip())


if __name__ == '__main__':
    unittest.main()
