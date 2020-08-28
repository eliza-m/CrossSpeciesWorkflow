try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(name='species_proteins',
      version='0.0.2',
      py_modules=['species_proteins','glycosylation', 'acetylation','phosphorylation', 'lipid','structural','sumoylation', 'localisation', 'util', 'workflow'],
      packages=find_packages(),
      description='species_proteins')
