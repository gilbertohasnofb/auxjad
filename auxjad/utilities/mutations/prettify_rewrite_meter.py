from typing import Union

import abjad

from .extract_trivial_tuplets import (
    extract_trivial_tuplets as extract_trivial_tuplets_function,
)


def prettify_rewrite_meter(selection: abjad.Selection,
                           meter: Union[abjad.Meter, abjad.TimeSignature],
                           *,
                           fuse_across_groups_of_beats: bool = True,
                           fuse_quadruple_meter: bool = True,
                           fuse_triple_meter: bool = True,
                           extract_trivial_tuplets: bool = True,
                           ):
    r"""Mutates an input |abjad.Selection| in place and has no return value;
    this function fuses pitched leaves according to the rules shown below,
    improving the default output of |abjad.mutate().rewrite_meter()|.

    Basic usage:
        Meters whose denominators are a crotchet or longer get tied notes
        within a beat after |abjad.mutate().rewrite_meter()| when they are at
        an offset ``denominator / 4``, so a rhythm such as  ``denominator / 4``
        ``denominator / 2`` ``denominator / 4`` becomes ``denominator / 4``
        ``denominator / 4`` ``~`` ``denominator / 4`` ``denominator / 4``. This
        function looks for those specific cases and fuses them, generating an
        output which is often more readable.

        >>> staff = abjad.Staff(
        ...     r"\time 3/4 c'16 d'8 e'16 f'16 g'16 a'8 b'8 c''16 d''16"
        ... )
        >>> meter = abjad.Meter((3, 4))
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'16
            d'16
            ~
            d'16
            e'16
            f'16
            g'16
            a'8
            b'8
            c''16
            d''16
        }

        .. figure:: ../_images/prettify_rewrite_meter-vlnd7l5fb7s.png

        >>> auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'16
            d'8
            e'16
            f'16
            g'16
            a'8
            b'8
            c''16
            d''16
        }

        .. figure:: ../_images/prettify_rewrite_meter-e7vfnese0ut.png

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.mutate()|. It can thus be used from either
        :func:`auxjad.mutate()` or |abjad.mutate()|. Therefore, the two lines
        below are equivalent:

        >>> auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
        >>> abjad.mutate(staff[:]).prettify_rewrite_meter(meter)

    Other examples:
        The rhythm of the leaves just before and after the two leaves to be
        fused can be different than ``denominator / 4``, as the function
        searches for logical ties of specific length and offset, and its
        surroundings do not matter.

        >>> staff = abjad.Staff(r"\time 3/4 c'32 d'32 e'8 f'16 "
        ...                     r"\times 2/3 {g'32 a'32 b'32} c''8 "
        ...                     r"r16 r32. d''64 e''8 f''32 g''32"
        ...                     )
        >>> meter = abjad.Meter((3, 4))
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'32
            d'32
            e'16
            ~
            e'16
            f'16
            \times 2/3 {
                g'32
                a'32
                b'32
            }
            c''16
            ~
            c''16
            r16
            r32.
            d''64
            e''16
            ~
            e''16
            f''32
            g''32
        }

        .. figure:: ../_images/prettify_rewrite_meter-kw09gse2zxj.png

        >>> auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'32
            d'32
            e'8
            f'16
            \times 2/3 {
                g'32
                a'32
                b'32
            }
            c''8
            r16
            r32.
            d''64
            e''8
            f''32
            g''32
        }

        .. figure:: ../_images/prettify_rewrite_meter-u5gmtdippsa.png

    ``fuse_across_groups_of_beats``:
        By default, this function also fuses rhythms of type
        ``denominator / 2`` ``denominator / 2`` ``~`` ``denominator / 2``
        ``denominator / 2``, becoming ``denominator / 2`` ``denominator``
        ``denominator / 2``. This is only applied when the meter's structure
        has a depth of 2, which is the case for meters with numerators equal to
        or larger than ``5``.

        >>> staff = abjad.Staff(r"\time 6/4 c'8 d'4 e'4 f'4 g'4 a'4 b'8")
        >>> meter = abjad.Meter((6, 4))
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 6/4
            c'8
            d'8
            ~
            d'8
            e'8
            ~
            e'8
            f'8
            ~
            f'8
            g'8
            ~
            g'8
            a'8
            ~
            a'8
            b'8
        }

        .. figure:: ../_images/prettify_rewrite_meter-tqi4p0u8qog.png

        >>> auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 6/4
            c'8
            d'4
            e'4
            f'8
            ~
            f'8
            g'4
            a'4
            b'8
        }

        .. figure:: ../_images/prettify_rewrite_meter-riif1glyqpo.png

        to disable this behaviour, set the optional keyword argument
        ``fuse_across_groups_of_beats`` to ``False``.

        >>> staff = abjad.Staff(r"\time 6/4 c'8 d'4 e'4 f'4 g'4 a'4 b'8")
        >>> meter = abjad.Meter((6, 4))
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> auxjad.mutate(staff[:]).prettify_rewrite_meter(
        ...     meter,
        ...     fuse_across_groups_of_beats=False,
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            \time 6/4
            c'8
            d'8
            ~
            d'8
            e'8
            ~
            e'8
            f'8
            ~
            f'8
            g'8
            ~
            g'8
            a'8
            ~
            a'8
            b'8
        }

        .. figure:: ../_images/prettify_rewrite_meter-ki5xbiteij.png

    |abjad.Meter| with ``increase_monotonic=True``:
        The fused notes will respect the beat structures of such meters, even
        when ``increase_monotonic`` is set to the non-default value ``True``.
        Compare the outputs below.

        >>> staff = abjad.Staff(r"\time 7/4 c'8 d'4 e'4 f'4 g'4 a'4 b'4 c''8")
        >>> meter = abjad.Meter((7, 4))
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
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
        }

        .. figure:: ../_images/prettify_rewrite_meter-bud0jhkvvl.png

        >>> staff = abjad.Staff(r"\time 7/4 c'8 d'4 e'4 f'4 g'4 a'4 b'4 c''8")
        >>> meter = abjad.Meter((7, 4), increase_monotonic=True)
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
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
        }

        .. figure:: ../_images/prettify_rewrite_meter-47y86pbwwv5.png

    Multiple measures:
        This function can take handle multiple measures at once, as long as
        they share the same meter.

        >>> staff = abjad.Staff(r"\time 5/8 c'16 d'8 e'8 f'8 g'8 a'16 ~ "
        ...                     r"a'16 b'8 c''8 d''8 e''8 f''16"
        ...                     )
        >>> meter = abjad.Meter((5, 8))
        >>> for measure in abjad.select(staff).group_by_measure():
        ...     abjad.mutate(measure).rewrite_meter(meter)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 5/8
            c'16
            d'16
            ~
            d'16
            e'16
            ~
            e'16
            f'16
            ~
            f'16
            g'16
            ~
            g'16
            a'16
            ~
            a'16
            b'16
            ~
            b'16
            c''16
            ~
            c''16
            d''16
            ~
            d''16
            e''16
            ~
            e''16
            f''16
        }

        .. figure:: ../_images/prettify_rewrite_meter-8jdzmvf9yl.png

        >>> auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 5/8
            c'16
            d'8
            e'8
            f'16
            ~
            f'16
            g'8
            a'16
            ~
            a'16
            b'8
            c''8
            d''16
            ~
            d''16
            e''8
            f''16
        }

        .. figure:: ../_images/prettify_rewrite_meter-pcn8x9hr6bb.png

    ``fuse_quadruple_meter``:
        This function also takes care of two special cases, namely quadruple
        and triple meters. By default, it will fuse leaves in quadruple meters
        across beats 1 and 2, and across beats 3 and 4 (as long as they fulfil
        the other requirements of duration and offset).

        >>> staff = abjad.Staff(r"\time 4/4 c'8 d'4 e'4 f'4 g'8")
        >>> meter = abjad.Meter((4, 4))
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'8
            d'4
            e'8
            ~
            e'8
            f'4
            g'8
        }

        .. figure:: ../_images/prettify_rewrite_meter-nap4bbf7mxe.png

        Set ``fuse_quadruple_meter`` to ``False`` to disable this behaviour.

        >>> staff = abjad.Staff(r"\time 4/4 c'8 d'4 e'4 f'4 g'8")
        >>> meter = abjad.Meter((4, 4))
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> auxjad.mutate(staff[:]).prettify_rewrite_meter(
        ...     meter,
        ...     fuse_quadruple_meter=False,
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'8
            d'8
            ~
            d'8
            e'8
            ~
            e'8
            f'8
            ~
            f'8
            g'8
        }

        .. figure:: ../_images/prettify_rewrite_meter-juipg9nzna.png

    ``fuse_triple_meter``:
        In the case of triple meters, it will fuse leaves across any beat as
        long as the previously mentioned conditions of offset and duration are
        met.

        >>> staff = abjad.Staff(r"\time 3/4 c'8 d'4 e'4 f'8")
        >>> meter = abjad.Meter((3, 4))
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'8
            d'4
            e'4
            f'8
        }

        .. figure:: ../_images/prettify_rewrite_meter-4wg3grpb94p.png

        Similarly to the example before, set ``fuse_triple_meter`` to ``False``
        to disable this behaviour.

        >>> staff = abjad.Staff(r"\time 3/4 c'8 d'4 e'4 f'8")
        >>> meter = abjad.Meter((3, 4))
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> auxjad.mutate(staff[:]).prettify_rewrite_meter(
        ...     meter,
        ...     fuse_triple_meter=False,
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'8
            d'8
            ~
            d'8
            e'8
            ~
            e'8
            f'8
        }

        .. figure:: ../_images/prettify_rewrite_meter-l16ostzscta.png

    ``extract_trivial_tuplets``:
        By default, this function extracts the contents of tuples that consist
        solely of rests, or solely of tied notes and chords.

        >>> staff = abjad.Staff(
        ...     r"\times 2/3 {c'4 ~ c'8} \times 2/3 {d'8 r4} "
        ...     r"\times 2/3 {r8 r8 r8} \times 2/3 {<e' g'>8 ~ <e' g'>4}"
        ... )
        >>> meter = abjad.Meter((4, 4))
        >>> abjad.mutate(staff[:]).rewrite_meter(meter)
        >>> abjad.mutate(staff[:]).prettify_rewrite_meter(meter)
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

        .. figure:: ../_images/prettify_rewrite_meter-a72jx4fc1xd.png

        Set ``extract_trivial_tuplets`` to ``False`` to disable this behaviour.

        >>> staff = abjad.Staff(
        ...     r"\times 2/3 {c'4 ~ c'8} \times 2/3 {d'8 r4} "
        ...     r"\times 2/3 {r8 r8 r8} \times 2/3 {<e' g'>8 ~ <e' g'>4}"
        ... )
        >>> meter = abjad.Meter((4, 4))
        >>> abjad.mutate(staff[:]).rewrite_meter(meter)
        >>> abjad.mutate(staff[:]).prettify_rewrite_meter(
        ...     meter,
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

        .. figure:: ../_images/prettify_rewrite_meter-v9q0ka94qcd.png

    Multiple measures:
        Similarly to |abjad.mutate().rewrite_meter()|, this function accepts
        selections of multiple measures:

        >>> staff = abjad.Staff(r"\time 4/4 c'8 d'4 e'4 f'4 g'8 | "
        ...                     r"a'8 b'4 c''8 d''16 e''4 f''8.")
        >>> meter = abjad.Meter((4, 4))
        >>> for measure in abjad.select(staff[:]).group_by_measure():
        ...     abjad.mutate(measure).rewrite_meter(meter)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'8
            d'8
            ~
            d'8
            e'8
            ~
            e'8
            f'8
            ~
            f'8
            g'8
            a'8
            b'8
            ~
            b'8
            c''8
            d''16
            e''8.
            ~
            e''16
            f''8.
        }

        .. figure:: ../_images/prettify_rewrite_meter-s8fg7a2k0tr.png

        >>> for measure in abjad.select(staff[:]).group_by_measure():
        ...     auxjad.mutate(measure).prettify_rewrite_meter(meter)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'8
            d'4
            e'8
            ~
            e'8
            f'4
            g'8
            a'8
            b'4
            c''8
            d''16
            e''8.
            ~
            e''16
            f''8.
        }

        .. figure:: ../_images/prettify_rewrite_meter-rgd7ok7fkq.png

    Multiple measures with different meters:
        If the measures have different meters, they can be passed on
        individually using :func:`zip()` as shown below.

        >>> staff = abjad.Staff(r"\time 3/4 c'8 d'4 e'4 f'16 g'16 | "
        ...                     r"\time 4/4 a'8 b'4 c''8 d''16 e''4 f''8.")
        >>> meters = [abjad.Meter((3, 4)), abjad.Meter((4, 4))]
        >>> for meter, measure in zip(
        ...     meters,
        ...     abjad.select(staff[:]).group_by_measure(),
        ... ):
        ...     abjad.mutate(measure).rewrite_meter(meter)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'8
            d'8
            ~
            d'8
            e'8
            ~
            e'8
            f'16
            g'16
            \time 4/4
            a'8
            b'8
            ~
            b'8
            c''8
            d''16
            e''8.
            ~
            e''16
            f''8.
        }

        .. figure:: ../_images/prettify_rewrite_meter-o2izz0m7s9k.png

        >>> for meter, measure in zip(
        ...     meters,
        ...     abjad.select(staff[:]).group_by_measure(),
        ... ):
        ...     auxjad.mutate(measure).prettify_rewrite_meter(meter)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'8
            d'4
            e'4
            f'16
            g'16
            \time 4/4
            a'8
            b'4
            c''8
            d''16
            e''8.
            ~
            e''16
            f''8.
        }

        .. figure:: ../_images/prettify_rewrite_meter-zh89kk66zon.png

    .. tip::

        Use :func:`auxjad.auto_rewrite_meter()` to automatically apply
        |abjad.mutate().rewrite_meter()| and
        |auxjad.mutate().prettify_rewrite_meter()| to a container with multiple
        time signatures.

    .. warning::

        The input selection must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containing
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(selection, abjad.Selection):
        raise TypeError("first argument must be 'abjad.Selection'")
    if not selection.leaves().are_contiguous_logical_voice():
        raise ValueError("first argument must be contiguous logical voice")
    if not isinstance(meter, (abjad.Meter, abjad.TimeSignature)):
        raise TypeError("argument must be 'abjad.Meter' or "
                        "'abjad.TimeSignature'")
    if not isinstance(fuse_across_groups_of_beats, bool):
        raise TypeError("'fuse_across_groups_of_beats' must be 'bool'")
    if not isinstance(fuse_quadruple_meter, bool):
        raise TypeError("'fuse_quadruple_meter' must be 'bool'")
    if not isinstance(fuse_triple_meter, bool):
        raise TypeError("'fuse_triple_meter' must be 'bool'")
    if not isinstance(extract_trivial_tuplets, bool):
        raise TypeError("'extract_trivial_tuplets' must be 'bool'")

    if isinstance(meter, abjad.TimeSignature):
        meter = abjad.Meter(meter.pair)

    logical_ties = selection.logical_ties(pitched=True)
    if len(logical_ties) == 0:
        return

    first_leaf = selection.logical_ties()[0]
    initial_offset = abjad.inspect(first_leaf).timespan().start_offset
    base = 1 / meter.denominator

    for logical_tie in logical_ties.filter_duration("==", base / 2):
        offset = abjad.inspect(logical_tie).timespan().start_offset
        offset -= initial_offset
        offset %= base
        if offset == base / 4:
            abjad.mutate(logical_tie).fuse()

    if fuse_across_groups_of_beats:
        for logical_tie in logical_ties.filter_duration("==", base):
            offset = abjad.inspect(logical_tie).timespan().start_offset
            offset -= initial_offset
            offset %= meter.duration
            offset_mod = offset % base
            if offset_mod == base / 2:
                if (not offset + base / 2
                        in meter.depthwise_offset_inventory[1]):
                    abjad.mutate(logical_tie).fuse()

    if fuse_quadruple_meter and meter.numerator == 4:
        for logical_tie in logical_ties.filter_duration("==", base):
            offset = abjad.inspect(logical_tie).timespan().start_offset
            offset -= initial_offset
            offset %= meter.duration
            offset_mod = offset % base
            if offset_mod == base / 2:
                if not offset + base / 2 in (abjad.Offset(0, 1),
                                             abjad.Offset(2 * base),
                                             abjad.Offset(4 * base),
                                             ):
                    abjad.mutate(logical_tie).fuse()

    if fuse_triple_meter and meter.numerator == 3:
        for logical_tie in logical_ties.filter_duration("==", base):
            offset = abjad.inspect(logical_tie).timespan().start_offset
            offset -= initial_offset
            offset %= meter.duration
            offset_mod = offset % base
            if offset_mod == base / 2:
                if not offset + base / 2 in (abjad.Offset(0, 1),
                                             abjad.Offset(3 * base),
                                             ):
                    abjad.mutate(logical_tie).fuse()

    if extract_trivial_tuplets:
        extract_trivial_tuplets_function(selection)
