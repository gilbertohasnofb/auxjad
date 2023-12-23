|Auxjad banner|

Welcome to Auxjad's documentation
=================================

|PyPI| |Build| |Python versions| |License| |Bug report|

Auxjad is a library of auxiliary classes and functions for `Abjad 3.4`_ aimed
at composers of algorithmic music. All classes and functions have a |doc|_
attribute with usage instructions.

This library's code is available at the `Auxjad Repository`_ at GitHub.

Bugs can be reported through the project's `Issue Tracker`_.

This library is published under the `MIT License`_.

.. _`Abjad 3.4`: https://abjad.github.io/
.. _`Auxjad Repository`: https://github.com/gilbertohasnofb/auxjad
.. _`Issue Tracker`: https://github.com/gilbertohasnofb/auxjad/issues
.. _`MIT License`: https://github.com/gilbertohasnofb/auxjad/blob/master/LICENSE



Installation
============

The recommended way to install Auxjad is via `pip`_::

    ~$ pip install --user auxjad

Or if you are using virtual environments, simply use::

    ~$ pip install auxjad

You will also need to install `Python 3.9`_ or higher, as well as `Abjad 3.4`_
and `LilyPond`_.



Documentation
=============

Each member of this library is individually documented in the `Auxjad API`_ page. In the `Score gallery`_ page, you will find examples of my own compositions created with these tools. The `Examples of usage`_ page contains simple examples showing some of the capabilities of this library.

.. _`Auxjad API`: https://gilbertohasnofb.github.io/auxjad-docs/api/index.html
.. _`Score gallery`: https://gilbertohasnofb.github.io/auxjad-docs/score_gallery/index.html
.. _`Examples of usage`: https://gilbertohasnofb.github.io/auxjad-docs/examples/index.html



.. toctree::
    :hidden:
    :maxdepth: 2
    :caption: Contents

    self
    examples/index
    score_gallery/index
    api/index


.. |doc| replace:: :attr:`__doc__`
.. _doc: https://docs.python.org/3/tutorial/controlflow.html#tut-docstrings
.. _pip: https://pip.pypa.io/en/stable/
.. _`Python 3.9`: https://www.python.org/
.. _LilyPond: http://lilypond.org/

.. |Auxjad banner| image:: https://raw.githubusercontent.com/gilbertohasnofb/auxjad/master/assets/auxjad-banner.png
   :target: https://github.com/gilbertohasnofb/auxjad
.. |PyPI| image:: https://img.shields.io/pypi/v/auxjad.svg?style=for-the-badge
   :target: https://pypi.python.org/pypi/auxjad
.. |Build| image:: https://img.shields.io/github/actions/workflow/status/gilbertohasnofb/auxjad/github-actions.yml?style=for-the-badge
   :target: https://github.com/gilbertohasnofb/auxjad/actions/workflows/github-actions.yml
.. |Python versions| image:: https://img.shields.io/pypi/pyversions/auxjad.svg?style=for-the-badge
   :target: https://www.python.org/downloads/release/python-390/
.. |License| image:: https://img.shields.io/badge/license-MIT-blue?style=for-the-badge
   :target: https://github.com/gilbertohasnofb/auxjad/blob/master/LICENSE
.. |Bug report| image:: https://img.shields.io/badge/bug-report-red.svg?style=for-the-badge
  :target: https://github.com/gilbertohasnofb/auxjad/issues
