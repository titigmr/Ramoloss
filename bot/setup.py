from setuptools import setup, find_packages


REQUIRED_PACKAGES = open('requirements.txt').readlines()

setup(name="bot",
      install_requires=REQUIRED_PACKAGES,
      packages=find_packages(),
      description='Bot SSBU')