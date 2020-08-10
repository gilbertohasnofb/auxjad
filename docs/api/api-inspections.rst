inspections
===========

The |inspections|_ subpackage contains inspection functions. Auxjad
automatically adds them as extension methods to |abjad.inspect()|. They all
take |abjad.Selection| as input type and return either a :obj:`bool` value or
an |abjad.Duration| in the case of :func:`auxjad.underfull_duration()`.

..  note::

    These functions are imported directly into the |auxjad|_ namespace.
    Therefore, to use a function such as :func:`auxjad.selection_is_full()` you
    only need to import |auxjad|_ and invoke the function from its namespace:

    >>> import auxjad
    >>> auxjad.selection_is_full(container[:])
    True

    Alternatively, these functions are added as extension methods to
    |abjad.mutate()| too:

    >>> abjad.inspect(container[:]).selection_is_full()
    True

Below is the full list of functions included in |inspections|_. Click on their
names for their individual documentation.

.. autosummary::
    :toctree: ../_api_members

    auxjad.leaves_are_tieable
    auxjad.selection_is_full
    auxjad.selections_are_equal
    auxjad.underfull_duration

.. |auxjad| replace:: :mod:`auxjad`
.. _auxjad: index.html
.. |inspections| replace:: :mod:`inspections <auxjad.inspections>`
.. _inspections: api-inspections.html

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
