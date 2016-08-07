from distutils.core import setup
from distutils.command.install_data import install_data
from setuptools import find_packages

setup(name='ledart',
      version='0.2',
      description='led controle software.',
      url='https://github.com/tkkrlab/py-ledart',
      author='Duality (aka Robert van der Tuuk',
      author_email='201292@live.nl',
      license='GPL3',
      packages=find_packages(),
      install_requires=['pip'],
      zip_safe=False)
