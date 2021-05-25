utilities
=========

The |utilities|_ subpackage contains mutation and getter functions. Mutations
and getters act on an input |abjad.Selection|, |abjad.Container|, or
|abjad.Leaf| (depending on the function). Mutations transform the input in
place, having no return value. Inspections do not alter the input and return a
value (normally a :obj:`bool`). Auxjad automatically adds them as extension
functions to |abjad.mutate| and |abjad.get|, respectivelly.

.. note::

    These functions are imported directly into the |auxjad|_ namespace.
    Therefore, to use a function such as
    |auxjad.get.selection_is_full()| you only need to import
    |auxjad|_ and invoke the function from its namespace.

    >>> import auxjad
    >>> auxjad.mutate.rests_to_multimeasure_rest(container[:])
    >>> auxjad.get.selection_is_full(container[:])
    True

    All mutation and getter functions are also added as extension methods
    to |abjad.mutate| and |abjad.get|, so it is possible to simply use
    |abjad.mutate| and |abjad.get| instead of :mod:`auxjad.mutate`
    and :mod:`auxjad.get`:

    >>> import abjad
    >>> import auxjad
    >>> abjad.mutate.rests_to_multimeasure_rest(container[:])
    >>> abjad.get.selection_is_full(container[:])
    True

Below is the full list of functions included in |utilities|_. Click on their
names for their individual documentation. :class:`auxjad.Inspection` and
:class:`auxjad.Mutation` will contain the documentaion of all of their methods.

.. currentmodule:: auxjad

.. autosummary::
    :toctree: ../_api_members

    get
    mutate

The full list of individual getters and mutations added as extension functions
by |auxjad|_ can be found in the table below.

.. autosummary::

   get.extract_time_signatures
   get.leaves_are_tieable
   get.selection_is_full
   get.selections_are_identical
   get.underfull_duration
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
