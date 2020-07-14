from typing import Union

import abjad


def prettify_rewrite_meter(container: abjad.Container,
                           meter: Union[tuple,
                                        abjad.Meter,
                                        abjad.TimeSignature,
                                        abjad.Duration,
                                        ],
                           *,
                           fuse_across_groups_of_beats: bool = True,
                           fuse_quadruple_meter: bool = True,
                           fuse_triple_meter: bool = True,
                           ):
    r"""Mutates an input container (of type ``abjad.Container`` or child class)
    in place and has no return value; this function fuses pitched leaves
    according to the rules shown below, improving the default output of
    ``abjad.rewrite_meter()``.

    Example:
        Meters whose denominators are a crotchet or longer get tied notes
        within a beat after ``rewrite_meter()`` when they are at an offset
        ``denominator / 4``, so a rhythm such as  ``denominator / 4``
        ``denominator / 2`` ``denominator / 4`` becomes ``denominator / 4``
        ``denominator / 4`` ``~`` ``denominator / 4`` ``denominator / 4``. This
        function looks for those specific cases and fuses them, generating an
        output which is often more readable.

        >>> staff = abjad.Staff(
        ...     r"\time 3/4 c'16 d'8 e'16 f'16 g'16 a'8 b'8 c''16 d''16")
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

        .. figure:: ../_images/image-prettify_rewrite_meter-1.png

        >>> auxjad.prettify_rewrite_meter(staff, meter)
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

        .. figure:: ../_images/image-prettify_rewrite_meter-2.png

    Example:
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

        .. figure:: ../_images/image-prettify_rewrite_meter-3.png

        >>> auxjad.prettify_rewrite_meter(staff, meter)
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

        .. figure:: ../_images/image-prettify_rewrite_meter-4.png

    Example:
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

        .. figure:: ../_images/image-prettify_rewrite_meter-5.png

        >>> auxjad.prettify_rewrite_meter(staff, meter)
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

        .. figure:: ../_images/image-prettify_rewrite_meter-6.png

        to disable this behaviour, set the optional keyword argument
        ``fuse_across_groups_of_beats`` to ``False``.

        >>> staff = abjad.Staff(r"\time 6/4 c'8 d'4 e'4 f'4 g'4 a'4 b'8")
        >>> meter = abjad.Meter((6, 4))
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> auxjad.prettify_rewrite_meter(staff,
        ...                               meter,
        ...                               fuse_across_groups_of_beats=False,
        ...                               )
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

        .. figure:: ../_images/image-prettify_rewrite_meter-7.png

    Example:
        The fused notes will respect the beat structures of such meters, even
        when ``increase_monotonic`` is set to the non-default value ``True``.
        Compare the outputs below.

        >>> staff = abjad.Staff(r"\time 7/4 c'8 d'4 e'4 f'4 g'4 a'4 b'4 c''8")
        >>> meter = abjad.Meter((7, 4))
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> auxjad.prettify_rewrite_meter(staff, meter)
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

        .. figure:: ../_images/image-prettify_rewrite_meter-8.png

        >>> staff = abjad.Staff(r"\time 7/4 c'8 d'4 e'4 f'4 g'4 a'4 b'4 c''8")
        >>> meter = abjad.Meter((7, 4), increase_monotonic=True)
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> auxjad.prettify_rewrite_meter(staff, meter)
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

        .. figure:: ../_images/image-prettify_rewrite_meter-9.png

    Example:
        This function can take handle multiple bars at once, as long as they
        share the same meter.

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

        .. figure:: ../_images/image-prettify_rewrite_meter-10.png

        >>> auxjad.prettify_rewrite_meter(staff, meter)
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

        .. figure:: ../_images/image-prettify_rewrite_meter-11.png

    Example:
        This function also takes care of two special cases, namely quadruple
        and triple meters. By default, it will fuse leaves in quadruple meters
        across beats 1 and 2, and across beats 3 and 4 (as long as they fulfil
        the other requirements of duration and offset).

        >>> staff = abjad.Staff(r"\time 4/4 c'8 d'4 e'4 f'4 g'8")
        >>> meter = abjad.Meter((4, 4))
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> auxjad.prettify_rewrite_meter(staff, meter)
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

        .. figure:: ../_images/image-prettify_rewrite_meter-12.png

        Set ``fuse_quadruple_meter`` to ``False`` to disable this behaviour.

        >>> staff = abjad.Staff(r"\time 4/4 c'8 d'4 e'4 f'4 g'8")
        >>> meter = abjad.Meter((4, 4))
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> auxjad.prettify_rewrite_meter(staff,
        ...                               meter,
        ...                               fuse_quadruple_meter=False,
        ...                               )
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

        .. figure:: ../_images/image-prettify_rewrite_meter-13.png

    Example:
        In the case of triple meters, it will fuse leaves across any beat as
        long as the previously mentioned conditions of offset and duration are
        met.

        >>> staff = abjad.Staff(r"\time 3/4 c'8 d'4 e'4 f'8")
        >>> meter = abjad.Meter((3, 4))
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> auxjad.prettify_rewrite_meter(staff, meter)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'8
            d'4
            e'4
            f'8
        }

        .. figure:: ../_images/image-prettify_rewrite_meter-14.png

        Similarly to the example before, set ``fuse_triple_meter`` to ``False``
        to disable this behaviour.

        >>> staff = abjad.Staff(r"\time 3/4 c'8 d'4 e'4 f'8")
        >>> meter = abjad.Meter((3, 4))
        >>> abjad.mutate(staff).rewrite_meter(meter)
        >>> auxjad.prettify_rewrite_meter(staff,
        ...                               meter,
        ...                               fuse_triple_meter=False,
        ...                               )
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

        .. figure:: ../_images/image-prettify_rewrite_meter-15.png
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")
    if not isinstance(meter, (tuple, abjad.Meter, abjad.Duration,
                              abjad.TimeSignature)):
        raise TypeError("argument must be 'tuple', 'abjad.Meter', "
                        "'abjad.Duration',  or 'abjad.TimeSignature'")
    if not isinstance(fuse_across_groups_of_beats, bool):
        raise TypeError("'fuse_across_groups_of_beats' must be 'bool'")
    if not isinstance(fuse_quadruple_meter, bool):
        raise TypeError("'fuse_quadruple_meter' must be 'bool'")
    if not isinstance(fuse_triple_meter, bool):
        raise TypeError("'fuse_triple_meter' must be 'bool'")

    logical_ties = abjad.select(container).logical_ties(pitched=True)
    base = 1 / meter.denominator

    for logical_tie in logical_ties.filter_duration("==", base / 2):
        offset = abjad.inspect(logical_tie).timespan().start_offset
        offset %= base
        if offset == base / 4:
            abjad.mutate(logical_tie).fuse()

    if fuse_across_groups_of_beats:
        for logical_tie in logical_ties.filter_duration("==", base):
            offset = abjad.inspect(logical_tie).timespan().start_offset
            offset %= meter.duration
            offset_mod = offset % base
            if offset_mod == base / 2:
                if (not offset + base / 2
                        in meter.depthwise_offset_inventory[1]):
                    abjad.mutate(logical_tie).fuse()

    if fuse_quadruple_meter and meter.numerator == 4:
        for logical_tie in logical_ties.filter_duration("==", base):
            offset = abjad.inspect(logical_tie).timespan().start_offset
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
            offset %= meter.duration
            offset_mod = offset % base
            if offset_mod == base / 2:
                if not offset + base / 2 in (abjad.Offset(0, 1),
                                             abjad.Offset(3 * base),
                                             ):
                    abjad.mutate(logical_tie).fuse()
