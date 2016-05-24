# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='nvidia_exporter',
    version='0.0.1',
    description='Prometheus exporter for NVIDIA GPU information',
    long_description=readme,
    author='Ben Navetta',
    author_email='benjamin_navetta@brown.edu',
    url='https://github.com/roguePanda/nvidia_exporter',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'nvidia-ml-py',
        'prometheus_client'
    ],
    entry_points={
        'console_scripts': [
            'nvidia_exporter = nvidia_exporter.main:main'
        ]
    }
)
