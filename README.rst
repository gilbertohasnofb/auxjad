|Auxjad image|

|PyPI| |Build| |Python versions| |License| |Bug report| |Documentation|

Auxjad is a library of auxiliary classes and functions that extends Abjad (a Python API for building
LilyPond scores) with tools aimed specifically at composers working with algorithmic and generative
techniques. It adds functionality for compositional methods such as manipulating and transforming
musical containers and generating rhythmic and pitch material, along with other utilities that come
up repeatedly when composing my own music in Abjad.

Every class and function is documented with a docstring explaining its usage (also accessible via
their ``__doc__`` attribute), and full documentation with examples is available at the
`Auxjad Docs`_ webpage. Note that Auxjad targets `Abjad 3.4`_ specifically and is not compatible
with newer Abjad releases.

Bugs can be reported through the project's `Issue Tracker`_.

This library is published under the `MIT License`_.


Installation
============

The recommended way to install Auxjad is via `pip`_::

    ~$ pip install --user auxjad

If you are using virtual environments, simply use::

    ~$ pip install auxjad

Auxjad requires `Python 3.10`_ or higher, `LilyPond 2.24`_ or higher, and `Abjad 3.4`_ (exact
version). Please note that Auxjad is **not compatible** with newever versions of Abjad.

.. _`Auxjad Docs`: https://gilbertohasnofb.github.io/auxjad-docs/
.. _`Issue Tracker`: https://github.com/gilbertohasnofb/auxjad/issues
.. _`MIT License`: https://github.com/gilbertohasnofb/auxjad/blob/main/LICENSE

.. _pip: https://pip.pypa.io/en/stable/
.. _`Abjad 3.4`: https://abjad.github.io/
.. _`LilyPond 2.24`: http://lilypond.org/
.. _`Python 3.10`: https://www.python.org/

.. |Auxjad image| image:: https://raw.githubusercontent.com/gilbertohasnofb/auxjad/main/assets/auxjad-banner.png
   :target: https://github.com/gilbertohasnofb/auxjad
.. |PyPI| image:: https://img.shields.io/pypi/v/auxjad.svg?style=for-the-badge
   :target: https://pypi.python.org/pypi/auxjad
.. |Build| image:: https://img.shields.io/github/actions/workflow/status/gilbertohasnofb/auxjad/github-actions.yml?style=for-the-badge
   :target: https://github.com/gilbertohasnofb/auxjad/actions/workflows/github-actions.yml
.. |Python versions| image:: https://img.shields.io/pypi/pyversions/auxjad.svg?style=for-the-badge
   :target: https://www.python.org/downloads/release/python-3100/
.. |License| image:: https://img.shields.io/badge/license-MIT-blue?style=for-the-badge
   :target: https://github.com/gilbertohasnofb/auxjad/blob/main/LICENSE
.. |Bug report| image:: https://img.shields.io/badge/bug-report-red.svg?style=for-the-badge
   :target: https://github.com/gilbertohasnofb/auxjad/issues
.. |Documentation| image:: https://img.shields.io/badge/docs-auxjad.docs-yellow?style=for-the-badge
   :target: https://gilbertohasnofb.github.io/auxjad-docs/
