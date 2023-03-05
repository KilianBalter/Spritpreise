# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Spritpreise',
    version='1.0.0',
    description='spritpreise',
    long_description=readme,
    author='Kilian Balter; Henrik Siesenop',
    author_email='kilian.balter@th-bingen.de; henrik.siesenop@th-bingen.de',
    url='https://github.com/KilianBalter/Spritpreise',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

