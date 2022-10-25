"""The setup script."""

from setuptools import find_packages
from setuptools import setup
from typing import List
from pathlib import Path

NAME = "milton_maps"
PACKAGES = find_packages()
META_PATH = Path("milton_maps") / "__init__.py"
HERE = Path(__file__).absolute().parent

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

INSTALL_REQUIRES = (HERE/"requirements.txt").read_text().split("\n") # type: List[str]

TEST_REQUIRES = ['pytest>=3',]
SETUP_REQUIRES = ['pytest-runner',]

setup(
    author="Alex Hasha",
    author_email='ahasha@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Analysis of GIS geospatial data sources for Milton, MA",
    entry_points={
        'console_scripts': [
            'milton_maps=milton_maps.cli:main',
        ],
    },
    install_requires=INSTALL_REQUIRES,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='milton_maps',
    name='milton_maps',
    packages=find_packages(include=['milton_maps', 'milton_maps.*']),
    setup_requires=SETUP_REQUIRES,
    test_suite='tests',
    tests_require=TEST_REQUIRES,
    url='https://github.com/ahasha/milton_maps',
    version='0.1.0',
    zip_safe=False,
)
