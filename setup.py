from distutils.core import setup
from setuptools import find_packages
import os

"""
    clearly assumes there already are tags pressent,
    and only gets it for the current branch.
    my case will only be used in the master branch.
"""

with os.popen("git describe --abbrev=0") as fd:
    version = fd.read().strip()

reqs = ['Pillow==3.3.0',
        'PyOpenGL==3.1.0',
        'PyUserInput==0.1.10',
        'cffi==1.7.0',
        'greenlet==0.4.9',
        'pygame-cffi==0.1.1',
        'pyserial==3.1.1',
        'python-xlib==0.16',
        'readline==6.2.4.1',
        'six==1.10.0',
        'wsgiref==0.1.2',
        'pyalsaaudio==0.8.2']

setup(name='Ledart',
      version=version,
      description='led controle software.',
      author='Duality (aka Robert van der Tuuk',
      author_email='201292@live.nl',
      license='GPL3',
      packages=find_packages(),
      install_requires=reqs,
      url='https://github.com/tkkrlab/py-ledart',
      download_url = ('https://github.com/tkkrlab/py-ledart/tarbal/%s' % version),
      zip_safe=False)
