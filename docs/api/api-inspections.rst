inspections
===========

The |inspections|_ subpackage contains functions that inspect conmponents.
Auxjad automatically adds them as extension methods to |abjad.inspect()|. They
all return a :obj:`bool` value with the exception of
|auxjad.inspect().underfull_duration()| which returns an |abjad.Duration|.


.. note::

    These functions are imported directly into the |auxjad|_ namespace.
    Therefore, to use a function such as |auxjad.inspect().selection_is_full()|
    you only need to import |auxjad|_ and invoke the function from its
    namespace:

    >>> import auxjad
    >>> auxjad.inspect(container[:]).selection_is_full()
    True

    Alternatively, these functions are added as extension methods to
    |abjad.inspect()| too:

    >>> abjad.inspect(container[:]).selection_is_full()
    True

Below is the full list of functions included in |inspections|_. Click on their
names for their individual documentation.

.. autosummary::
    :toctree: ../_api_members

    auxjad.inspect
    auxjad.Inspection

.. |auxjad| replace:: :mod:`auxjad`
.. _auxjad: index.html
.. |inspections| replace:: :mod:`inspections <auxjad.inspections>`
.. _inspections: api-inspections.html

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
