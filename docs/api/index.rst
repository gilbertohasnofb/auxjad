Auxjad API
==========

Auxjad is made out of nine subpackages: |core|_, |get|_, |indicators|_,
|makers|_, |mutate|_, |score|_, |select|_, |spanners|_, and |utilities|_.

|core|_ contains most of Auxjad's classes and is focused on algorithmic
transformations and manipulations of |abjad.Container| objects. |indicators|_
and |spanners|_ contain derived classes and extension methods for Abjad's
indicators and spanners. |score|_ contains score component classes, such as
harmonic leaves. |makers|_ contain an expanded leaf making class. |get|_,
|mutate|_, and |select|_ contain inspection, selection, and mutation functions,
respectively. |utilities|_ contain general utility functions..

..  note::

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
| |get|_         | inspection functions                                        |
+----------------+-------------------------------------------------------------+
| |indicators|_  | indicator classes                                           |
+----------------+-------------------------------------------------------------+
| |makers|_      | leaf making classes                                         |
+----------------+-------------------------------------------------------------+
| |mutate|_      | mutation functions                                          |
+----------------+-------------------------------------------------------------+
| |score|_       | score component classes: artificial and natural harmonics   |
+----------------+-------------------------------------------------------------+
| |select|_      | selection functions                                         |
+----------------+-------------------------------------------------------------+
| |spanners|_    | spanner classes                                             |
+----------------+-------------------------------------------------------------+
| |utilities|_   | utility functions                                           |
+----------------+-------------------------------------------------------------+

.. toctree::
    :hidden:
    :maxdepth: 2
    :caption: Auxjad API

    api-core
    api-get
    api-indicators
    api-makers
    api-mutate
    api-score
    api-select
    api-spanners
    api-utilities

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
