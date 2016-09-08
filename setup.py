#! /usr/bin/env python
'''pygeos is designed to make common data processing, plotting and file conversion tasks easier'''
# Be sure that the GEOSOFT API is installed on your machine

from setuptools import setup

setup(name='pygeos',
      version='1.01',
      description='Python interface for common geoscience data crunching tasks',
      maintainer='Eric Daniels',
      maintainer_email='ericbdaniels@gmail.com',
      author='Eric Daniels',
      #license='GPLv3',
      packages=['pygeos'],
      zip_safe = False)

# To install, run python with:
# python setup.py install

#ONLY FOR GEOSOFT API FUNCTIONS
#Geosoft functions require gx developer 8.4
#https://geosoftgxdev.atlassian.net/wiki/display/GD/Version+8.4
