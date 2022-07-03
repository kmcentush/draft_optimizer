from os import path

from setuptools import find_packages, setup

# Library requirements
here = path.abspath(path.dirname(__file__))
install_requires = open(path.join(here, "requirements.txt")).read().strip().split("\n")

# Version tag
version = open(path.join(here, "version.txt")).read().strip()

# Setup
setup(
    name="draft_optimizer",
    version=version,
    description="Draft Optimizer",
    author="Kyle McEntush",
    author_email="slatebitstudios@gmail.com",
    packages=find_packages(),
    install_requires=install_requires,
)
