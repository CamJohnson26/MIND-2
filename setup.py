# http://python-packaging.readthedocs.org/en/latest/minimal.html

from setuptools import setup

setup(name='MIND2',
      version='0.1',
      description='The MIND package',
      url='http://github.com',
      author='Cameron Johnson',
      author_email='',
      license='Closed',
      packages=['MIND2'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'])
