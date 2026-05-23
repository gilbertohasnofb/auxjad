PYTHON      ?= ../.venv/bin/python
SPHINXOPTS   =
SPHINXBUILD  = $(PYTHON) -m sphinx
SOURCEDIR    = .
BUILDDIR     = _build
OPEN         := $(shell command -v xdg-open || command -v open)

.PHONY: docs-clean docs-help docs-html docs-images docs-latex docs-release

docs-help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

docs-clean:
	rm -Rif $(BUILDDIR)/*
	rm -Rif $(SOURCEDIR)/_logs
	rm -Rif $(SOURCEDIR)/_api_members

docs-images:
	rm -Rif $(SOURCEDIR)/_images/
	mkdir -p $(SOURCEDIR)/_images/lilypond-files/
	mkdir $(SOURCEDIR)/_logs/
	$(PYTHON) ./image-generator.py
	for f in `ls $(SOURCEDIR)/_images/lilypond-files/*.ly`; \
		do \
			echo "Compiling: $$(basename $${f%})"; \
			lilypond -o "$(SOURCEDIR)/_images/" \
			-ddelete-intermediate-files \
			--png \
			-dbackend=eps \
			-dresolution=150 \
			-danti-alias-factor=1 \
			-dlog-file="$(SOURCEDIR)/_logs/$$(basename $${f%.*})" \
			--loglevel=WARN \
			$${f%}; \
		done;
	find $(SOURCEDIR)/_images/ \
		\( -name '*.eps' \
		-o -name '*.count' \
		-o -name '*.pdf' \
		-o -name '*.tex' \
		-o -name '*.texi' \) \
		-delete
	find $(SOURCEDIR)/_logs/ -type f -empty -delete

docs-html:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	$(OPEN) ./_build/html/index.html

docs-latex:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	$(MAKE) -C "$(BUILDDIR)"/latex/
	mv "$(BUILDDIR)"/latex/*.pdf "$(SOURCEDIR)"

docs-release: docs-clean docs-images docs-html
