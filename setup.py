from inspect import currentframe, getfile
from os.path import abspath, dirname, basename
from setuptools import setup, find_packages

packages = []

setup(name="cumulonimble",
    version="0.0.1",
    description="A system for simultaneously distributing computation across auctioned and non-auctioned cloud machines from various providers in a cost effective manner",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    author="Jacob M. Luber, Braden T. Tierney, Evan M. Cofer, Chirag J. Patel, Aleksandar D. Kostic",
    author_email="jluber@g.harvard.edu",
    url="https://kosticlab.github.io/cumulonimble",
    license="MIT",
    download_url="https://github.com/kosticlab/cumulonimble/tarball/master",
    install_requires=['numpy', 'scipy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'])
