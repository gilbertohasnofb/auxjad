mutate
======

The |mutate|_ subpackage contains mutation functions. Mutations act on an
input |abjad.Selection|, |abjad.Container|, or |abjad.Leaf| (depending on the
function), transforming the input in place, having no return value. Auxjad
automatically adds them as extension functions to |abjad.mutate|.

..  note::

    All mutation functions are also added as extension functions to
    |abjad.mutate|, so it is possible to simply use |abjad.mutate| instead of
    |auxjad.mutate|_:

    >>> import abjad
    >>> import auxjad
    >>> abjad.mutate.rests_to_multimeasure_rest(container[:])

Below is the full list of functions included in |mutate|_. Click on their
names for their individual documentation.

.. currentmodule:: auxjad.mutate

.. autosummary::
    :toctree: ../_api_members

    auto_rewrite_meter
    close_container
    enforce_time_signature
    extend_notes
    extract_trivial_tuplets
    fill_with_rests
    merge_hairpins
    merge_partial_tuplets
    prettify_rewrite_meter
    remove_repeated_dynamics
    remove_repeated_time_signatures
    reposition_clefs
    reposition_dynamics
    reposition_slurs
    respell_augmented_unisons
    rests_to_multimeasure_rest
    sustain_notes
    sync_containers

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
