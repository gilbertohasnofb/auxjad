utilities
=========

The |utilities|_ subpackage contains utility functions.

..  note::

    These functions are imported directly into the |auxjad|_ namespace.
    Therefore, to use a function such as
    :func:`auxjad.simplified_time_signature_ratio()` you only need to import
    |auxjad|_ and invoke the function from its namespace:

    >>> import auxjad
    >>> auxjad.simplified_time_signature_ratio(pair)

Below is the full list of functions included in |utilities|_. Click on their
names for their individual documentation.

.. autosummary::
    :toctree: ../_api_members

    auxjad.repeat_container
    auxjad.simplified_time_signature_ratio

.. |auxjad| replace:: :mod:`auxjad`
.. _auxjad: index.html
.. |utilities| replace:: :mod:`utilities <auxjad.utilities>`
.. _utilities: api-utilities.html

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
