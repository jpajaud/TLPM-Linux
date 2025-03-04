import sys
# this line is a quick fix for an error in which the numpy package is not visible to the virtual environment
# sys.path.append('path/to/environment/site-packages')
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