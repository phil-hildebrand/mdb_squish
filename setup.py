#!/usr/bin/env python

from setuptools import setup, Command, Extension
import unittest
from os.path import splitext, basename, join as pjoin
import os, sys

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name = 'mdb_squish',
      version = '0.1.2',
      description = 'MongoDB compaction tool',
      url = 'http://github.com/phil-hildebrand/mdb-squish',
      author = 'Phil Hildebrand',
      author_email = 'phil.hildebrand@gmail.com',
      license = 'mit',
      install_requires = [ requirements ],
      packages = ['mdb_squish'],
      package_dir = {'mdb_squish': 'mdb_squish'},
      test_suite="tests",
      use_2to3=True
)
