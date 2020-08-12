from typing import Optional, Union

import abjad

from .close_container import close_container
from .enforce_time_signature import enforce_time_signature
from .fill_with_rests import fill_with_rests
from .prettify_rewrite_meter import prettify_rewrite_meter
from .remove_empty_tuplets import remove_empty_tuplets
from .remove_repeated_dynamics import remove_repeated_dynamics
from .remove_repeated_time_signatures import remove_repeated_time_signatures
from .reposition_clefs import reposition_clefs
from .reposition_dynamics import reposition_dynamics
from .reposition_slurs import reposition_slurs
from .respell_accidentals import respell_accidentals
from .rests_to_multimeasure_rest import rests_to_multimeasure_rest
from .sync_containers import sync_containers


class Mutation:
    r"""Mutation class containing all of Auxjad's mutation methods.

    Example:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> auxjad.mutate(staff[2:])
        Mutation(client=Selection([Note("d'4"), Note("f'4")]))

    ..  note::

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

    def close_container(self):
        return close_container(self.client)

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
                               boundary_depth: Optional[int] = None,
                               maximum_dot_count: Optional[int] = None,
                               rewrite_tuplets: bool = True,
                               ):
        return enforce_time_signature(
            self.client,
            time_signatures=time_signatures,
            cyclic=cyclic,
            fill_with_rests=fill_with_rests,
            close_container=close_container,
            disable_rewrite_meter=disable_rewrite_meter,
            boundary_depth=boundary_depth,
            maximum_dot_count=maximum_dot_count,
            rewrite_tuplets=rewrite_tuplets,
        )

    def fill_with_rests(self,
                        *,
                        disable_rewrite_meter: bool = False,
                        ):
        return fill_with_rests(
            self.client,
            disable_rewrite_meter=disable_rewrite_meter,
        )

    def prettify_rewrite_meter(self,
                               meter: Union[abjad.Meter, abjad.TimeSignature],
                               *,
                               fuse_across_groups_of_beats: bool = True,
                               fuse_quadruple_meter: bool = True,
                               fuse_triple_meter: bool = True,
                               ):
        return prettify_rewrite_meter(
            self._client,
            meter=meter,
            fuse_across_groups_of_beats=fuse_across_groups_of_beats,
            fuse_quadruple_meter=fuse_quadruple_meter,
            fuse_triple_meter=fuse_triple_meter,
        )

    def remove_empty_tuplets(self):
        return remove_empty_tuplets(self._client)

    def remove_repeated_dynamics(self,
                                 *,
                                 ignore_hairpins: bool = False,
                                 reset_after_rests: bool = False,
                                 ):
        return remove_repeated_dynamics(
            self._client,
            ignore_hairpins=ignore_hairpins,
            reset_after_rests=reset_after_rests,
        )

    def remove_repeated_time_signatures(self):
        return remove_repeated_time_signatures(self._client)

    def reposition_clefs(self,
                         *,
                         shift_clef_to_notes: bool = True,
                         implicit_clef: abjad.Clef = abjad.Clef('treble'),
                         ):
        return reposition_clefs(self._client,
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
        return reposition_dynamics(
            self._client,
            allow_hairpins_under_rests=allow_hairpins_under_rests,
            check_hairpin_trends=check_hairpin_trends,
            remove_repeated_dynamics=remove_repeated_dynamics,
            allow_hairpin_to_rest_with_dynamic=(
                allow_hairpin_to_rest_with_dynamic
            ),
        )

    def reposition_slurs(self,
                         *,
                         allow_slurs_under_rests: bool = False,
                         remove_unterminated_slurs: bool = True,
                         ):
        return reposition_slurs(
            self._client,
            allow_slurs_under_rests=allow_slurs_under_rests,
            remove_unterminated_slurs=remove_unterminated_slurs,
        )

    def respell_accidentals(self,
                            *,
                            include_multiples: bool = False,
                            respell_by_pitch_class: bool = False,
                            ):
        return respell_accidentals(
            self._client,
            include_multiples=include_multiples,
            respell_by_pitch_class=respell_by_pitch_class,
        )

    def rests_to_multimeasure_rest(self):
        return rests_to_multimeasure_rest(self._client)

    def sync_containers(self,
                        *,
                        use_multimeasure_rests: bool = True,
                        adjust_last_time_signature: bool = True,
                        ):
        return sync_containers(
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

Mutation.close_container.__doc__ = close_container.__doc__
Mutation.enforce_time_signature.__doc__ = enforce_time_signature.__doc__
Mutation.fill_with_rests.__doc__ = fill_with_rests.__doc__
Mutation.prettify_rewrite_meter.__doc__ = prettify_rewrite_meter.__doc__
Mutation.remove_empty_tuplets.__doc__ = remove_empty_tuplets.__doc__
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
Mutation.sync_containers.__doc__ = sync_containers.__doc__


### FUNCTIONS ###

def mutate(client):
    r"""Makes a mutation agent. See :class:`Mutation` for the documentation
    of all of its methods.

    Example:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> auxjad.mutate(staff[2:])
        Mutation(client=Selection([Note("d'4"), Note("f'4")]))

    ..  note::

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

