mutate
========

The |mutate|_ subpackage contains mutation functions. Mutations act on an
input |abjad.Selection|, |abjad.Container|, or |abjad.Leaf| (depending on the
function), transforming the input in place, having no return value. Auxjad
automatically adds them as extension functions to |abjad.mutate|.

.. note::

    All mutation functions are also added as extension functions to
    |abjad.mutate|, so it is possible to simply use |abjad.mutate| instead of
    :mod:`auxjad.mutate`:

    >>> import abjad
    >>> import auxjad
    >>> abjad.mutate.rests_to_multimeasure_rest(container[:])

Below is the full list of functions included in |mutate|_. Click on their
names for their individual documentation.

.. currentmodule:: auxjad

.. autosummary::
    :toctree: functions

   mutate.auto_rewrite_meter
   mutate.close_container
   mutate.double_barlines_before_time_signatures
   mutate.enforce_time_signature
   mutate.extract_trivial_tuplets
   mutate.fill_with_rests
   mutate.merge_partial_tuplets
   mutate.prettify_rewrite_meter
   mutate.remove_repeated_dynamics
   mutate.remove_repeated_time_signatures
   mutate.reposition_clefs
   mutate.reposition_dynamics
   mutate.reposition_slurs
   mutate.respell_accidentals
   mutate.rests_to_multimeasure_rest
   mutate.sustain_notes
   mutate.sync_containers

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
