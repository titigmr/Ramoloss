from setuptools import setup, find_packages

with open('requirements.txt', 'r', encoding='utf-8') as f:
    REQUIRED_PACKAGES = f.readlines()

setup(name="bot",
      install_requires=REQUIRED_PACKAGES,
      packages=find_packages(),
      description='Bot SSBU')
