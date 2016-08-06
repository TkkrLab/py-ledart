from setuptools import setup, find_packages

def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]

reqs = parse_requirements("Ledart/requirements.txt")

setup(name='ledart',
      version='0.2',
      description='led controle software.',
      url='https://github.com/tkkrlab/py-ledart',
      author='Duality (aka Robert van der Tuuk',
      author_email='201292@live.nl',
      license='GPL3',
      packages=find_packages(),
      install_requires=reqs,
      zip_safe=False)
