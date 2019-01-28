#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages

setup(
    name='maya_mock',
    version='1.0',
    description='Mock for Autodesk Maya',
    author='Renaud Lessard Larouche',
    author_email='sigmao@gmail.com',
    url='https://github.com/renaudll/maya-mock',
    packages=find_packages(where='python'),  # TODO: remove python to src
    package_dir={'': 'python'},  # TODO: Remove this line
    requires=['enum', 'mock'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Testing :: Mocking',
    ]
)
