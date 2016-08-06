from setuptools import setup, find_packages
from distutils.command.install import install
import subprocess as sp

# reqs = parse_requirements("Ledart/requirements.txt")

class PipInstall(install):
    def run(self):
        install.run(self)

        p = sp.Popen("pip install -r Ledart/requirements.txt", shell=False,
                     stdout=sp.PIPE)
        out, err = p.communicate()

setup(name='ledart',
      version='0.2',
      description='led controle software.',
      url='https://github.com/tkkrlab/py-ledart',
      author='Duality (aka Robert van der Tuuk',
      author_email='201292@live.nl',
      license='GPL3',
      packages=find_packages(),
      install_requires=['pip'],
      cmdclass=dict(install=PipInstall),
      zip_safe=False)
