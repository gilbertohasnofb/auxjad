SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help clean html latex images

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	rm -Rif $(BUILDDIR)/*

images:
	rm -Rif "$(SOURCEDIR)"/_images/
	rm -Rif "$(SOURCEDIR)"/_api_members/
	mkdir "$(SOURCEDIR)"/_images/
	mkdir "$(SOURCEDIR)"/_images/lilypond-files/
	python3 ./image-generator.py
	for f in `ls ./_images/lilypond-files/*.ly`; \
		do \
			lilypond -o "_images/" \
			-ddelete-intermediate-files \
			$$include --png \
			-dbackend=eps \
			-dresolution=150 \
			-danti-alias-factor=1 \
			$${f%}; \
	    done;
	find $(SOURCEDIR)/_images/ \
	-name '*.eps' \
	-o -name '*.count' \
	-o -name '*.tex' \
	-o -name '*.texi' | \
	xargs rm

html:
	rm -Rif "$(SOURCEDIR)"/_api_members
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

latex:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	make -C "$(BUILDDIR)"/latex/
	mv "$(BUILDDIR)"/latex/*.pdf "$(SOURCEDIR)"

release:
	make clean
	make images
	make html
