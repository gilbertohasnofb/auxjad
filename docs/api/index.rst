Auxjad API
==========

Auxjad is made out of three subpackages: |core|_, |score|_, and |utilities|_.
|core|_ contains most of Auxjad's classes and is focused on algorithmic
transformations and manipulations of |abjad.Container| objects. |score|_
contains score component and component maker classes, such as an expanded leaf
maker as well as harmonic leaves. |utilities|_ contains mutation and inspection
methods as well as a couple of utility functions.

.. note::

    Auxjad classes and functions are imported directly into the |auxjad|_
    namespace. Therefore, to use a class such as
    :class:`auxjad.CartographySelector` you only need to import |auxjad|_ and
    instantiate the class from its namespace:

    >>> import auxjad
    >>> selector = auxjad.CartographySelector(pitch_list)

The documentation for the members of each subpackage can be below, as well as
in the navigation pane in the left.

+----------------+-------------------------------------------------------------+
| |core|_        | core classes: loopers, shufflers, phasers, selectors, etc.  |
+----------------+-------------------------------------------------------------+
| |score|_       | score component classes: artificial and natural harmonics.  |
+----------------+-------------------------------------------------------------+
| |utilities|_   | mutation methods, inspection methods, and utility functions |
+----------------+-------------------------------------------------------------+

.. toctree::
    :hidden:
    :maxdepth: 2
    :caption: Auxjad API

    api-core
    api-score
    api-utilities

.. |auxjad| replace:: :mod:`auxjad`
.. _auxjad: index.html
.. |core| replace:: :mod:`core <auxjad.core>`
.. _core: api-core.html
.. |score| replace:: :mod:`score <auxjad.score>`
.. _score: api-score.html
.. |utilities| replace:: :mod:`utilities <auxjad.utilities>`
.. _utilities: api-utilities.html

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
