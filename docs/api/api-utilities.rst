utilities
=========

The |utilities|_ subpackage contains utility functions. Most of these act on
one or more |abjad.Container| as input. Some (but not all) have no return value
and will transform a container in place. Check their individual documentation
pages from the list below for each specific function.

..  note::

    These functions are imported directly into the |auxjad|_ namespace.
    Therefore, to use a function such as :func:`auxjad.close_container()` you
    only need to import |auxjad|_ and invoke the function from its namespace:

    >>> import auxjad
    >>> auxjad.close_container(container)

Below is the full list of functions included in |utilities|_. Click on their
names for their individual documentation.

.. autosummary::
    :toctree: ../_api_members

    auxjad.close_container
    auxjad.enforce_time_signature
    auxjad.fill_with_rests
    auxjad.repeat_container
    auxjad.simplified_time_signature_ratio
    auxjad.sync_containers
    auxjad.time_signature_extractor

.. |auxjad| replace:: :mod:`auxjad`
.. _auxjad: index.html
.. |utilities| replace:: :mod:`utilities <auxjad.utilities>`
.. _utilities: api-utilities.html

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
