# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sherlock',
    version='0.1.0',
    description='Data validation tool wrapped around cerberus',
    install_requires=['pandas', 'cerberus'],
    long_description=readme,
    author='Sylvain Bourrat',
    author_email='sylvain@bourrat.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
)