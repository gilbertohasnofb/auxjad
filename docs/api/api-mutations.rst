mutations
=========

The |mutations|_ subpackage contains functions that mutate an input in place
and have no return value. Auxjad automatically adds them as extension methods
to |abjad.mutate()|.

..  note::

    These functions are imported directly into the |auxjad|_ namespace.
    Therefore, to use a function such as
    |auxjad.mutate().rests_to_multimeasure_rest()| you only need to import
    |auxjad|_ and invoke the function from its namespace:

    >>> import auxjad
    >>> auxjad.mutate(container[:]).rests_to_multimeasure_rest()

    Alternatively, these functions are added as extension methods to
    |abjad.mutate()| too:

    >>> abjad.mutate(container[:]).rests_to_multimeasure_rest()

Below is the full list of functions included in |mutations|_. Click on their
names for their individual documentation.

.. autosummary::
    :toctree: ../_api_members

    auxjad.mutate
    auxjad.Mutation
    auxjad.Mutation.auto_rewrite_meter
    auxjad.Mutation.close_container
    auxjad.Mutation.enforce_time_signature
    auxjad.Mutation.extract_trivial_tuplets
    auxjad.Mutation.fill_with_rests
    auxjad.Mutation.prettify_rewrite_meter
    auxjad.Mutation.remove_repeated_dynamics
    auxjad.Mutation.remove_repeated_time_signatures
    auxjad.Mutation.reposition_clefs
    auxjad.Mutation.reposition_dynamics
    auxjad.Mutation.reposition_slurs
    auxjad.Mutation.respell_accidentals
    auxjad.Mutation.rests_to_multimeasure_rest
    auxjad.Mutation.sustain_notes
    auxjad.Mutation.sync_containers

.. |auxjad| replace:: :mod:`auxjad`
.. _auxjad: index.html
.. |mutations| replace:: :mod:`mutations <auxjad.mutations>`
.. _mutations: api-mutations.html

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
