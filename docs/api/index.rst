Auxjad API
==========

Auxjad is made out of six subpackages: |core|_, |get|_, |indicators|_,
|mutate|_, |score|_, and |spanners|_. |core|_ contains most of Auxjad's classes
and is focused on algorithmic transformations and manipulations of
|abjad.Container| objects. |indicators|_ and |spanners|_ contain derived
classes and extension methods for Abjad's indicators and spanners. |score|_
contains score component and component maker classes, such as an expanded leaf
maker as well as harmonic leaves. |get|_ and |mutate|_ contains inspection and
mutation functions.

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
| |mutate|_      | mutation functions                                          |
+----------------+-------------------------------------------------------------+
| |score|_       | score component classes: artificial and natural harmonics   |
+----------------+-------------------------------------------------------------+
| |spanners|_    | spanner classes                                             |
+----------------+-------------------------------------------------------------+

.. toctree::
    :hidden:
    :maxdepth: 2
    :caption: Auxjad API

    api-core
    api-get
    api-indicators
    api-mutate
    api-score
    api-spanners

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
