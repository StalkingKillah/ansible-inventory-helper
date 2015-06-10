#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__init__.py

Created on 2015-06-01 by Djordje Stojanovic <djordje.stojanovic@shadow-inc.net>
"""
import sys

if sys.version_info >= (2, 7):
    import unittest  # NOQA
else:
    import unittest2 as unittest  # NOQA