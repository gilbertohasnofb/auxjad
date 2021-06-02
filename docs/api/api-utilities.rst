utilities
=========

The |utilities|_ subpackage contains utility functions that are neither
mutations nor inspections.

..  note::

    All utility functions are imported directly into the |auxjad|_ namespace.
    Therefore, to use a function such as :func:`auxjad.staff_splitter` you only
    need to import |auxjad|_ and instantiate the class from its namespace:

    >>> import auxjad
    >>> abjad.staff_splitter(staff)

Below is the full list of functions included in |utilities|_. Click on their
names for their individual documentation.

.. currentmodule:: auxjad

.. autosummary::
    :toctree: ../_api_members

    staff_splitter

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
