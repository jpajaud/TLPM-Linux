import sys
sys.path.append('/home/jon/.pythonenv/local_env/lib/python3.12/site-packages')
from setuptools   import setup, find_packages
import numpy

setup(name = 'tlpmSCPI',
      version='0.0.0',
      description='SCPI interface for ThorLabs PM16-130 that extends functionality to linux',
      author='Jon Pajaud',
      author_email='jpajaud@arizona.edu',
      packages = find_packages(),#['quictools','quictools.spins','quictools.models.pspin','quictools.quantum','quictools.constants']
      zip_safe=False,
      include_dirs=[numpy.get_include()],
)
    #   package_data={'quictools':['DocStrings/*.txt']}
# )

# run python setup.py bdist_egg
# resulting egg in in ./dist/ directory