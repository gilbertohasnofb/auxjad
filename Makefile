.PHONY: build clean docs-html docs-release flake8 pydoctsyle release-webpage \
	isort-check isort-reformat pytest reformat release check test

build:
	python3.9 setup.py sdist

clean:
	find . -name '*.pyc' | xargs rm
	rm -Rif *.egg-info/
	rm -Rif .cache
	rm -Rif __pycache__
	rm -Rif build
	rm -Rif dist

docs-html:
	make -C docs/ html

docs-release:
	make -C docs/ release

flake_ignore = --ignore=E203,E266,W503
flake_exclude = --exclude=./sandbox.py,./docs/conf.py

flake8:
	python3.9 -m flake8 ${flake_ignore} ${flake_exclude}

pydocstyle_select = --select=D101,D102,D103,D105,D107

pydoctsyle:
	python3.9 -m pydocstyle ${pydocstyle_select}

release-webpage:
	rm -Rf auxjad-docs/
	git clone https://github.com/gilbertohasnofb/auxjad-docs auxjad-docs
	rsync -rtv --del --exclude=.git --exclude=README.rst \
	docs/_build/html/ auxjad-docs/
	cd auxjad-docs && \
		touch .nojekyll && \
		git add -A && \
		git commit -m "Update docs" && \
		git push -u origin master
	rm -Rf auxjad-docs/

isort-check:
	python3.9 -m isort \
	--case-sensitive \
	--check-only \
	--diff \
	--line-width=79 \
	--multi-line=3 \
	--project=auxjad \
	--skip=auxjad/__init__.py \
	--skip=sandbox.py \
	--trailing-comma \
	--use-parentheses \
	.

isort-reformat:
	python3.9 -m isort \
	--case-sensitive \
	--line-width=79 \
	--multi-line=3 \
	--project=auxjad \
	--skip=auxjad/__init__.py \
	--skip=sandbox.py \
	--trailing-comma \
	--use-parentheses \
	.

pytest:
	python3.9 -m pytest

reformat:
	make isort-reformat

release:
	make test
	make docs-release
	make clean
	make build
	pip install -U twine
	twine upload dist/*.tar.gz
	make release-webpage

check:
	make flake8
	make isort-check

test:
	make flake8
	make pydoctsyle
	make isort-check
	make pytest
