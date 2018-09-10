# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

gh_repo = 'https://github.com/weaming/json-schema-generator'

setup(
    name='json-schema-generator2',  # Required

    version='0.1.13',  # Required

    description='Pretty print json contains python style coments, string literal.',  # Required

    url=gh_repo,  # Optional
    author='weaming',  # Optional
    author_email='garden.yuen@gmail.com',  # Optional

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required

    install_requires=[
        'pretty-format-json',
    ],  # Optional

    keywords='json format',  # Optional

    entry_points={  # Optional
        'console_scripts': [
            'generate-json-schema=json_schema_generator2.generator:main',
        ],
    },

    project_urls={  # Optional
        'Bug Reports': gh_repo,
        'Source': gh_repo,
    },
    )
