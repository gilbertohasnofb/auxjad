PYTHON := .venv/bin/python

.PHONY: build black-check black-reformat check clean docs-html docs-release flake8 isort-check \
		isort-reformat open-html pydocstyle pytest reformat release release-webpage setup test

# Formatting and linting
black-check: setup
	$(PYTHON) -m black . --check
black-reformat: setup
	$(PYTHON) -m black .
flake8: setup
	$(PYTHON) -m flake8
isort-check: setup
	$(PYTHON) -m isort --check-only --diff .
isort-reformat: setup
	$(PYTHON) -m isort .
pydocstyle: setup
	$(PYTHON) -m pydocstyle
check: black-check flake8 isort-check pydocstyle
reformat: black-reformat isort-reformat

# Testing
pytest: setup
	$(PYTHON) -m pytest

# Building documentation
docs-html:
	$(MAKE) -C docs/ html
open-html:
	$(MAKE) -C docs/ open-html
docs-release:
	$(MAKE) -C docs/ release
release-webpage: docs-html
	rm -Rf auxjad-docs/
	git clone https://github.com/gilbertohasnofb/auxjad-docs auxjad-docs
	rsync -rtv --delete --exclude=.git --exclude=README.rst docs/_build/html/ auxjad-docs/ && \
	cd auxjad-docs && \
	touch .nojekyll && \
	git add -A && \
	git commit -m "Update docs" && \
	git push -u origin main
	rm -Rf auxjad-docs/

# Building library
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -rf {} +
	rm -Rif *.egg-info/
	rm -Rif .cache
	rm -Rif build
	rm -Rif dist
.venv/.installed: requirements.txt
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	touch .venv/.installed
setup: .venv/.installed
build: setup
	$(PYTHON) -m build

# Releasing
release: check pytest docs-release clean build release-webpage
	$(PYTHON) -m twine upload dist/*.tar.gz
