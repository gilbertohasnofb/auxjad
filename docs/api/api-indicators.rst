indicators
==========

The |indicators|_ subpackage contains derived classes and extension
methods for Abjad's indicator classes.

..  note::

    The extension methods are added to Abjad's own classes, and therefore usage
    is as follows:

    >>> import abjad
    >>> import auxjad
    >>> time_signature = abjad.TimeSignature((4, 8))
    >>> time_signature.simplify_ratio()

    The derived classes are imported directly into the |auxjad|_ namespace.

Below is the full list of derived classes and extension methods included in
|indicators|_. Click on their names for their individual documentation.

.. currentmodule:: auxjad

.. autosummary::
    :toctree: ../_api_members

    TimeSignature.simplify_ratio

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
