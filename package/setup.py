import sys
from setuptools   import setup, find_packages
import numpy

setup(name = 'tlpmSCPI',
      version='0.0.0',
      description='SCPI interface for ThorLabs PM16-130 that extends functionality to linux',
      author='Jon Pajaud',
      author_email='jpajaud2@gmail.com',
      packages = find_packages(),
      zip_safe=False,
      include_dirs=[numpy.get_include()],
)