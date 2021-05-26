spanners
========

The |spanners|_ subpackage contains functions that add spanners to containers
and selections.

..  note::

    These functions are imported directly into the |auxjad|_ namespace.
    Therefore, to use a function such as :func:`auxjad.half_piano_pedal()` you
    only need to import |auxjad|_ and use it directly from |auxjad|_'s
    namespace:

    >>> import abjad
    >>> import auxjad
    >>> staff = abjad.Staff(r"c'''4 d'''4 e'''4 f'''4")
    >>> auxjad.half_piano_pedal(staff[:], 1)

    These functions are also added to the :mod:`abjad` namespace:

    >>> import abjad
    >>> import auxjad
    >>> staff = abjad.Staff(r"c'''4 d'''4 e'''4 f'''4")
    >>> abjad.half_piano_pedal(staff[:], 1)

Below is the full list of functions included in |spanners|_. Click on their
names for their individual documentation.

.. currentmodule:: auxjad

.. autosummary::
    :toctree: ../_api_members

    half_piano_pedal
    piano_pedal

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
