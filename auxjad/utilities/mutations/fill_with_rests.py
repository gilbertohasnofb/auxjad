from typing import Optional

import abjad

from ..inspect import inspect
from .prettify_rewrite_meter import (
    prettify_rewrite_meter as prettify_rewrite_meter_function,
)


def fill_with_rests(container: abjad.Container,
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
                    ):
    r"""Mutates an input container (of type |abjad.Container| or child class)
    in place and has no return value; this function fills a container with
    rests in order to make it full.

    Basic usage:
        Returns the missing duration of the last measure of any container or
        child class. If no time signature is encountered, it uses LilyPond's
        convention and considers the container as in 4/4.

        >>> container1 = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Container(r"c'4 d'4 e'4")
        >>> container3 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4")
        >>> container4 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4 d'4 e'4 f'4")
        >>> auxjad.mutate(container1).fill_with_rests()
        >>> auxjad.mutate(container2).fill_with_rests()
        >>> auxjad.mutate(container3).fill_with_rests()
        >>> auxjad.mutate(container4).fill_with_rests()
        >>> abjad.f(container1)
        {
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/fill_with_rests-up297scg6t.png

        >>> abjad.f(container2)
        {
            c'4
            d'4
            e'4
            r4
        }

        .. figure:: ../_images/fill_with_rests-azrrw0z0buw.png

        >>> abjad.f(container3)
        {
            c'4
            d'4
            e'4
            f'4
            c'4
            r2.
        }

        .. figure:: ../_images/fill_with_rests-jtyw5ikc0k.png

        >>> abjad.f(container4)
        {
            c'4
            d'4
            e'4
            f'4
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/fill_with_rests-xjkm2vzjfpr.png

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.mutate()|. It can thus be used from either
        :func:`auxjad.mutate()` or |abjad.mutate()|. Therefore, the two lines
        below are equivalent:

        >>> auxjad.mutate(staff).fill_with_rests()
        >>> abjad.mutate(staff).fill_with_rests()

    Time signature changes:
        Handles any time signatures as well as changes of time signature.

        >>> staff1 = abjad.Staff(r"\time 4/4 c'4 d'4 e'4 f'4 g'")
        >>> staff2 = abjad.Staff(r"\time 3/4 a2. \time 2/4 c'4")
        >>> staff3 = abjad.Staff(r"\time 5/4 g1 ~ g4 \time 4/4 af'2")
        >>> auxjad.mutate(staff1).fill_with_rests()
        >>> auxjad.mutate(staff2).fill_with_rests()
        >>> auxjad.mutate(staff3).fill_with_rests()
        >>> abjad.f(staff1)
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
            g'4
            r2.
        }

        .. figure:: ../_images/fill_with_rests-7zydps2jsb.png

        >>> abjad.f(staff2)
        {
            \time 3/4
            a2.
            \time 2/4
            c'4
            r4
        }

        .. figure:: ../_images/fill_with_rests-1lphcrl5pnr.png

        >>> abjad.f(staff3)
        {
            \time 5/4
            g1
            ~
            g4
            \time 4/4
            af'2
            r2
        }

        .. figure:: ../_images/fill_with_rests-e00jvx986r.png

    .. note::

        When using |abjad.Container|'s, all time signatures in the output will
        be commented out with ``%%%.`` This is because Abjad only applies time
        signatures to containers that belong to a |abjad.Staff|. The present
        function works with either |abjad.Container| and |abjad.Staff|.

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
        >>> abjad.f(container)
        {
            %%% \time 3/4 %%%
            c'4
            d'4
            e'4
        }

        .. figure:: ../_images/fill_with_rests-b0qflg50qfn.png

        >>> staff = abjad.Staff([container])
        >>> abjad.f(container)
        {
            \time 3/4
            c'4
            d'4
            e'4
        }

        .. figure:: ../_images/fill_with_rests-qtaswjiecg.png

    Partial time signatures:
        Correctly handles partial time signatures.

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4 g'4")
        >>> time_signature = abjad.TimeSignature((3, 4), partial=(1, 4))
        >>> abjad.attach(time_signature, staff[0])
        >>> auxjad.mutate(staff).fill_with_rests()
        >>> abjad.f(staff)
        {
            \partial 4
            \time 3/4
            c'4
            d'4
            e'4
            f'4
            g'4
            r2
        }

        .. figure:: ../_images/fill_with_rests-9smva9ajdi.png

    ``disable_rewrite_meter``:
        By default, this class applies the |abjad.mutate().rewrite_meter()|
        mutation to the last measure when rests are added.

        >>> staff = abjad.Staff(r"\time 4/4 c'8 d'4 e'4")
        >>> auxjad.mutate(staff).fill_with_rests()
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'8
            d'4
            e'8
            ~
            e'8
            r4.
        }

        .. figure:: ../_images/fill_with_rests-n83nmnfh92c.png

        Call this function with the optional keyword argument
        ``disable_rewrite_meter`` set to ``True`` in order to disable this
        behaviour.

        >>> staff = abjad.Staff(r"\time 4/4 c'8 d'4 e'4")
        >>> auxjad.mutate(staff, disable_rewrite_meter=True).fill_with_rests()
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'8
            d'4
            e'4
            r4.
        }

        .. figure:: ../_images/fill_with_rests-9rg2i4n1vhr.png

    .. note::

        This function also accepts the arguments ``boundary_depth``,
        ``maximum_dot_count``, and ``rewrite_tuplets``, which are passed on to
        |abjad.mutate().rewrite_meter()|, and ``fuse_across_groups_of_beats``,
        ``fuse_quadruple_meter``, ``fuse_triple_meter``, and
        ``extract_trivial_tuplets``, which are passed on to
        |auxjad.mutate().prettify_rewrite_meter()| (the latter can be disabled
        by setting ``prettify_rewrite_meter`` to ``False``). See the
        documentation of those functions for more details on these arguments.

    .. error::

        If a container is malformed, i.e. it has an underfilled measure before
        a time signature change, the function raises a :exc:`ValueError`
        exception.

        >>> container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'4")
        >>> auxjad.mutate(container).fill_with_rests()
        ValueError: 'container' is malformed, with an underfull measure
        preceding a time signature change

    .. warning::

        The input container must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containing
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")
    if not abjad.select(container).leaves().are_contiguous_logical_voice():
        raise ValueError("argument must be contiguous logical voice")
    try:
        if not inspect(container[:]).selection_is_full():
            underfull_rests = abjad.LeafMaker()(
                None,
                inspect(container[:]).underfull_duration(),
            )
            container.extend(underfull_rests)
        else:
            return
    except ValueError as err:
        raise ValueError("'container' is malformed, with an underfull measure "
                         "preceding a time signature change") from err
    if not disable_rewrite_meter:
        time_signatures = inspect(container).time_signature_extractor(
            do_not_use_none=True,
        )
        measures = abjad.select(container[:]).group_by_measure()
        abjad.mutate(measures[-1]).rewrite_meter(
            time_signatures[-1],
            boundary_depth=boundary_depth,
            maximum_dot_count=maximum_dot_count,
            rewrite_tuplets=rewrite_tuplets,
        )
        if prettify_rewrite_meter:
            measures = abjad.select(container[:]).group_by_measure()
            prettify_rewrite_meter_function(
                measures[-1],
                time_signatures[-1],
                extract_trivial_tuplets=extract_trivial_tuplets,
                fuse_across_groups_of_beats=fuse_across_groups_of_beats,
                fuse_quadruple_meter=fuse_quadruple_meter,
                fuse_triple_meter=fuse_triple_meter,
            )
