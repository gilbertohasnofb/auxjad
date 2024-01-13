SPHINXOPTS    =
SPHINXBUILD   = python3.9 -msphinx  # sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help clean images html latex release

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	rm -Rif $(BUILDDIR)/*
	rm -Rif $(SOURCEDIR)/_logs

images:
	rm -Rif "$(SOURCEDIR)"/_images/
	rm -Rif "$(SOURCEDIR)"/_api_members/
	mkdir "$(SOURCEDIR)"/_images/
	mkdir "$(SOURCEDIR)"/_images/lilypond-files/
	mkdir "$(SOURCEDIR)"/_logs/
	python3.9 ./image-generator.py
	for f in `ls $(SOURCEDIR)/_images/lilypond-files/*.ly`; \
		do \
			echo "Compiling: $$(basename $${f%})"; \
			lilypond -o "$(SOURCEDIR)/_images/" \
			-ddelete-intermediate-files \
			$$include --png \
			-dbackend=eps \
			-dresolution=150 \
			-danti-alias-factor=1 \
			-dlog-file="$(SOURCEDIR)/_logs/$$(basename $${f%.*})" \
			--loglevel=WARN \
			$${f%}; \
	    done;
	find $(SOURCEDIR)/_images/ \
	-name '*.eps' \
	-o -name '*.count' \
	-o -name '*.pdf' \
	-o -name '*.tex' \
	-o -name '*.texi' | \
	xargs rm
	find $(SOURCEDIR)/_logs/ -type f -empty -delete

html:
	rm -Rif "$(SOURCEDIR)"/_api_members
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	firefox --new-tab ./_build/html/index.html

latex:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	make -C "$(BUILDDIR)"/latex/
	mv "$(BUILDDIR)"/latex/*.pdf "$(SOURCEDIR)"

release:
	make clean
	make images
	make html
