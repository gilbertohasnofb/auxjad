utilities
=========

The |utilities|_ subpackage contains utility functions which include mutation
functions (e.g. to adjust indicators of a container in place) and :obj:`bool`
functions (e.g. to check whether a container satisfy some condition).

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
    auxjad.container_is_full
    auxjad.containers_are_equal
    auxjad.enforce_time_signature
    auxjad.fill_with_rests
    auxjad.leaves_are_tieable
    auxjad.prettify_rewrite_meter
    auxjad.remove_empty_tuplets
    auxjad.remove_repeated_dynamics
    auxjad.remove_repeated_time_signatures
    auxjad.repeat_container
    auxjad.reposition_clefs
    auxjad.reposition_dynamics
    auxjad.reposition_slurs
    auxjad.respell_chord
    auxjad.respell_container
    auxjad.rests_to_multimeasure_rest
    auxjad.simplified_time_signature_ratio
    auxjad.sync_containers
    auxjad.time_signature_extractor
    auxjad.underfull_duration

.. |auxjad| replace:: :mod:`auxjad`
.. _auxjad: index.html
.. |utilities| replace:: :mod:`utilities <auxjad.utilities>`
.. _utilities: api-utilities.html

.. include:: abjad-targets.rst