def _close_container(self):
    close_container(self.client)


def _enforce_time_signature(self,
                            time_signatures: Union[abjad.TimeSignature,
                                                   tuple,
                                                   list,
                                                   ],
                            *,
                            cyclic: bool = False,
                            fill_with_rests: bool = True,
                            close_container: bool = False,
                            disable_rewrite_meter: bool = False,
                            boundary_depth: Optional[int] = None,
                            maximum_dot_count: Optional[int] = None,
                            rewrite_tuplets: bool = True,
                            ):
    enforce_time_signature(self.client,
                           time_signatures=time_signatures,
                           cyclic=cyclic,
                           fill_with_rests=fill_with_rests,
                           close_container=close_container,
                           disable_rewrite_meter=disable_rewrite_meter,
                           boundary_depth=boundary_depth,
                           maximum_dot_count=maximum_dot_count,
                           rewrite_tuplets=rewrite_tuplets,
                           )


def _fill_with_rests(self,
                     *,
                     disable_rewrite_meter: bool = False,
                     ):
    fill_with_rests(self.client,
                    disable_rewrite_meter=disable_rewrite_meter,
                    )


def _prettify_rewrite_meter(self,
                            meter,
                            *,
                            fuse_across_groups_of_beats: bool = True,
                            fuse_quadruple_meter: bool = True,
                            fuse_triple_meter: bool = True,
                            ):
    prettify_rewrite_meter(
        self._client,
        meter,
        fuse_across_groups_of_beats=fuse_across_groups_of_beats,
        fuse_quadruple_meter=fuse_quadruple_meter,
        fuse_triple_meter=fuse_triple_meter,
    )


def _remove_empty_tuplets(self):
    remove_empty_tuplets(self._client)


def _remove_repeated_dynamics(self,
                              *,
                              ignore_hairpins: bool = False,
                              reset_after_rests: bool = False,
                              ):
    remove_repeated_dynamics(self._client,
                             ignore_hairpins=ignore_hairpins,
                             reset_after_rests=reset_after_rests,
                             )


def _remove_repeated_time_signatures(self):
    remove_repeated_time_signatures(self._client)


def _reposition_clefs(self,
                      *,
                      shift_clef_to_notes: bool = True,
                      implicit_clef: abjad.Clef = abjad.Clef('treble'),
                      ):
    reposition_clefs(self._client,
                     shift_clef_to_notes=shift_clef_to_notes,
                     implicit_clef=implicit_clef,
                     )


def _reposition_dynamics(
    self,
    *,
    allow_hairpins_under_rests: bool = False,
    check_hairpin_trends: bool = True,
    remove_repeated_dynamics: bool = True,
    allow_hairpin_to_rest_with_dynamic: bool = True,
):
    reposition_dynamics(
        self._client,
        allow_hairpins_under_rests=allow_hairpins_under_rests,
        check_hairpin_trends=check_hairpin_trends,
        remove_repeated_dynamics=remove_repeated_dynamics,
        allow_hairpin_to_rest_with_dynamic=allow_hairpin_to_rest_with_dynamic,
    )


def _reposition_slurs(self,
                      *,
                      allow_slurs_under_rests: bool = False,
                      remove_unterminated_slurs: bool = False,
                      ):
    reposition_slurs(self._client,
                     allow_slurs_under_rests=allow_slurs_under_rests,
                     remove_unterminated_slurs=remove_unterminated_slurs,
                     )


def _respell_accidentals(self,
                         *,
                         include_multiples: bool = False,
                         respell_by_pitch_class: bool = False,
                         ):
    respell_accidentals(self._client,
                        include_multiples=include_multiples,
                        respell_by_pitch_class=respell_by_pitch_class,
                        )


def _rests_to_multimeasure_rest(self):
    rests_to_multimeasure_rest(self._client)


def _sync_containers(self,
                     *,
                     use_multimeasure_rests: bool = True,
                     adjust_last_time_signature: bool = True,
                     ):
    sync_containers(self._client,
                    use_multimeasure_rests=use_multimeasure_rests,
                    adjust_last_time_signature=adjust_last_time_signature,
                    )


abjad.Mutation.close_container = _close_container
abjad.Mutation.enforce_time_signature = _enforce_time_signature
abjad.Mutation.fill_with_rests = _fill_with_rests
abjad.Mutation.prettify_rewrite_meter = _prettify_rewrite_meter
abjad.Mutation.remove_empty_tuplets = _remove_empty_tuplets
abjad.Mutation.remove_repeated_dynamics = _remove_repeated_dynamics
abjad.Mutation.remove_repeated_time_signatures = (
    _remove_repeated_time_signatures
)
abjad.Mutation.reposition_clefs = _reposition_clefs
abjad.Mutation.reposition_dynamics = _reposition_dynamics
abjad.Mutation.reposition_slurs = _reposition_slurs
abjad.Mutation.respell_accidentals = _respell_accidentals
abjad.Mutation.rests_to_multimeasure_rest = _rests_to_multimeasure_rest
abjad.Mutation.sync_containers = _sync_containers
