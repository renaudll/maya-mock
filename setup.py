#!/usr/bin/env python
"""
maya_mock package definition
"""

from setuptools import setup, find_packages

setup(
    name="maya_mock",
    version="1.0",
    description="Mock for Autodesk Maya",
    author="Renaud Lessard Larouche",
    author_email="sigmao@gmail.com",
    url="https://github.com/renaudll/maya-mock",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["enum; python_version < '3.0'", "six", "mock"],
    extras_require={
        "test": ["pytest", "pytest-cov", "coverage", "hypothesis"],
        "doc": ["sphinx", "sphinx-rtd-theme"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Testing :: Mocking",
    ],
)
