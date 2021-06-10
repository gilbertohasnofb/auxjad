spanners
========

The |spanners|_ subpackage contains functions that add spanners to containers
and selections.

..  note::

    The new functionality of these extended spanner functions are added to
    Abjad's own functions, and therefore usage is as follows:

    >>> import abjad
    >>> import auxjad
    >>> staff = abjad.Staff(r"c'''4 d'''4 e'''4 f'''4")
    >>> abjad.piano_pedal(staff[:])

Below is the full list of functions included in |spanners|_. Click on their
names for their individual documentation.

.. currentmodule:: auxjad

.. autosummary::
    :toctree: ../_api_members

    piano_pedal

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
