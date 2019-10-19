import os
from setuptools import setup, find_packages

BASEDIR = os.path.dirname(os.path.abspath(__file__))
VERSION = open(os.path.join(BASEDIR, 'VERSION')).read().strip()

BASE_DEPENDENCIES = [
    'wf-database-connection-honeycomb>=0.1.3',
    'bluepy>=1.3.0',
    'click>=7.0'
]

# allow setup.py to be run from any path
os.chdir(os.path.normpath(BASEDIR))

setup(
    name='wf-shoe-sensor',
    packages=find_packages(),
    version=VERSION,
    include_package_data=True,
    description='Python package for communicating with Wildflower shoe sensors through BLE interface',
    long_description=open('README.md').read(),
    url='https://github.com/WildflowerSchools/shoe_sensor',
    author='Theodore Quinn',
    author_email='ted.quinn@wildflowerschools.org',
    install_requires=BASE_DEPENDENCIES,
    keywords=['bluetooth'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
    ]
)
