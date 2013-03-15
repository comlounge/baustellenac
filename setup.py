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
        "userbase",
        "pymongo",
        "mongogogo",
        "setuptools",
      ],
      entry_points="""
      [nopaste.app_factory]
      main = baustellenac.app:app
      """,
      )
