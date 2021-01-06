# sphinx-astrorefs
Astro-style references in Sphinx documents

![Tests](https://github.com/jobovy/sphinx-astrorefs/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/jobovy/sphinx-astrorefs/branch/master/graph/badge.svg)](https://codecov.io/gh/jobovy/sphinx-astrorefs)
[![Documentation Status](https://readthedocs.org/projects/sphinx-astrorefs/badge/?version=latest)](https://sphinx-astrorefs.readthedocs.io/en/latest/?badge=latest)
[![image](http://img.shields.io/pypi/v/sphinx-astrorefs.svg)](https://pypi.python.org/pypi/sphinx-astrorefs/)


``sphinx-astrorefs`` is a Sphinx extension for formatting citations and references in a style similar to that used in the astrophysics literature. It is built on top of [sphinxcontrib-bibtex](https://github.com/mcmtroffaes/sphinxcontrib-bibtex), a Sphinx extension for including bibtex citations in Sphinx documents. By pre- and post-processing the input and output from Sphinx and sphinxcontrib-bibtex, ``sphinx-astrorefs`` allows you to obtain citations in the astro-specific style in the HTML and LaTeX rendering of your Sphinx documents.

* Author: Jo Bovy - bovy at astro dot utoronto dot ca
* Documentation: [https://sphinx-astrorefs.readthedocs.io/](https://sphinx-astrorefs.readthedocs.io/)

## Changelog

* **2021/01/06**: Version 0.6: Small changes for ``sphinxcontrib.bibtex`` version 2.1 (no longer required to run sphinx twice or to commit ``bibtex.json``). This package is compatible with ``sphinxcontrib.bibtex`` v1 and v2.1 and beyond, but not v2.0.
* **2020/12/19**: Version 0.5: Minor bug fixes (missing volume fields, latex preambe) and changes for ``sphinxcontrib.bibtex`` version 2.
* **2020/08/25**: Version 0.4: Adds correct dealing with duplicate labels by adding a letter ('a', 'b', ...) to the year and added the remainder of the AAS macros so they are now all correctly resolved.
* **2020/08/09**: Version 0.3: Fixes a minor bug in 0.2 that caused multiple \citealt-style citations in a single line be parsed incorrectly. All reference replacements are now done one at a time, so multi-citation lines should now be handled correctly for all citation types.
* **2020/07/22**: Version 0.2: Removes printing the Sphinx builder's name and makes the bibtex label invisible in the HTML reference section without removing the element entirely and thus removing the id link, thus fixing the HTML rendering of the reference section.
* **2020/07/01**: Version 0.1.

## Development notes

To release a new version, do the following

* ``bumpversion release`` and commit the result with ``git commit -m "Bump version to next release" .``
* ``git tag `python -c "import sphinx_astrorefs; print(sphinx_astrorefs.__version__)"` && git push --tags``
* `` rm -rf build && rm -rf dist/* && python setup.py sdist bdist_wheel``
* ``twine upload dist/*`` for uploading to PyPI
* ``bumpversion minor`` for setting up development version of next minor release or ``bumpversion major`` for a next major release. Then commit the result with ``git commit -m "Bump version to next development version" .``
