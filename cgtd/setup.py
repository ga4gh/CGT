#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import sys
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


def parse_reqs(req_path='./requirements.txt'):
    """Recursively parse requirements from nested pip files."""
    install_requires = []
    with codecs.open(req_path, 'r') as handle:
        # remove comments and empty lines
        lines = (line.strip() for line in handle
                 if line.strip() and not line.startswith('#'))
        for line in lines:
            # check for nested requirements files
            if line.startswith('-r'):
                # recursively call this function
                install_requires += parse_reqs(req_path=line[3:])
            else:
                # add the line as a new requirement
                install_requires.append(line)
    return install_requires


# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):

    """Set up the py.test test runner."""

    def finalize_options(self):
        """Set options for the command line."""
        TestCommand.finalize_options(self)
        self.test_args = ['-v']
        self.test_suite = True

    def run_tests(self):
        """Execute the test runner command."""
        # Import here, because outside the required eggs aren't loaded yet
        import pytest
        sys.exit(pytest.main(self.test_args))

setup(
    name='ctgd',
    version='0.1',
    description='Decentralized distributed database of cancer variants and
    clinical data. http: // ga4gh.org /  # /cancergenetrust',
    author='Rob Currie',
    author_email='rcurrie@ucsc.edu',
    packages=find_packages(exclude=('tests*', 'docs', 'examples')),
    include_package_data=True,
    install_requires=parse_reqs(),
    cmdclass=dict(test=PyTest),
    zip_safe=False,
    keywords='pytest cli',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    platforms='any',
    license='BSD License',
    entry_points={
        'console_scripts': ['cgtd = cgtd.cli:base'],
    },
    scripts=[
        'scripts/cgtd',
    ]
)
