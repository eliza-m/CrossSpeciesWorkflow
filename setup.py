try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(name='species-proteins',
      version='0.0.1',
      py_modules=['species_proteins','glycosylation', 'phosphorylation','structural','sumoylation'],
      packages=find_packages(),
      description='species_proteins')