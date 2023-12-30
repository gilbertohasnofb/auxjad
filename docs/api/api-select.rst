select
======

The |select|_ subpackage contains selection functions. Selections take as input
an |abjad.Container| or |abjad.Leaf| (depending on the function). They do not
alter the input when return a value (normally an |abjad.Selection|). Auxjad
automatically adds them as extension functions to |abjad.select|.

..  note::

    All selection functions are also added as extension functions to
    |abjad.select|, so it is possible to simply use |abjad.select| instead of
    |auxjad.select|_:

    >>> import abjad
    >>> import auxjad
    >>> logical_selections = abjad.select.logical_selections(container)

Below is the full list of functions included in |select|_. Click on their names
for their individual documentation.

.. currentmodule:: auxjad.select

.. autosummary::
    :toctree: ../_api_members

    logical_selections

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
