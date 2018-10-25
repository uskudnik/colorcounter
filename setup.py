# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='colorcounter',
    version='0.5',
    description='Get most common colors from a list of URLs.',
    long_description=readme,
    author='Urban Skudnik',
    author_email='urban.skudnik@gmail.com',
    url='https://github.com/uskudnik/colorcounter',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
