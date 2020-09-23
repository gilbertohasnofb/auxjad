indicators
==========

The |indicators|_ subpackage contains extension methods for Abjad's indicator
classes. Currently this subpackage contains only the method
:meth:`~auxjad.TimeSignature.simplify_ratio()` for |abjad.TimeSignature|.

.. note::

    The extension methods are added to Abjad's own classes, and therefore usage
    is as follows:

    >>> import abjad
    >>> import auxjad
    >>> time_signature = abjad.TimeSignature((4, 8))
    >>> time_signature.simplify_ratio()

Below is the full list of extension methods included in |indicators|_.
Click on their names for their individual documentation.

.. currentmodule:: auxjad

.. autosummary::
    :toctree: ../_api_members

    TimeSignature.simplify_ratio

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
