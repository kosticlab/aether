from inspect import currentframe, getfile
from os.path import abspath, dirname, basename
from setuptools import setup, find_packages

packages = []

setup(name="aether",
    version="1.0.0",
    description="A system for simultaneously distributing computation across auctioned and non-auctioned cloud machines from various providers in a cost effective manner",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    author="Jacob M. Luber, Braden T. Tierney, Evan M. Cofer, Chirag J. Patel, Aleksandar D. Kostic",
    author_email="jluber@g.harvard.edu",
    url="https://kosticlab.github.io/aether",
    download_url="https://github.com/kosticlab/aether/tarball/master",
    install_requires=['numpy', 'scipy', 'Click'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points='''
        [console_scripts]
        aether=aether.utils.cli:cli
    ''',)
