import setuptools

from pathlib import Path

with open(Path(__file__).parent.jointpath('readme.md')) as f:
    readme = f.read()

with open(Path(__file__).parent.jointpath('VERSION')) as f:
    version = f.read()

setuptools.setup(
    name="mjfpl_old",
    version=version,
    author="Kacper Zoladziejewski PyKasztan",
    author_email="kzoladziejewski@gmail..com",
    description="Just joke I am say",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    license="License :: Other/Proprietary License",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
