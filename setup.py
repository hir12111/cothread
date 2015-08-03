#!/usr/bin/env python

import glob
import os
import platform
import re

try:
    # We prefer to use setuptools if possible, but it isn't always available
    from setuptools import setup, Extension

    setup_args = dict(
        entry_points = {
            'console_scripts': [
                'pvtree.py = cothread.tools.pvtree:main' ] },
        install_requires = ['numpy'],
        zip_safe = False)

except ImportError:
    from distutils.core import setup, Extension
    setup_args = {}

def get_version():
    """Extracts the version number from the version.py file.
    """
    VERSION_FILE = 'cothread/version.py'
    mo = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', open(VERSION_FILE).read(), re.M)
    if mo:
        version = mo.group(1)
        bs_version = os.environ.get('MODULEVER', '0.0')
        assert bs_version == "0.0" or bs_version == version, \
            "Version {} specified by the build system doesn't match {} in " \
            "version.py".format(bs_version, version)
        return version
    else:
        raise RuntimeError('Unable to find version string in {0}.'.format(VERSION_FILE))

def get_readme():
    """Strip off the header from README.rst and return it
    """
    readme = open("README.rst").read()
    mo = re.search(r'cothread\n[=]*\n', readme, re.M)
    if mo:
        return readme[mo.start():]
    else:
        raise RuntimeError('Unable to find tag in {0}'.format(README_FILE))

# Extension module providing core coroutine functionality.  Very similar in
# spirit to greenlet.
extra_compile_args = [
#    '-Werror',
    '-Wall',
    '-Wextra',
    '-Wno-unused-parameter',
    '-Wno-missing-field-initializers',
    '-Wundef',
    '-Wshadow',
    '-Wcast-align',
    '-Wwrite-strings',
    '-Wredundant-decls',
    '-Wmissing-prototypes',
    '-Wmissing-declarations',
    '-Wstrict-prototypes']
_coroutine = Extension('cothread._coroutine',
    ['context/_coroutine.c', 'context/cocore.c', 'context/switch.c'],
    extra_compile_args = extra_compile_args,
    depends = glob.glob('context/switch-*.c') + glob.glob('context/*.h'))
ext_modules = [_coroutine]

if platform.system() == 'Windows':
    _winlib = Extension(
        'cothread._winlib', ['context/_winlib.c'],
        extra_compile_args = extra_compile_args)
    ext_modules.append(_winlib)

setup(
    name = 'cothread',
    version = get_version(),
    description = 'Cooperative threading based utilities',
    long_description = get_readme(),
    author = 'Michael Abbott',
    author_email = 'Michael.Abbott@diamond.ac.uk',
    url = 'http://controls.diamond.ac.uk/downloads/python/cothread/',
    license = 'GPL2',
    packages = ['cothread', 'cothread.tools'],
    ext_modules = ext_modules,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
    ],
    **setup_args)
