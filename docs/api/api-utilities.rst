utilities
=========

The |utilities|_ subpackage contains mutation and inspection methods as well
as a couple of utility functions. Mutations and inspections act on an input
|abjad.Selection|, |abjad.Container|, or |abjad.Leaf| (depending on the
function). Mutations transform the input in place, having no return value.
Inspections do not alter the input and return a value (normally a :obj:`bool`).
Auxjad automatically adds them as extension methods to |abjad.mutate()| and
|abjad.inspect()|, respectivelly.

.. note::

    These functions are imported directly into the |auxjad|_ namespace.
    Therefore, to use a function such as
    :func:`auxjad.simplify_time_signature_ratio()` you only need to import
    |auxjad|_ and invoke the function from its namespace. The same is true for
    :func:`auxjad.mutate()` and :func:`auxjad.inspect()`:

    >>> import auxjad
    >>> auxjad.simplify_time_signature_ratio(pair)
    >>> auxjad.mutate(container[:]).rests_to_multimeasure_rest()
    >>> auxjad.inspect(container[:]).selection_is_full()
    True

    Regarding mutations and inspections, these methods are also added as
    extension methods to |abjad.mutate()| and |abjad.inspect()|, so it is
    possible to use |abjad.mutate()| and |abjad.inspect()| instead of
    :func:`auxjad.mutate()` and :func:`auxjad.inspect()`:

    >>> import abjad
    >>> import auxjad
    >>> abjad.mutate(container[:]).rests_to_multimeasure_rest()
    >>> abjad.inspect(container[:]).selection_is_full()
    True

Below is the full list of functions included in |utilities|_. Click on their
names for their individual documentation. :class:`auxjad.Inspection` and
:class:`auxjad.Mutation` will contain the documentaion of all of their methods.

.. autosummary::
    :toctree: ../_api_members

    auxjad.inspect
    auxjad.Inspection
    auxjad.mutate
    auxjad.Mutation
    auxjad.simplify_time_signature_ratio

.. |auxjad| replace:: :mod:`auxjad`
.. _auxjad: index.html
.. |utilities| replace:: :mod:`utilities <auxjad.utilities>`
.. _utilities: api-utilities.html

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
