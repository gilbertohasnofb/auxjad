Auxjad API
==========

Auxjad is made out of five subpackages: |core|_, |indicators|_, |spanners|_,
|score|_, and |utilities|_. |core|_ contains most of Auxjad's classes and is
focused on algorithmic transformations and manipulations of |abjad.Container|
objects. |indicators|_ and |spanners|_ contain derived classes and extension
methods for Abjad's indicators and spanners. |score|_ contains score component
and component maker classes, such as an expanded leaf maker as well as harmonic
leaves. |utilities|_ contains mutation and inspection methods as well as a
couple of utility functions.

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
| |indicators|_  | indicator classes                                           |
+----------------+-------------------------------------------------------------+
| |score|_       | score component classes: artificial and natural harmonics   |
+----------------+-------------------------------------------------------------+
| |spanners|_    | spanner classes                                             |
+----------------+-------------------------------------------------------------+
| |utilities|_   | mutation methods, inspection methods, and utility functions |
+----------------+-------------------------------------------------------------+

.. toctree::
    :hidden:
    :maxdepth: 2
    :caption: Auxjad API

    api-core
    api-indicators
    api-score
    api-spanners
    api-utilities

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
