spanners
========

The |spanners|_ subpackage contains functions that add spanners to containers
and selections.

.. note::

    These functions are imported directly into the |auxjad|_ namespace.
    Therefore, to use a function such as :class:`auxjad.numeric_ottava` you
    only need to import |auxjad|_ and use it directly from |auxjad|_'s
    namespace:

    >>> import abjad
    >>> import auxjad
    >>> staff = abjad.Staff(r"c'''4 d'''4 e'''4 f'''4")
    >>> auxjad.numeric_ottava(staff[:], 1)

Below is the full list of functions included in |spanners|_. Click on their
names for their individual documentation.

.. currentmodule:: auxjad

.. autosummary::
    :toctree: ../_api_members

    numeric_ottava

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
