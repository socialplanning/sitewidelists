from setuptools import setup, find_packages
import sys, os

version = '0.0'
long_description=open('README.txt').read()

setup(name='opencore_sitewidelists',
      version=version,
      description="enable sitewide mailing lists",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author='Ethan Jucovy',
      author_email='',
      url='',
      license='GPLv3 or greater',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[

      ],
      entry_points="""
      [opencore.versions]
      opencore_sitewidelists = opencore_sitewidelists
      [topp.zcmlloader]
      opencore = opencore_sitewidelists
      """,
      )
