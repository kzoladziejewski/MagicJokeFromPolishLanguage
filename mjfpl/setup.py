import os
import sys

from setuptools import setup, find_packages

sys.path.append('.')
with open('readme.md') as f:
    readme = f.read()

with open(os.path.join('.', 'VERSION')) as f:
    version = f.read()
sys.path.remove('.')

setup(
    name="MagicPolishJokes",
    version=version,
    author="Kacper Zoladziejewski PyKasztan",
    author_email="kzoladziejewski@gmail..com",
    description="Just joke I am say",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['tests']),
include_package_data=True,
    license="License :: Other/Proprietary License",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
