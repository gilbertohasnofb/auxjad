from typing import Union

import abjad

from .prettify_rewrite_meter import prettify_rewrite_meter
from .remove_empty_tuplets import remove_empty_tuplets
from .remove_repeated_dynamics import remove_repeated_dynamics
from .remove_repeated_time_signatures import remove_repeated_time_signatures
from .reposition_clefs import reposition_clefs
from .reposition_dynamics import reposition_dynamics
from .reposition_slurs import reposition_slurs
from .respell_accidentals import respell_accidentals
from .rests_to_multimeasure_rest import rests_to_multimeasure_rest


class Mutation:
    r"""Mutation class containing all of Auxjad's mutation methods.

    Example:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> auxjad.mutate(staff[2:])
        Mutation(client=Selection([Note("d'4"), Note("f'4")]))
    """

    ### CLASS VARIABLES ###

    __slots__ = ('_client',)

    ### INITIALISER ###

    def __init__(self, client=None):
        self._client = client

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        r'Gets interpreter representation.'
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC METHODS ###

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

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        r'Gets client. Returns selection or component.'
        return self._client


### METHOD DOCSTRINGS ###

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


### FUNCTIONS ###


def mutate(client):
    r"""Makes a mutation agent. See :class:`Mutation` for the documentation
    of all of its methods.

    Example:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> auxjad.mutate(staff[2:])
        Mutation(client=Selection([Note("d'4"), Note("f'4")]))

    Using |abjad.mutate()|:
        All of the methods in :class:`auxjad.Mutation` are automatically added
        as aextension methods to |abjad.mutate()|. Example:

        >>> staff = abjad.Staff(r"c'4\pp e'4\pp d'4\f f'4")
        >>> abjad.mutate(staff[:]).remove_repeated_dynamics()
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \pp
            e'4
            d'4
            \f
            f'4
        }

        .. figure:: ../_images/image-mutate-1.png
    """
    return Mutation(client)
