Auxjad API
==========

Auxjad is made out of three subpackages: ``core``, ``score``, and
``utilities``. ``core`` contain most of Auxjad's classes and is focused on
algorithmic transformations and manipulations of ``abjad.Container`` objects.
``utilities`` contain a number of utility functions. ``score`` contain a couple
of classes that can be used as score components, such as artificial harmonics.

..  note::

    Auxjad classes and functions are imported directly into the ``auxjad``
    namespace. Therefore, to use a class such as :class:`CartographySelector`
    you only need to import ``auxjad`` and instantiate the class from its
    namespace:

    >>> import auxjad
    >>> selector = auxjad.CartographySelector(pitch_list)

The documentation for the members of each subpackage can be below, as well as
in the navigation pane in the left.

+--------------+------------------------------------------------------------+
| |core|_      | core classes: loopers, shufflers, phasers, selectors, etc. |
+--------------+------------------------------------------------------------+
| |score|_     | score component classes: artificial and natural harmonics. |
+--------------+------------------------------------------------------------+
| |utilities|_ | utility functions                                          |
+--------------+------------------------------------------------------------+

.. |core| replace:: ``core``
.. _core: api-core.html
.. |score| replace:: ``score``
.. _score: api-score.html
.. |utilities| replace:: ``utilities``
.. _utilities: api-utilities.html

.. toctree::
    :hidden:
    :maxdepth: 2
    :caption: Auxjad API

    api-core
    api-score
    api-utilities
