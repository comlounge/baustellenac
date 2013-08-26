# coding: utf-8
from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='baustellenac',
      version=version,
      description="Baustellen-Datenbank für Aachen",
      long_description="""
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='COM.lounge',
      author_email='info@comlounge.net',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        "starflyer",
        "Paste",
        "PasteDeploy",
        "PasteScript",
        "pymongo",
        "wtforms",
        "mongogogo",
        "userbase",
        "setuptools",
        "requests",
        "geopy",
      ],
      entry_points="""
      [paste.app_factory]
      main = baustellenac.app:app
      [console_scripts]
      import_baustellen = baustellenac.scripts.import_data:import_data

      """,
      )
