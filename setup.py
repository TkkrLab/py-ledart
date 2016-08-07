from distutils.core import setup
from distutils.command.install_data import install_data
from setuptools import find_packages

reqs = []
links = []

with open("Ledart/requirements.txt") as f:
    for line in f:
        line = line.strip()
        if line.startswith("#"):
            continue
        elif "+" in line:
            line = line[line.index("+") + 1:]
            links.append(line)
        else:
            reqs.append(line)

setup(name='Ledart',
      version='0.2',
      description='led controle software.',
      author='Duality (aka Robert van der Tuuk',
      author_email='201292@live.nl',
      license='GPL3',
      packages=find_packages(),
      install_requires=reqs,
      url='https://github.com/tkkrlab/py-ledart',
      download_url = 'https://github.com/tkkrlab/py-ledart/tarbal/0.2',
      dependency_links=links,
      zip_safe=False)
