#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__init__.py

Created on 2015-06-01 by Djordje Stojanovic <djordje.stojanovic@shadow-inc.net>
"""
import types


class OpinionatedType(type):
    pass


class OpinionatedDict(dict):
    default_factory = property(lambda self, *args, **kwargs: OpinionatedDict(*args, **kwargs), lambda self, value: value)

    def __init__(self, iterable=None, default_factory=None, **kwargs):
        if isinstance(default_factory, types.NoneType):
            self.default_factory = default_factory
        super(OpinionatedDict, self).__init__(iterable or {}, **kwargs)

    def getset(self, key, default=None, *args, **kwargs):
        if isinstance(default, types.NoneType):
            default = self.default_factory
        self.setdefault(key, default)
        return self.get(key)
