utilities
=========

The |utilities|_ subpackage contains mutation and inspection methods. Mutations
and inspections act on an input |abjad.Selection|, |abjad.Container|, or
|abjad.Leaf| (depending on the function). Mutations transform the input in
place, having no return value. Inspections do not alter the input and return a
value (normally a :obj:`bool`). Auxjad automatically adds them as extension
methods to |abjad.mutate()| and |abjad.inspect()|, respectivelly.

.. note::

    These functions are imported directly into the |auxjad|_ namespace.
    Therefore, to use a function such as
    |auxjad.inspect().selection_is_full()| you only need to import
    |auxjad|_ and invoke the function from its namespace.

    >>> import auxjad
    >>> auxjad.mutate(container[:]).rests_to_multimeasure_rest()
    >>> auxjad.inspect(container[:]).selection_is_full()
    True

    All mutation and inspection functions are also added as extension methods
    to |abjad.mutate()| and |abjad.inspect()|, so it is possible to simply use
    |abjad.mutate()| and |abjad.inspect()| instead of :func:`auxjad.mutate()`
    and :func:`auxjad.inspect()`:

    >>> import abjad
    >>> import auxjad
    >>> abjad.mutate(container[:]).rests_to_multimeasure_rest()
    >>> abjad.inspect(container[:]).selection_is_full()
    True

Below is the full list of functions included in |utilities|_. Click on their
names for their individual documentation. :class:`auxjad.Inspection` and
:class:`auxjad.Mutation` will contain the documentaion of all of their methods.

.. currentmodule:: auxjad

.. autosummary::
    :toctree: ../_api_members

    inspect
    Inspection
    mutate
    Mutation

The full list of individual inspections and mutations added as extension
methods by |auxjad|_ can be found in the table below. Click on their names for
to navigate to their documentation (these are all documented in the two
documentation pages of :class:`auxjad.Inspection` and :class:`auxjad.Mutation`)

.. autosummary::

   Inspection.extract_time_signatures
   Inspection.leaves_are_tieable
   Inspection.selection_is_full
   Inspection.selections_are_identical
   Inspection.underfull_duration
   Mutation.auto_rewrite_meter
   Mutation.close_container
   Mutation.double_barlines_before_time_signatures
   Mutation.enforce_time_signature
   Mutation.extract_trivial_tuplets
   Mutation.fill_with_rests
   Mutation.merge_partial_tuplets
   Mutation.prettify_rewrite_meter
   Mutation.remove_repeated_dynamics
   Mutation.remove_repeated_time_signatures
   Mutation.reposition_clefs
   Mutation.reposition_dynamics
   Mutation.reposition_slurs
   Mutation.respell_accidentals
   Mutation.rests_to_multimeasure_rest
   Mutation.sustain_notes
   Mutation.sync_containers

.. include:: abjad-targets.rst
.. include:: auxjad-targets.rst
