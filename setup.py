import os
from setuptools import setup, find_packages

requirements = [
    'networkx',
    'numpy',
    'scipy',
]

VERSION = '0.0.1'

setup(
    name='SSNA',
    version=VERSION,
    url='https://github.com/vishwakftw/CS6270-TDBMS',
    description='Datasets, tools and prediction algorithms for signed social networks',
    license='MIT',

    packages=find_packages(exclude=('tests',)),

    zip_safe=True,
    install_requires=requirements,
)
