#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from glob import glob
from setuptools import setup
from setuptools import find_packages


project_name = "inijira"


def get_version(*file_paths):
    """Retrieves the version from [your_package]/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = get_version("src", project_name, "__init__.py")


with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = [
    "Click",
    "python-dotenv",
]

test_requirements = [
    "pytest",
    "pytest-env",
]


setup(
    name=project_name,
    version=version,
    description="init jira with incidents in confluence html export",
    long_description=readme,
    author="nmaekawa",
    author_email="nmaekawa@g.harvard.edu",
    url="https://github.com/nmaekawa/" + project_name,
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[
        os.path.splitext(os.path.basename(path))[0] for path in glob("src/*.py")
    ],
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords=project_name,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        "console_scripts": [
            "{}={}.cli:cli".format(project_name, project_name),
        ],
    },
    test_suite="tests",
    tests_require=test_requirements,
)
