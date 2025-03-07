# sphinx-astrorefs
Astro-style references in Sphinx documents

![Tests](https://github.com/jobovy/sphinx-astrorefs/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/jobovy/sphinx-astrorefs/branch/main/graph/badge.svg)](https://codecov.io/gh/jobovy/sphinx-astrorefs)
[![Documentation Status](https://readthedocs.org/projects/sphinx-astrorefs/badge/?version=latest)](https://sphinx-astrorefs.readthedocs.io/en/latest/?badge=latest)
[![image](http://img.shields.io/pypi/v/sphinx-astrorefs.svg)](https://pypi.python.org/pypi/sphinx-astrorefs/)


``sphinx-astrorefs`` is a Sphinx extension for formatting citations and references in a style similar to that used in the astrophysics literature. It is built on top of [sphinxcontrib-bibtex](https://github.com/mcmtroffaes/sphinxcontrib-bibtex), a Sphinx extension for including bibtex citations in Sphinx documents. By pre- and post-processing the input and output from Sphinx and sphinxcontrib-bibtex, ``sphinx-astrorefs`` allows you to obtain citations in the astro-specific style in the HTML and LaTeX rendering of your Sphinx documents.

* Author: Jo Bovy - bovy at astro dot utoronto dot ca
* Documentation: [https://sphinx-astrorefs.readthedocs.io/](https://sphinx-astrorefs.readthedocs.io/)

## Changelog

* **2025/03/06**: Version 0.15: Fix the handling of the ``\apjl`` macro to correctly format the ApJL journal name. Also fix some new syntax errors in the code for reformatting HTML and LaTeX output.
* **2024/11/06**: Version 0.14: Fix id anchors in the reference lists, so links to references are correctly resolved again.
* **2024/10/22**: Version 0.13: Make use of status_iterator compatible again with earlier Sphinx versions.
* **2024/10/21**: Version 0.12: Tweak CSS to make reference section indentation look a bit better. More tweaking may be required for your theme, but this seems to work okay with many common themes.
* **2024/10/21**: Version 0.11: Fixed the use of a deprecated Sphinx function to maintain compatibility with the latest versions of Sphinx.
* **2023/07/23**: Version 0.10: Fix small issue introduced in version 0.9 with how book titles were formatted. Also remove printing ISBN for books.
* **2023/07/23**: Version 0.9: Perform better formatting of book, proceedings, and PhD thesis references that is also more consistent with how articles are formatted.
* **2022/07/06**: Version 0.8: Pin ``sphinxcontrib.bibtex`` version to 2.1.4, because this code doesn't work for more recent versions (yet). Also allow the ``arxiv.org`` part of the arXiv URL to be changed through the ``astrorefs_arxiv_url`` configuration parameter.
* **2021/01/06**: Version 0.7: Further changes for ``sphinxcontrib.bibtex`` version 2.1, because those in version 0.6 were not correct. As in version 0.6, this package is compatible with ``sphinxcontrib.bibtex`` v1 and v2.1 and beyond, but not v2.0.
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
* Create a release on GitHub --> this triggers the GitHub action that will build the package and upload it to PyPI
* Update default version on readthedocs.
* ``bumpversion minor`` for setting up development version of next minor release or ``bumpversion major`` for a next major release. Then commit the result with ``git commit -m "Bump version to next development version" .``
