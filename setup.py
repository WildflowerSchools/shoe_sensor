import os
from setuptools import setup, find_packages


BASEDIR = os.path.dirname(os.path.abspath(__file__))
VERSION = open(os.path.join(BASEDIR, 'VERSION')).read().strip()
REQUIREMENTS = []
DEPENDENCY_LINKS = []


with open(os.path.join(BASEDIR, 'requirements.txt')) as fp:
    lines = fp.readlines()
    for line in lines:
        line = line.strip()
        if ("http://" in line or "https://" in line or "ssh://" in line) and "#egg=" in line:
            parts = line.split("#egg=")
            REQUIREMENTS.append(parts[-1])
            DEPENDENCY_LINKS.append(line)
        elif len(line) and line[0] != "#" and line[0] != "-":
            REQUIREMENTS.append(line)

# allow setup.py to be run from any path
os.chdir(os.path.normpath(BASEDIR))

setup(
    name='shoe_sensor',
    packages=find_packages(),
    version='0.0.1',
    include_package_data=True,
    description='Python package for communicating with Wildflower shoe sensors through BLE interface',
    long_description=open('README.md').read(),
    url='https://github.com/WildflowerSchools/shoe_sensor',
    author='Ted Quinn',
    author_email='ted.quinn@wildflowerschools.org',
    install_requires=REQUIREMENTS,
    dependency_links=DEPENDENCY_LINKS,
    keywords=['bluetooth'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Linux',
        'Programming Language :: Python',
    ]
)
