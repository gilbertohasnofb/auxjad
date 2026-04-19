.PHONY: build black-check black-reformat clean docs-html docs-release flake8 pydocstyle \
	release-webpage isort-check isort-reformat pytest reformat release check test

# Formatting and linting
black-check:
	python3 -m black . --check
black-reformat:
	python3 -m black .
flake8:
	python3 -m flake8
isort-check:
	python3 -m isort --check-only --diff .
isort-reformat:
	python3 -m isort .
pydocstyle:
	python3 -m pydocstyle
check:
	$(MAKE) black-check
	$(MAKE) flake8
	$(MAKE) isort-check
	$(MAKE) pydocstyle
reformat:
	$(MAKE) black-reformat
	$(MAKE) isort-reformat

# Testing
pytest:
	python3 -m pytest
test:
	$(MAKE) check
	$(MAKE) pytest

# Building documentation
docs-html:
	$(MAKE) -C docs/ html
docs-release:
	$(MAKE) -C docs/ release
release-webpage:
	rm -Rf auxjad-docs/
	git clone https://github.com/gilbertohasnofb/auxjad-docs auxjad-docs
	rsync -rtv --delete --exclude=.git --exclude=README.rst docs/_build/html/ auxjad-docs/ && \
	cd auxjad-docs && \
	touch .nojekyll && \
	git add -A && \
	git commit -m "Update docs" && \
	git push -u origin master
	rm -Rf auxjad-docs/

# Building library
clean:
	find . -name '*.pyc' -delete
	rm -Rif *.egg-info/
	rm -Rif .cache
	rm -Rif __pycache__
	rm -Rif build
	rm -Rif dist
build:
	python3 -m build

# Releasing
release:
	$(MAKE) test
	$(MAKE) docs-release
	$(MAKE) clean
	$(MAKE) build
	pip install -U twine
	python3 -m twine upload dist/*.tar.gz
	$(MAKE) release-webpage
