from typing import Optional

import abjad

from ..inspect import inspect
from .extract_trivial_tuplets import (
    extract_trivial_tuplets as extract_trivial_tuplets_function,
)
from .merge_partial_tuplets import (
    merge_partial_tuplets as merge_partial_tuplets_function,
)
from .prettify_rewrite_meter import (
    prettify_rewrite_meter as prettify_rewrite_meter_function,
)


def auto_rewrite_meter(container: abjad.Container,
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
    r"""Mutates an input container (of type |abjad.Container| or child class)
    in place and has no return value; this function takes every measure of a
    container, detects its time signature, and apply both
    |abjad.mutate().rewrite_meter()| and
    |auxjad.mutate().prettify_rewrite_meter()| to it.

    Basic usage:
        For this example, the following container will be mutated:

        >>> staff = abjad.Staff(r"c'16 d'8 e'16 f'8 g'4 a'4 b'8 "
        ...                     r"c'16 d'4. e'16 f'8 g'4 a'16 b'16")
        >>> abjad.f(staff)
        \new Staff
        {
            c'16
            d'8
            e'16
            f'8
            g'4
            a'4
            b'8
            c'16
            d'4.
            e'16
            f'8
            g'4
            a'16
            b'16
        }

        .. figure:: ../_images/auto_rewrite_meter-xyx2wh7ufer.png

        Abjad's |abjad.mutate().rewrite_meter()| mutates an |abjad.Selection|
        of a measure, improving its notation.

        >>> for measure in abjad.select(staff[:]).group_by_measure():
        ...     abjad.mutate(measure).rewrite_meter(abjad.Meter((4, 4)))
        >>> abjad.f(staff)
        \new Staff
        {
            c'16
            d'16
            ~
            d'16
            e'16
            f'8
            g'8
            ~
            g'8
            a'8
            ~
            a'8
            b'8
            c'16
            d'8.
            ~
            d'8.
            e'16
            f'8
            g'8
            ~
            g'8
            a'16
            b'16
        }

        .. figure:: ../_images/auto_rewrite_meter-7fn2uj2xupb.png

        This function mutates an |abjad.Container| (or child class),
        identifying the implied meters of each measure and applying both
        |abjad.mutate().rewrite_meter()| and
        |auxjad.mutate().prettify_rewrite_meter()| to it. See the documentation
        of the latter for a detailed explanation of what it does.

        Applying |auxjad.mutate().auto_rewrite_meter()| to the same initial
        container shown in the first figure above outputs:

        >>> staff = abjad.Staff(r"c'16 d'8 e'16 f'8 g'4 a'4 b'8 "
        ...                     r"c'16 d'4. e'16 f'8 g'4 a'16 b'16")
        >>> auxjad.mutate(staff).auto_rewrite_meter()
        >>> abjad.f(staff)
        \new Staff
        {
            c'16
            d'8
            e'16
            f'8
            g'8
            ~
            g'8
            a'4
            b'8
            c'16
            d'8.
            ~
            d'8.
            e'16
            f'8
            g'4
            a'16
            b'16
        }

        .. figure:: ../_images/auto_rewrite_meter-ahdaggaiqbc.png

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.mutate()|. It can thus be used from either
        :func:`auxjad.mutate()` or |abjad.mutate()|. Therefore, the two lines
        below are equivalent:

        >>> auxjad.mutate(staff).auto_rewrite_meter()
        >>> abjad.mutate(staff).auto_rewrite_meter()

    Time signature changes:
        It automatically handles time signature changes.

        >>> staff = abjad.Staff(r"c'16 d'8 e'16 f'8 g'4 a'4 b'8 "
        ...                     r"\time 6/8 b'4 c''4 r4 ")
        >>> auxjad.mutate(staff).auto_rewrite_meter()
        >>> abjad.f(staff)
        \new Staff
        {
            c'16
            d'8
            e'16
            f'8
            g'8
            ~
            g'8
            a'4
            b'8
            \time 6/8
            b'4
            c''8
            ~
            c''8
            r4
        }

        .. figure:: ../_images/auto_rewrite_meter-08sckfp19vil.png

    ``prettify_rewrite_meter``:
        By default, this function invokes both |abjad.mutate().rewrite_meter()|
        and |auxjad.mutate().prettify_rewrite_meter()|.

        >>> staff = abjad.Staff(r"c'16 d'8 e'16 f'8 g'4 a'4 b'8 "
        ...                     r"c'16 d'8 e'16 f'8 g'4 a'4 b'8")
        >>> auxjad.mutate(staff).auto_rewrite_meter()
        >>> abjad.f(staff)
        \new Staff
        {
            c'16
            d'8
            e'16
            f'8
            g'8
            ~
            g'8
            a'4
            b'8
            c'16
            d'8
            e'16
            f'8
            g'8
            ~
            g'8
            a'4
            b'8
        }

        .. figure:: ../_images/auto_rewrite_meter-vbytyszlkng.png

        Set ``prettify_rewrite_meter`` to ``False`` to not invoke
        |auxjad.mutate().prettify_rewrite_meter()|.

        >>> staff = abjad.Staff(r"c'16 d'8 e'16 f'8 g'4 a'4 b'8 "
        ...                     r"c'16 d'4. e'16 f'8 g'4 a'16 b'16")
        >>> auxjad.mutate(staff).auto_rewrite_meter(
        ...     prettify_rewrite_meter=False,
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            c'16
            d'16
            ~
            d'16
            e'16
            f'8
            g'8
            ~
            g'8
            a'8
            ~
            a'8
            b'8
            c'16
            d'8.
            ~
            d'8.
            e'16
            f'8
            g'8
            ~
            g'8
            a'16
            b'16
        }

        .. figure:: ../_images/auto_rewrite_meter-64wse58hvko.png

    ``meter_list``:
        When no ``meter_list`` is supplied, this function detects the time
        signature of each measure and uses those when rewritting it:

        >>> staff = abjad.Staff(r"\time 7/4 c'8 d'4 e'4 f'4 g'4 a'4 b'4 c''8 "
        ...                     r"\time 5/4 d''8 e''4 f''4 g''4 a''4 b''8")
        >>> auxjad.mutate(staff).auto_rewrite_meter()
        >>> abjad.f(staff)
        \new Staff
        {
            \time 7/4
            c'8
            d'4
            e'4
            f'8
            ~
            f'8
            g'4
            a'8
            ~
            a'8
            b'4
            c''8
            \time 5/4
            d''8
            e''4
            f''4
            g''8
            ~
            g''8
            a''4
            b''8
        }

        .. figure:: ../_images/auto_rewrite_meter-l4xnpevp3z.png

        To use a custom list of meters (one for each measure), set
        ``meter_list`` to a :obj:`list` of |abjad.Meter|'s or
        |abjad.TimeSignature|'s.

        >>> staff = abjad.Staff(r"\time 7/4 c'8 d'4 e'4 f'4 g'4 a'4 b'4 c''8 "
        ...                     r"\time 5/4 d''8 e''4 f''4 g''4 a''4 b''8")
        >>> meter_list = [abjad.Meter((7, 4), increase_monotonic=True),
        ...               abjad.Meter((5, 4), increase_monotonic=True),
        ...               ]
        >>> auxjad.mutate(staff).auto_rewrite_meter(meter_list=meter_list)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 7/4
            c'8
            d'4
            e'8
            ~
            e'8
            f'4
            g'8
            ~
            g'8
            a'4
            b'4
            c''8
            \time 5/4
            d''8
            e''4
            f''8
            ~
            f''8
            g''4
            a''4
            b''8
        }

        .. figure:: ../_images/auto_rewrite_meter-uqif4i8tqxk.png

    Number of measures:
        This function handles a container with any number of measures and any
        number of time signature changes:

        >>> staff = abjad.Staff(
        ...     r"\time 3/4 c'8 d'4 e'4 f'8 "
        ...     r"\time 5/8 g'4 a'4 r8 "
        ...     r"\time 6/8 b'4 c''4 r4 "
        ...     r"\time 4/4 d''8 e''4 f''8 g''16 a''4 r8."
        ... )
        >>> auxjad.mutate(staff).auto_rewrite_meter()
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'8
            d'4
            e'4
            f'8
            \time 5/8
            g'4
            a'8
            ~
            a'8
            r8
            \time 6/8
            b'4
            c''8
            ~
            c''8
            r4
            \time 4/4
            d''8
            e''4
            f''8
            g''16
            a''8.
            ~
            a''16
            r8.
        }

        .. figure:: ../_images/auto_rewrite_meter-hkhtqnqita.png

    ``extract_trivial_tuplets``:
        By default, tuplets filled with rests or tied notes or chords are
        extracted:

        >>> staff = abjad.Staff(
        ...     r"\times 2/3 {c'4 ~ c'8} \times 2/3 {d'8 r4} "
        ...     r"\times 2/3 {r8 r8 r8} \times 2/3 {<e' g'>8 ~ <e' g'>4}"
        ... )
        >>> auxjad.mutate(staff).auto_rewrite_meter()
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \times 2/3 {
                d'8
                r4
            }
            r4
            <e' g'>4
        }

        .. figure:: ../_images/auto_rewrite_meter-nq6t6qwka7a.png

        Set ``extract_trivial_tuplets`` to ``False`` to disable this behaviour.

        >>> staff = abjad.Staff(
        ...     r"\times 2/3 {c'4 ~ c'8} \times 2/3 {d'8 r4} "
        ...     r"\times 2/3 {r8 r8 r8} \times 2/3 {<e' g'>8 ~ <e' g'>4}"
        ... )
        >>> auxjad.mutate(staff).auto_rewrite_meter(
        ...     extract_trivial_tuplets=False,
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                c'4.
            }
            \times 2/3 {
                d'8
                r4
            }
            \times 2/3 {
                r4.
            }
            \times 2/3 {
                <e' g'>4.
            }
        }

        .. figure:: ../_images/auto_rewrite_meter-ssnsui7o9cc.png

    ``merge_partial_tuplets``:
        By default, consecutive partial tuplets with the same ratio that sum up
        to an assignable duration will be merged together:

        >>> staff = abjad.Staff(r"\times 2/3 {c'2 d'1}"
        ...                     r"\times 2/3 {e'2} \times 2/3 {f'1}"
        ...                     )
        >>> auxjad.mutate(staff).auto_rewrite_meter()
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                c'2
                d'1
            }
            \times 2/3 {
                e'2
                f'1
            }
        }

        .. figure:: ../_images/auto_rewrite_meter-ty72t5wvc1.png

        Set ``merge_partial_tuplets`` to ``False`` to disable this behaviour.

        >>> staff = abjad.Staff(r"\times 2/3 {c'2 d'1}"
        ...                     r"\times 2/3 {e'2} \times 2/3 {f'1}"
        ...                     )
        >>> auxjad.mutate(staff).auto_rewrite_meter(
        ...     merge_partial_tuplets=False,
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                c'2
                d'1
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                e'2
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                f'1
            }
        }

        .. figure:: ../_images/auto_rewrite_meter-4rouf819bjb.png

    .. note::

        This function also accepts the arguments ``boundary_depth``,
        ``maximum_dot_count``, and ``rewrite_tuplets``, which are passed on to
        |abjad.mutate().rewrite_meter()|, and ``fuse_across_groups_of_beats``,
        ``fuse_quadruple_meter``, ``fuse_triple_meter``, and
        ``split_quadruple_meter``, which are passed on to
        |auxjad.mutate().prettify_rewrite_meter()|. ``merge_partial_tuplets``
        is used to invoke |auxjad.mutate().merge_partial_tuplets()| See the
        documentation of these functions for more details on these arguments.

    .. warning::

        Setting ``boundary_depth`` to a value equal to or larger than ``1``
        will automatically disable ``fuse_across_groups_of_beats``,
        ``fuse_quadruple_meter``, and ``fuse_triple_meter``, regardless of
        their values. This is because when any of those arguments is ``True``,
        |auxjad.mutate().prettify_rewrite_meter()| will fuse across beats,
        which goes against the purpose of using ``boundary_depth``. Compare the
        results below. In the first case, simply applying
        |auxjad.mutate().prettify_rewrite_meter()| with no arguments results in
        some logical ties being tied across beats.

        >>> staff = abjad.Staff(r"\time 4/4 c'4. d'4. e'4 f'8 g'4 a'4 b'4.")
        >>> meter = abjad.Meter((4, 4))
        >>> for measure in abjad.select(staff[:]).group_by_measure():
        ...     abjad.mutate(measure).rewrite_meter(meter, boundary_depth=1)
        >>> for measure in abjad.select(staff[:]).group_by_measure():
        ...     auxjad.mutate(measure).prettify_rewrite_meter(meter)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'4
            ~
            c'8
            d'8
            ~
            d'4
            e'4
            f'8
            g'4
            a'8
            ~
            a'8
            b'8
            ~
            b'4
        }

        .. figure:: ../_images/auto_rewrite_meter-cf09ysj16fo.png

        By automatically setting all ``fuse_across_groups_of_beats``,
        ``fuse_quadruple_meter``, and  ``fuse_triple_meter` to ``False`` when
        ``boundary_depth`` is equal to or larger than ``1``, this function will
        not fuse those leaves against the required boundary depth.

        >>> staff = abjad.Staff(r"\time 4/4 c'4. d'4. e'4 f'8 g'4 a'4 b'4.")
        >>> auxjad.mutate(staff).auto_rewrite_meter(boundary_depth=1)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'4
            ~
            c'8
            d'8
            ~
            d'4
            e'4
            f'8
            g'8
            ~
            g'8
            a'8
            ~
            a'8
            b'8
            ~
            b'4
        }

        .. figure:: ../_images/auto_rewrite_meter-mm9xvmaqwfj.png
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("first positional argument must be 'abjad.Container' "
                        "or child class")
    if meter_list is not None:
        if not isinstance(meter_list, list):
            raise TypeError("'meter_list' must be a 'list' of 'abjad.Meter' "
                            "or 'abjad.TimeSignature'")
        else:
            for meter in meter_list:
                if not isinstance(meter, (abjad.Meter, abjad.TimeSignature)):
                    raise TypeError("elements of 'meter_list' must be "
                                    "'abjad.Meter' or 'abjad.TimeSignature'")
                if isinstance(meter, abjad.TimeSignature):
                    meter = abjad.Meter(meter.pair)
    if not isinstance(prettify_rewrite_meter, bool):
        raise TypeError("'prettify_rewrite_meter' must be 'bool'")
    if not isinstance(fuse_across_groups_of_beats, bool):
        raise TypeError("'fuse_across_groups_of_beats' must be 'bool'")
    if not isinstance(fuse_quadruple_meter, bool):
        raise TypeError("'fuse_quadruple_meter' must be 'bool'")
    if not isinstance(fuse_triple_meter, bool):
        raise TypeError("'fuse_triple_meter' must be 'bool'")
    if boundary_depth is not None:
        if not isinstance(boundary_depth, int):
            raise TypeError("'boundary_depth' must be 'int'")
    if maximum_dot_count is not None:
        if not isinstance(maximum_dot_count, int):
            raise TypeError("'maximum_dot_count' must be 'int'")
    if not isinstance(rewrite_tuplets, bool):
        raise TypeError("'rewrite_tuplets' must be 'bool'")
    if not isinstance(merge_partial_tuplets, bool):
        raise TypeError("'merge_partial_tuplets' must be 'bool'")
    if not isinstance(split_quadruple_meter, bool):
        raise TypeError("'split_quadruple_meter' must be 'bool'")

    if extract_trivial_tuplets:
        extract_trivial_tuplets_function(container[:])
    if merge_partial_tuplets:
        merge_partial_tuplets_function(container[:])
        if extract_trivial_tuplets:
            extract_trivial_tuplets_function(abjad.select(container))

    if meter_list is None:
        time_signatures = inspect(container).time_signature_extractor(
            do_not_use_none=True,
        )
        meter_list = [abjad.Meter(ts.pair) for ts in time_signatures]
    measures = abjad.select(container[:]).group_by_measure()
    for meter, measure in zip(meter_list, measures):
        abjad.mutate(measure).rewrite_meter(
            meter,
            boundary_depth=boundary_depth,
            maximum_dot_count=maximum_dot_count,
            rewrite_tuplets=rewrite_tuplets,
        )
    if prettify_rewrite_meter:
        measures = abjad.select(container[:]).group_by_measure()
        for meter, measure in zip(meter_list, measures):
            if boundary_depth is None or boundary_depth < 1:
                prettify_rewrite_meter_function(
                    measure,
                    meter,
                    fuse_across_groups_of_beats=fuse_across_groups_of_beats,
                    fuse_quadruple_meter=fuse_quadruple_meter,
                    fuse_triple_meter=fuse_triple_meter,
                    extract_trivial_tuplets=False,
                    split_quadruple_meter=split_quadruple_meter,
                )
            else:
                prettify_rewrite_meter_function(
                    measure,
                    meter,
                    fuse_across_groups_of_beats=False,
                    fuse_quadruple_meter=False,
                    fuse_triple_meter=False,
                    extract_trivial_tuplets=False,
                    split_quadruple_meter=False,
                )
