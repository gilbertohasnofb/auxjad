from typing import Optional, Union

import abjad

from .mutations.auto_rewrite_meter import auto_rewrite_meter
from .mutations.close_container import close_container
from .mutations.enforce_time_signature import enforce_time_signature
from .mutations.extract_trivial_tuplets import extract_trivial_tuplets
from .mutations.fill_with_rests import fill_with_rests
from .mutations.merge_partial_tuplets import merge_partial_tuplets
from .mutations.prettify_rewrite_meter import prettify_rewrite_meter
from .mutations.remove_repeated_dynamics import remove_repeated_dynamics
from .mutations.remove_repeated_time_signatures import (
    remove_repeated_time_signatures,
)
from .mutations.reposition_clefs import reposition_clefs
from .mutations.reposition_dynamics import reposition_dynamics
from .mutations.reposition_slurs import reposition_slurs
from .mutations.respell_accidentals import respell_accidentals
from .mutations.rests_to_multimeasure_rest import rests_to_multimeasure_rest
from .mutations.sustain_notes import sustain_notes
from .mutations.sync_containers import sync_containers


class Mutation:
    r"""Mutation class containing all of Auxjad's mutation methods.

    Example:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> auxjad.mutate(staff[2:])
        Mutation(client=Selection([Note("d'4"), Note("f'4")]))

    .. note::

        Auxjad automatically adds all methods of :class:`Mutation` as
        extension methods to |abjad.mutate()|. Therefore they can be used from
        either :func:`auxjad.mutate()` or |abjad.mutate()|, as shown below:

        >>> staff1 = abjad.Staff(r"c'4\p d'4\p e'4 f'4\ff")
        >>> auxjad.mutate(staff1[:]).remove_repeated_dynamics()
        >>> staff2 = abjad.Staff(r"c'4\p d'4\p e'4 f'4\ff")
        >>> abjad.mutate(staff2[:]).remove_repeated_dynamics()
        >>> abjad.inspect([staff1[:], staff2[:]]).selections_are_equal()
        True
    """

    ### CLASS VARIABLES ###

    __slots__ = ('_client',)

    ### INITIALISER ###

    def __init__(self, client=None):
        r'Initialises self.'
        self._client = client

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        r'Gets interpreter representation.'
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC METHODS ###

    def auto_rewrite_meter(self,
                           meter_list: list = None,
                           *,
                           prettify_rewrite_meter: bool = True,
                           extract_trivial_tuplets: bool = True,
                           fuse_across_groups_of_beats: bool = True,
                           fuse_quadruple_meter: bool = True,
                           fuse_triple_meter: bool = True,
                           boundary_depth: Optional[int] = None,
                           maximum_dot_count: Optional[int] = None,
                           rewrite_tuplets: bool = True,
                           merge_partial_tuplets: bool = True,
                           split_quadruple_meter: bool = True,
                           ):
        auto_rewrite_meter(
            self.client,
            meter_list=meter_list,
            prettify_rewrite_meter=prettify_rewrite_meter,
            extract_trivial_tuplets=extract_trivial_tuplets,
            fuse_across_groups_of_beats=fuse_across_groups_of_beats,
            fuse_quadruple_meter=fuse_quadruple_meter,
            fuse_triple_meter=fuse_triple_meter,
            boundary_depth=boundary_depth,
            maximum_dot_count=maximum_dot_count,
            rewrite_tuplets=rewrite_tuplets,
            merge_partial_tuplets=merge_partial_tuplets,
            split_quadruple_meter=split_quadruple_meter,
        )

    def close_container(self):
        close_container(self.client)

    def enforce_time_signature(self,
                               time_signatures: Union[abjad.TimeSignature,
                                                      tuple,
                                                      list,
                                                      ],
                               *,
                               cyclic: bool = False,
                               fill_with_rests: bool = True,
                               close_container: bool = False,
                               disable_rewrite_meter: bool = False,
                               prettify_rewrite_meter: bool = True,
                               boundary_depth: Optional[int] = None,
                               maximum_dot_count: Optional[int] = None,
                               rewrite_tuplets: bool = True,
                               extract_trivial_tuplets: bool = True,
                               fuse_across_groups_of_beats: bool = True,
                               fuse_quadruple_meter: bool = True,
                               fuse_triple_meter: bool = True,
                               split_quadruple_meter: bool = True,
                               ):
        enforce_time_signature(
            self.client,
            time_signatures=time_signatures,
            cyclic=cyclic,
            fill_with_rests=fill_with_rests,
            close_container=close_container,
            disable_rewrite_meter=disable_rewrite_meter,
            prettify_rewrite_meter=prettify_rewrite_meter,
            boundary_depth=boundary_depth,
            maximum_dot_count=maximum_dot_count,
            rewrite_tuplets=rewrite_tuplets,
            extract_trivial_tuplets=extract_trivial_tuplets,
            fuse_across_groups_of_beats=fuse_across_groups_of_beats,
            fuse_quadruple_meter=fuse_quadruple_meter,
            fuse_triple_meter=fuse_triple_meter,
            split_quadruple_meter=split_quadruple_meter,
        )

    def extract_trivial_tuplets(self):
        extract_trivial_tuplets(self._client)

    def fill_with_rests(self,
                        *,
                        disable_rewrite_meter: bool = False,
                        prettify_rewrite_meter: bool = True,
                        boundary_depth: Optional[int] = None,
                        maximum_dot_count: Optional[int] = None,
                        rewrite_tuplets: bool = True,
                        extract_trivial_tuplets: bool = True,
                        fuse_across_groups_of_beats: bool = True,
                        fuse_quadruple_meter: bool = True,
                        fuse_triple_meter: bool = True,
                        split_quadruple_meter: bool = True,
                        ):
        fill_with_rests(
            self.client,
            disable_rewrite_meter=disable_rewrite_meter,
            prettify_rewrite_meter=prettify_rewrite_meter,
            boundary_depth=boundary_depth,
            maximum_dot_count=maximum_dot_count,
            rewrite_tuplets=rewrite_tuplets,
            extract_trivial_tuplets=extract_trivial_tuplets,
            fuse_across_groups_of_beats=fuse_across_groups_of_beats,
            fuse_quadruple_meter=fuse_quadruple_meter,
            fuse_triple_meter=fuse_triple_meter,
            split_quadruple_meter=split_quadruple_meter,
        )

    def merge_partial_tuplets(self,
                              *,
                              merge_across_barlines: bool = False,
                              ):
        merge_partial_tuplets(self._client,
                              merge_across_barlines=merge_across_barlines,
                              )

    def prettify_rewrite_meter(self,
                               meter: Union[abjad.Meter, abjad.TimeSignature],
                               *,
                               fuse_across_groups_of_beats: bool = True,
                               fuse_quadruple_meter: bool = True,
                               fuse_triple_meter: bool = True,
                               extract_trivial_tuplets: bool = True,
                               split_quadruple_meter: bool = True,
                               ):
        prettify_rewrite_meter(
            self._client,
            meter=meter,
            fuse_across_groups_of_beats=fuse_across_groups_of_beats,
            fuse_quadruple_meter=fuse_quadruple_meter,
            fuse_triple_meter=fuse_triple_meter,
            extract_trivial_tuplets=extract_trivial_tuplets,
            split_quadruple_meter=split_quadruple_meter,
        )

    def remove_repeated_dynamics(self,
                                 *,
                                 ignore_hairpins: bool = False,
                                 reset_after_rests: bool = False,
                                 ):
        remove_repeated_dynamics(
            self._client,
            ignore_hairpins=ignore_hairpins,
            reset_after_rests=reset_after_rests,
        )

    def remove_repeated_time_signatures(self):
        remove_repeated_time_signatures(self._client)

    def reposition_clefs(self,
                         *,
                         shift_clef_to_notes: bool = True,
                         implicit_clef: abjad.Clef = abjad.Clef('treble'),
                         ):
        reposition_clefs(self._client,
                         shift_clef_to_notes=shift_clef_to_notes,
                         implicit_clef=implicit_clef,
                         )

    def reposition_dynamics(self,
                            *,
                            allow_hairpins_under_rests: bool = False,
                            check_hairpin_trends: bool = True,
                            remove_repeated_dynamics: bool = True,
                            allow_hairpin_to_rest_with_dynamic: bool = True,
                            ):
        allow_hairpin_to_rest_with_dyn = allow_hairpin_to_rest_with_dynamic
        reposition_dynamics(
            self._client,
            allow_hairpins_under_rests=allow_hairpins_under_rests,
            check_hairpin_trends=check_hairpin_trends,
            remove_repeated_dynamics=remove_repeated_dynamics,
            allow_hairpin_to_rest_with_dynamic=allow_hairpin_to_rest_with_dyn,
        )

    def reposition_slurs(self,
                         *,
                         allow_slurs_under_rests: bool = False,
                         close_unterminated_final_slur: bool = True,
                         ):
        reposition_slurs(
            self._client,
            allow_slurs_under_rests=allow_slurs_under_rests,
            close_unterminated_final_slur=close_unterminated_final_slur,
        )

    def respell_accidentals(self,
                            *,
                            include_multiples: bool = False,
                            respell_by_pitch_class: bool = False,
                            ):
        respell_accidentals(
            self._client,
            include_multiples=include_multiples,
            respell_by_pitch_class=respell_by_pitch_class,
        )

    def rests_to_multimeasure_rest(self):
        rests_to_multimeasure_rest(self._client)

    def sustain_notes(self):
        sustain_notes(self.client)

    def sync_containers(self,
                        *,
                        use_multimeasure_rests: bool = True,
                        adjust_last_time_signature: bool = True,
                        ):
        sync_containers(
            self._client,
            use_multimeasure_rests=use_multimeasure_rests,
            adjust_last_time_signature=adjust_last_time_signature,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'Gets client. Returns selection or component.'
        return self._client


### METHOD DOCSTRINGS ###

Mutation.auto_rewrite_meter.__doc__ = auto_rewrite_meter.__doc__
Mutation.close_container.__doc__ = close_container.__doc__
Mutation.enforce_time_signature.__doc__ = enforce_time_signature.__doc__
Mutation.extract_trivial_tuplets.__doc__ = extract_trivial_tuplets.__doc__
Mutation.fill_with_rests.__doc__ = fill_with_rests.__doc__
Mutation.merge_partial_tuplets.__doc__ = merge_partial_tuplets.__doc__
Mutation.prettify_rewrite_meter.__doc__ = prettify_rewrite_meter.__doc__
Mutation.remove_repeated_dynamics.__doc__ = remove_repeated_dynamics.__doc__
Mutation.remove_repeated_time_signatures.__doc__ = (
    remove_repeated_time_signatures.__doc__
)
Mutation.reposition_clefs.__doc__ = reposition_clefs.__doc__
Mutation.reposition_dynamics.__doc__ = reposition_dynamics.__doc__
Mutation.reposition_slurs.__doc__ = reposition_slurs.__doc__
Mutation.respell_accidentals.__doc__ = respell_accidentals.__doc__
Mutation.rests_to_multimeasure_rest.__doc__ = (
    rests_to_multimeasure_rest.__doc__
)
Mutation.sustain_notes.__doc__ = sustain_notes.__doc__
Mutation.sync_containers.__doc__ = sync_containers.__doc__


### FUNCTIONS ###

def mutate(client):
    r"""Makes a mutation agent. See :class:`Mutation` for the documentation
    of all of its methods.

    Example:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> auxjad.mutate(staff[2:])
        Mutation(client=Selection([Note("d'4"), Note("f'4")]))

    .. note::

        Auxjad automatically adds all methods of :class:`Mutation` as
        extension methods to |abjad.mutate()|. Therefore they can be used from
        either :func:`auxjad.mutate()` or |abjad.mutate()|, as shown below:

        >>> staff1 = abjad.Staff(r"c'4\p d'4\p e'4 f'4\ff")
        >>> auxjad.mutate(staff1[:]).remove_repeated_dynamics()
        >>> staff2 = abjad.Staff(r"c'4\p d'4\p e'4 f'4\ff")
        >>> abjad.mutate(staff2[:]).remove_repeated_dynamics()
        >>> abjad.inspect([staff1[:], staff2[:]]).selections_are_equal()
        True
    """
    return Mutation(client)


### EXTENSION METHODS ###

abjad.Mutation.auto_rewrite_meter = Mutation.auto_rewrite_meter
abjad.Mutation.close_container = Mutation.close_container
abjad.Mutation.enforce_time_signature = Mutation.enforce_time_signature
abjad.Mutation.extract_trivial_tuplets = Mutation.extract_trivial_tuplets
abjad.Mutation.fill_with_rests = Mutation.fill_with_rests
abjad.Mutation.merge_partial_tuplets = Mutation.merge_partial_tuplets
abjad.Mutation.prettify_rewrite_meter = Mutation.prettify_rewrite_meter
abjad.Mutation.remove_repeated_dynamics = Mutation.remove_repeated_dynamics
abjad.Mutation.remove_repeated_time_signatures = (
    Mutation.remove_repeated_time_signatures
)
abjad.Mutation.reposition_clefs = Mutation.reposition_clefs
abjad.Mutation.reposition_dynamics = Mutation.reposition_dynamics
abjad.Mutation.reposition_slurs = Mutation.reposition_slurs
abjad.Mutation.respell_accidentals = Mutation.respell_accidentals
abjad.Mutation.rests_to_multimeasure_rest = Mutation.rests_to_multimeasure_rest
abjad.Mutation.sustain_notes = Mutation.sustain_notes
abjad.Mutation.sync_containers = Mutation.sync_containers
