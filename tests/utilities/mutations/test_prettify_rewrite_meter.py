import abjad

import auxjad


def test_prettify_rewrite_meter_01():
    staff = abjad.Staff(
        r"\time 3/4 c'16 d'8 e'16 f'16 g'16 a'8 b'8 c''16 d''16"
    )
    meter = abjad.Meter((3, 4))
    abjad.mutate(staff[:]).rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)
    auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_prettify_rewrite_meter_02():
    staff = abjad.Staff(r"\time 3/4 c'32 d'32 e'8 f'16 "
                        r"\times 2/3 {g'32 a'32 b'32} c''8 "
                        r"r16 r32. d''64 e''8 f''32 g''32"
                        )
    meter = abjad.Meter((3, 4))
    abjad.mutate(staff[:]).rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)
    auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_prettify_rewrite_meter_03():
    staff = abjad.Staff(r"\time 6/4 c'8 d'4 e'4 f'4 g'4 a'4 b'8")
    meter = abjad.Meter((6, 4))
    abjad.mutate(staff[:]).rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)
    auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_prettify_rewrite_meter_04():
    staff = abjad.Staff(r"\time 6/4 c'8 d'4 e'4 f'4 g'4 a'4 b'8")
    meter = abjad.Meter((6, 4))
    abjad.mutate(staff[:]).rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)
    auxjad.mutate(staff[:]).prettify_rewrite_meter(
        meter,
        fuse_across_groups_of_beats=False,
    )
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_prettify_rewrite_meter_05():
    staff = abjad.Staff(r"\time 7/4 c'8 d'4 e'4 f'4 g'4 a'4 b'4 c''8")
    meter = abjad.Meter((7, 4))
    abjad.mutate(staff[:]).rewrite_meter(meter)
    auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)
    staff = abjad.Staff(r"\time 7/4 c'8 d'4 e'4 f'4 g'4 a'4 b'4 c''8")
    meter = abjad.Meter((7, 4), increase_monotonic=True)
    abjad.mutate(staff[:]).rewrite_meter(meter)
    auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_prettify_rewrite_meter_06():
    staff = abjad.Staff(r"\time 5/8 c'16 d'8 e'8 f'8 g'8 a'16 ~ "
                        r"a'16 b'8 c''8 d''8 e''8 f''16"
                        )
    meter = abjad.Meter((5, 8))
    for measure in abjad.select(staff[:]).group_by_measure():
        abjad.mutate(measure).rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)
    auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_prettify_rewrite_meter_07():
    staff = abjad.Staff(r"\time 4/4 c'8 d'4 e'4 f'4 g'8")
    meter = abjad.Meter((4, 4))
    abjad.mutate(staff[:]).rewrite_meter(meter)
    auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)
    staff = abjad.Staff(r"\time 4/4 c'8 d'4 e'4 f'4 g'8")
    meter = abjad.Meter((4, 4))
    abjad.mutate(staff[:]).rewrite_meter(meter)
    auxjad.mutate(staff[:]).prettify_rewrite_meter(meter,
                                                   fuse_quadruple_meter=False,
                                                   )
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_prettify_rewrite_meter_08():
    staff = abjad.Staff(r"\time 3/4 c'8 d'4 e'4 f'8")
    meter = abjad.Meter((3, 4))
    abjad.mutate(staff[:]).rewrite_meter(meter)
    auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'8
            d'4
            e'4
            f'8
        }
        """)
    staff = abjad.Staff(r"\time 3/4 c'8 d'4 e'4 f'8")
    meter = abjad.Meter((3, 4))
    abjad.mutate(staff[:]).rewrite_meter(meter)
    auxjad.mutate(staff[:]).prettify_rewrite_meter(meter,
                                                   fuse_triple_meter=False,
                                                   )
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_prettify_rewrite_meter_09():
    staff = abjad.Staff(r"\times 2/3 {c'16 d'8 ~ } "
                        r"\times 2/3 {d'32 e'8 f'32 ~ } "
                        r"f'32 \times 2/3 {g'16 a'32} r32")
    abjad.attach(abjad.TimeSignature((3, 8)), staff[0][0])
    meter = abjad.Meter((3, 8))
    abjad.mutate(staff[:]).rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                \time 3/8
                c'16
                d'8
                ~
            }
            \times 2/3 {
                d'32
                e'32
                ~
                e'16.
                f'32
                ~
            }
            f'32
            \times 2/3 {
                g'16
                a'32
            }
            r32
        }
        """)
    auxjad.mutate(staff[:]).prettify_rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                \time 3/8
                c'16
                d'8
                ~
            }
            \times 2/3 {
                d'32
                e'32
                ~
                e'16.
                f'32
                ~
            }
            f'32
            \times 2/3 {
                g'16
                a'32
            }
            r32
        }
        """)


def test_prettify_rewrite_meter_10():
    staff = abjad.Staff(r"\time 4/4 c'8 d'4 e'4 f'4 g'8 | "
                        r"a'8 b'4 c''8 d''16 e''4 f''8.")
    meter = abjad.Meter((4, 4))
    for measure in abjad.select(staff[:]).group_by_measure():
        abjad.mutate(measure).rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)
    for measure in abjad.select(staff[:]).group_by_measure():
        auxjad.mutate(measure).prettify_rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_prettify_rewrite_meter_11():
    staff = abjad.Staff(r"\time 3/4 c'8 d'4 e'4 f'16 g'16 | "
                        r"\time 4/4 a'8 b'4 c''8 d''16 e''4 f''8.")
    meters = [abjad.Meter((3, 4)), abjad.Meter((4, 4))]
    for meter, measure in zip(meters,
                              abjad.select(staff[:]).group_by_measure(),
                              ):
        abjad.mutate(measure).rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)
    for meter, measure in zip(meters,
                              abjad.select(staff[:]).group_by_measure(),
                              ):
        auxjad.mutate(measure).prettify_rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_prettify_rewrite_meter_12():
    container1 = abjad.Staff(
        r"\time 4/4 c'8 d'8 ~ d'8 e'8 c'16 d'16 ~ d'16 e'16 r4 "
        r"c'8 d'8 ~ d'8 e'8 c'16 d'16 ~ d'16 e'16 r4"
    )
    container2 = abjad.mutate(container1).copy()
    meter = abjad.Meter((4, 4))
    abjad.mutate(container1[:]).prettify_rewrite_meter(meter)
    for measure in abjad.select(container2[:]).group_by_measure():
        abjad.mutate(measure).prettify_rewrite_meter(meter)
    selections = [container1[:], container2[:]]
    assert auxjad.inspect(selections).selections_are_equal()


def test_prettify_rewrite_meter_13():
    staff = abjad.Staff(
        r"\times 2/3 {c'4 ~ c'8} \times 2/3 {d'8 r4} "
        r"\times 2/3 {r8 r8 r8} \times 2/3 {<e' g'>8 ~ <e' g'>4}"
    )
    meter = abjad.Meter((4, 4))
    abjad.mutate(staff[:]).rewrite_meter(meter)
    abjad.mutate(staff[:]).prettify_rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_prettify_rewrite_meter_14():
    staff = abjad.Staff(
        r"\times 2/3 {c'4 ~ c'8} \times 2/3 {d'8 r4} "
        r"\times 2/3 {r8 r8 r8} \times 2/3 {<e' g'>8 ~ <e' g'>4}"
    )
    meter = abjad.Meter((4, 4))
    abjad.mutate(staff[:]).rewrite_meter(meter)
    abjad.mutate(staff[:]).prettify_rewrite_meter(
        meter,
        extract_trivial_tuplets=False,
    )
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_prettify_rewrite_meter_15():
    staff = abjad.Staff(
        r"c'4 d'2 r4"
        r"e'4. f'2 g'8"
        r"a'4. b'4. c''4"
        r"d''16 e''8. f''4. g''4 a''8"
    )
    meter = abjad.Meter((4, 4))
    for measure in abjad.select(staff[:]).group_by_measure():
        abjad.mutate(measure).rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'2
            r4
            e'4.
            f'8
            ~
            f'4.
            g'8
            a'4.
            b'4.
            c''4
            d''16
            e''8.
            f''4.
            g''8
            ~
            g''8
            a''8
        }
        """)
    abjad.mutate(staff[:]).prettify_rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'2
            r4
            e'4.
            f'8
            ~
            f'4.
            g'8
            a'4.
            b'8
            ~
            b'4
            c''4
            d''16
            e''8.
            f''4
            ~
            f''8
            g''4
            a''8
        }
        """)
    staff = abjad.Staff(
        r"c'4 d'2 r4"
        r"e'4. f'2 g'8"
        r"a'4. b'4. c''4"
        r"d''16 e''8. f''4. g''4 a''8"
    )
    meter = abjad.Meter((4, 4))
    for measure in abjad.select(staff[:]).group_by_measure():
        abjad.mutate(measure).rewrite_meter(meter)
    abjad.mutate(staff[:]).prettify_rewrite_meter(
        meter,
        split_quadruple_meter=False,
    )
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'2
            r4
            e'4.
            f'8
            ~
            f'4.
            g'8
            a'4.
            b'4.
            c''4
            d''16
            e''8.
            f''4.
            g''4
            a''8
        }
        """)


def test_prettify_rewrite_meter_16():
    staff = abjad.Staff(
        r"\time 3/4 c'16 d'8 e'16 f'16 g'16 a'8 b'8 c''16 d''16"
    )
    meter = abjad.Meter((3, 4))
    abjad.mutate(staff[:]).rewrite_meter(meter)
    abjad.mutate(staff[:]).prettify_rewrite_meter(meter)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)
