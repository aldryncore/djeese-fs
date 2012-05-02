#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fs import __version__
from setuptools import setup, find_packages


INSTALL_REQUIRES = [
    'Django==1.4',
    'Twisted==12.0.0',
    'argparse==1.2.1',
    'certifi==0.0.8',
    'chardet==1.0.1',
    'requests==0.11.2',
    'wsgiref==0.1.2',
    'zope.interface==3.8.0',

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development',
]

setup(
    name='djeesefs',
    version=__version__,
    description='A twisted based daemon file system for djeese',
    author='Jonas Obrist',
    author_email='ojiidotch@gmail.com',
    url='https://github.com/djeese/djeese-fs',
    packages=find_packages(),
    license='Proprietary',
    platforms=['OS Independent'],
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    entry_points="""
    [console_scripts]
    djeesefs = fs.cli:main
    """,
)
