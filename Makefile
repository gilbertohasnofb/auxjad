PYTHON := .venv/bin/python

.PHONY: build black-check black-reformat check clean docs-html docs-release flake8 isort-check \
		sort-reformat pydocstyle reformat release release-webpage setup test

# Setup
.venv/.installed: requirements.txt requirements-dev.txt requirements-test.txt
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install -r requirements-dev.txt
	.venv/bin/pip install -r requirements-test.txt
	touch .venv/.installed
setup: .venv/.installed

# Formatting and linting
black-check:
	@$(PYTHON) -m black . --check
black-reformat:
	@$(PYTHON) -m black .
flake8:
	@$(PYTHON) -m flake8
isort-check:
	@$(PYTHON) -m isort --check-only --diff .
isort-reformat:
	@$(PYTHON) -m isort .
pydocstyle:
	@$(PYTHON) -m pydocstyle
check: black-check flake8 isort-check pydocstyle
reformat: black-reformat isort-reformat

# Unit testing
test:
	@$(PYTHON) -m pytest

# Building documentation
docs-html:
	$(MAKE) -C docs/ docs-html
docs-release:
	$(MAKE) -C docs/ docs-release
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
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -Rif *.egg-info/
	rm -Rif .cache
	rm -Rif build
	rm -Rif dist
build: setup
	@$(PYTHON) -m build

# Releasing
release: check test docs-release clean build release-webpage
	@$(PYTHON) -m twine upload dist/*.tar.gz
