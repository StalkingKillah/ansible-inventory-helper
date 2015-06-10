from distutils.core import setup

from setuptools import find_packages
import sys

tests_require = [
    'nose>=1.3.6',
    'tox>=1.9.2',
]

if sys.version_info < (2, 7):
    tests_require.append('unittest2')

setup(
    name='ansible-dynamic-inventory-helper',
    version='v0.0.1',
    packages=find_packages(exclude=['tests.*', 'tests']),
    url='',
    license='',
    author='Djordje Stojanovic',
    author_email='djordje.stojanovic@shadow-inc.net',
    description='Various helper classes and methods for creating dynamic inventory sources for ansible',
    tests_require=tests_require,
    test_suite='noose.collector',
)
