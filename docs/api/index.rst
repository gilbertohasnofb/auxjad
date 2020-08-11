Auxjad API
==========

Auxjad is made out of five subpackages: |core|_, |inspections|_, |mutations|_,
|score|_, and |utilities|_. |core|_ contain most of Auxjad's classes and is
focused on algorithmic transformations and manipulations of |abjad.Container|
objects. |inspections|_ and |mutations|_ contain functions for inspecting and
mutating |abjad.Selection|'s in place; Auxjad automatically adds these
functions as extention methods to |abjad.inspect()| and |abjad.mutate()|,
respectively.  |utilities|_ contain a number of utility functions, most of
which take an |abjad.Container| as input. |score|_ contain score component and
component maker classes, such as an expanded leaf maker as well as harmonic
leaves.

..  note::

    Auxjad classes and functions are imported directly into the |auxjad|_
    namespace. Therefore, to use a class such as
    :class:`auxjad.CartographySelector` you only need to import |auxjad|_ and
    instantiate the class from its namespace:

    >>> import auxjad
    >>> selector = auxjad.CartographySelector(pitch_list)

The documentation for the members of each subpackage can be below, as well as
in the navigation pane in the left.

+----------------+------------------------------------------------------------------------------------------------+
| |core|_        | core classes: loopers, shufflers, phasers, selectors, etc.                                     |
+----------------+------------------------------------------------------------------------------------------------+
| |inspections|_ | inspect agent with inspection methods, also included as extension methods in |abjad.inspect()| |
+----------------+------------------------------------------------------------------------------------------------+
| |mutations|_   | mutate agent with mutation methods, also included as extension methods in |abjad.mutate()|     |
+----------------+------------------------------------------------------------------------------------------------+
| |score|_       | score component classes: artificial and natural harmonics.                                     |
+----------------+------------------------------------------------------------------------------------------------+
| |utilities|_   | utility functions                                                                              |
+----------------+------------------------------------------------------------------------------------------------+

.. toctree::
    :hidden:
    :maxdepth: 2
    :caption: Auxjad API

    api-core
    api-inspections
    api-mutations
    api-score
    api-utilities

.. |auxjad| replace:: :mod:`auxjad`
.. _auxjad: index.html
.. |core| replace:: :mod:`core <auxjad.core>`
.. _core: api-core.html
.. |inspections| replace:: :mod:`inspections <auxjad.inspections>`
.. _inspections: api-inspections.html
.. |mutations| replace:: :mod:`mutations <auxjad.mutations>`
.. _mutations: api-mutations.html
.. |score| replace:: :mod:`score <auxjad.score>`
.. _score: api-score.html
.. |utilities| replace:: :mod:`utilities <auxjad.utilities>`
.. _utilities: api-utilities.html

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
