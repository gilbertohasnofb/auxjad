.PHONY: docs build docs-webpage

build:
	python3.6 setup.py sdist

clean:
	find . -name '*.pyc' | xargs rm
	rm -Rif *.egg-info/
	rm -Rif .cache
	rm -Rif __pycache__
	rm -Rif build
	rm -Rif dist

html:
	make -C docs/ html

docs:
	make -C docs/ release

flake_ignore = --ignore=E203,E266,W503
flake_exclude = --exclude=./sandbox.py,./docs/conf.py

flake8:
	python3.6 -m flake8 ${flake_ignore} ${flake_exclude}

docs-webpage:
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
	python3.6 -m isort \
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
	python3.6 -m isort \
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
	python3.6 -m pytest

reformat:
	make isort-reformat

release:
	make test
	make docs
	make clean
	make build
	pip install -U twine
	twine upload dist/*.tar.gz
	make docs-webpage

check:
	make flake8
	make isort-check

test:
	make flake8
	make isort-check
	make pytest
