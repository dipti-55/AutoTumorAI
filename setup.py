'''
This setup.py file is a script for configuring the settings of Python project. It's used with setuptools, a library for packaging Python projects. This file includes metadata about project, such as its name, version, author information, and dependencies. It helps in distributing and installing your project, making it easier for others to use and contribute to it.
'''

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


__version__ = "0.1.0"

REPO_NAME = "Automated-Tumor-Detection"
AUTHOR_USER_NAME = "dipti-55"
SRC_REPO = "Classifier"
AUTHOR_EMAIL = "dipti1010.singh@gmail.com"


setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A Python package for CNN-based tumor detection",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)