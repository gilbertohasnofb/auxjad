get
===

The |get|_ subpackage contains inspection functions. Inspections take as input
an |abjad.Selection|, |abjad.Container|, or |abjad.Leaf| (depending on the
function). They do not alter the input when return a value (normally a
:obj:`bool`). Auxjad automatically adds them as extension functions to
|abjad.get|.

..  note::

    All mutation functions are also added as extension functions to
    |abjad.get|, so it is possible to simply use |abjad.get| instead of
    |auxjad.get|_:

    >>> import abjad
    >>> import auxjad
    >>> abjad.get.selection_is_full(container[:])
    True

Below is the full list of functions included in |get|_. Click on their names
for their individual documentation.

.. currentmodule:: auxjad.get

.. autosummary::
    :toctree: ../_api_members

    leaves_are_tieable
    selection_is_full
    selections_are_identical
    time_signature_list
    underfull_duration
    virtual_fundamental

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
