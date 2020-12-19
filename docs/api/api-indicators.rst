indicators
==========

The |indicators|_ subpackage contains derived classes and extension
methods for Abjad's indicator classes.

.. note::

    The extension methods are added to Abjad's own classes, and therefore usage
    is as follows:

    >>> import abjad
    >>> import auxjad
    >>> time_signature = abjad.TimeSignature((4, 8))
    >>> time_signature.simplify_ratio()

    The derived classes are imported directly into the |auxjad|_ namespace.
    Therefore, to use a class such as :class:`auxjad.NumericOttava` you only
    need to import |auxjad|_ and instantiate the class from its namespace:

    >>> import auxjad
    >>> ottava = auxjad.NumericOttava(2)

Below is the full list of derived classes and extension methods included in
|indicators|_. Click on their names for their individual documentation.

.. currentmodule:: auxjad

.. autosummary::
    :toctree: ../_api_members

    NumericOttava
    TimeSignature.simplify_ratio

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
