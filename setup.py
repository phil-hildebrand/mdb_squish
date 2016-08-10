#!/usr/bin/env python

from setuptools import setup, Command, Extension
import unittest
from os.path import splitext, basename, join as pjoin
import os, sys

class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        self._dir = os.getcwd()

        sys.path.append(self._dir + "/tests")

    def finalize_options(self):
        pass

    def run(self):
        """
        Finds all the tests modules in tests/, and runs them.
        """
        unittest.main(verbosity=1, argv=['', 'discover', 'tests/', 'test_*.py'])

class CleanCommand(Command):
    user_options = []

    def initialize_options(self):
        self._clean_me = []
        for root, dirs, files in os.walk('.'):
            for f in files:
                if f.endswith('.pyc'):
                    self._clean_me.append(pjoin(root, f))

    def finalize_options(self):
        pass

    def run(self):
        for clean_me in self._clean_me:
            try:
                os.unlink(clean_me)
            except:
                pass

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name = 'mdb_squish',
      version = '0.1.0',
      description = 'MongoDB compaction tool',
      url = 'http://github.com/phil-hildebrand/squish',
      author = 'Phil Hildebrand',
      author_email = 'phil.hildebrand@gmail.com',
      license = 'mit',
      install_requires = [ requirements ],
      packages = ['mdb_squish'],
      test_suite="tests",
      use_2to3=True,
#      scripts = ['bin/mdb_squish.py'],
      cmdclass = {'test': TestCommand, 'clean': CleanCommand}
)

