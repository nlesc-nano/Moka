#!/usr/bin/env python
import os

from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(HERE, 'moka', '__version__.py')) as f:
    exec(f.read(), version)


with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='moka',
    version=version,
    description="command line interface to compute and query molecular properties from a database",
    long_description=readme + '\n\n',
    author="Felipe Zapata",
    author_email='f.zapata@esciencecenter.nl',
    url='https://github.com/nlesc-nano/moka',
    packages=[
        'moka',
    ],
    include_package_data=True,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='moka',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': [
            'molecular_server=moka.cli:main'
        ]
    },
    install_requires=[
        'properties_database@git+https://github.com/nlesc-nano/properties_database@master',
        'numpy', 'pandas', 'pyyaml>=5.1.1', 'schema', 'typing-extensions'],
    extras_require={
        'test': ['coverage', 'mypy', 'pycodestyle', 'pytest>=3.9', 'pytest-cov',
                 'pytest-mock'],
        'doc': ['sphinx', 'sphinx-autodoc-typehints', 'sphinx_rtd_theme',
                'nbsphinx']
    },
    data_files=[('citation/moka', ['CITATION.cff'])]
)
