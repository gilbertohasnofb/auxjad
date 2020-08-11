mutations
=========

The |mutations|_ subpackage contains functions that mutate an input
|abjad.Selection| in place and have no return value. Auxjad automatically adds
them as extension methods to |abjad.mutate()|.

..  note::

    These functions are imported directly into the |auxjad|_ namespace.
    Therefore, to use a function such as
    :func:`auxjad.rests_to_multimeasure_rest()` you only need to import
    |auxjad|_ and invoke the function from its namespace:

    >>> import auxjad
    >>> auxjad.rests_to_multimeasure_rest(container[:])

    Alternatively, these functions are added as extension methods to
    |abjad.mutate()| too:

    >>> abjad.mutate(container[:]).rests_to_multimeasure_rest()

Below is the full list of functions included in |mutations|_. Click on their
names for their individual documentation.

.. autosummary::
    :toctree: ../_api_members

    auxjad.mutate
    auxjad.Mutation

.. |auxjad| replace:: :mod:`auxjad`
.. _auxjad: index.html
.. |mutations| replace:: :mod:`mutations <auxjad.mutations>`
.. _mutations: api-mutations.html

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
