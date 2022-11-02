.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint lint/flake8
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint/flake8: ## check style with flake8
	flake8 milton_maps tests

lint: lint/flake8 ## check style

test: ## run tests quickly with the default Python
	pytest


test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source milton_maps -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/milton_maps.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ milton_maps
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

clean-raw-data:
	rm -rf data/raw/openspace
	rm -rf data/raw/L3_SHP_M189_MILTON
	rm -rf data/raw/M189_parcels_gdb
	rm -rf data/raw/L3_SHP_M243_QUINCY
	rm -rf data/raw/M243_parcels_gdb

clean-processed-data:
	rm -f data/processed/*.pkl
	rm -f data/processed/*.zip
	rm -f data/processed/*.json

clean-data: clean-raw-data clean-processed-data

refresh-openspace-data:
	rm -rf data/raw/openspace
	curl -o data/raw/openspace.zip https://s3.us-east-1.amazonaws.com/download.massgis.digital.mass.gov/shapefiles/state/openspace.zip
	unzip data/raw/openspace.zip -d data/raw/openspace
	rm data/raw/openspace.zip

refresh-propertytax-data:
	rm -rf data/raw/L3_SHP_M189_MILTON
	rm -rf data/raw/M189_parcels_gdb
	rm -rf data/raw/L3_SHP_M243_QUINCY
	rm -rf data/raw/M243_parcels_gdb
	curl -o data/raw/L3_SHP_M189_MILTON.zip http://download.massgis.digital.mass.gov/shapefiles/l3parcels/L3_SHP_M189_MILTON.zip
	curl -o data/raw/L3_SHP_M243_QUINCY.zip http://download.massgis.digital.mass.gov/shapefiles/l3parcels/L3_SHP_M243_QUINCY.zip
	curl -o data/raw/M189_parcels_gdb.zip http://download.massgis.digital.mass.gov/gdbs/l3parcels/M189_parcels_gdb.zip
	curl -o data/raw/M243_parcels_gdb.zip http://download.massgis.digital.mass.gov/gdbs/l3parcels/M243_parcels_gdb.zip
	unzip data/raw/L3_SHP_M189_MILTON.zip -d data/raw/L3_SHP_M189_MILTON
	unzip data/raw/M189_parcels_gdb.zip -d data/raw/M189_parcels_gdb
	unzip data/raw/L3_SHP_M243_QUINCY.zip -d data/raw/L3_SHP_M243_QUINCY
	unzip data/raw/M243_parcels_gdb.zip -d data/raw/M243_parcels_gdb
	rm data/raw/L3_SHP_M189_MILTON.zip
	rm data/raw/M189_parcels_gdb.zip
	rm data/raw/L3_SHP_M243_QUINCY.zip
	rm data/raw/M243_parcels_gdb.zip

refresh-municipal-boundary-data:
	rm -rf data/raw/townssurvey_shp
	curl -o data/raw/townssurvey_shp.zip https://s3.us-east-1.amazonaws.com/download.massgis.digital.mass.gov/shapefiles/state/townssurvey_shp.zip
	unzip data/raw/townssurvey_shp.zip -d data/raw/townssurvey_shp
	rm data/raw/townssurvey_shp.zip