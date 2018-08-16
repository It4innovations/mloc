from setuptools import setup, find_packages


with open('requirements.txt') as reqs:
    requirements = [line for line in reqs.read().split('\n') if line]


setup(name='mloc',
      version='0.1',
      description='Machine Learning on Cluster',
      long_description='',
      url='',
      author='Vojtech Cima',
      author_email='cima.vojtech@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=requirements)
