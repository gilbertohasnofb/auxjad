import abjad
import pytest

import auxjad


def test_auto_rewrite_meter_01():
    staff = abjad.Staff(r"c'16 d'8 e'16 f'8 g'4 a'4 b'8 "
                        r"c'16 d'4. e'16 f'8 g'4 a'16 b'16")
    auxjad.mutate(staff).auto_rewrite_meter()
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_auto_rewrite_meter_02():
    staff = abjad.Staff(r"c'16 d'8 e'16 f'8 g'4 a'4 b'8 "
                        r"\time 6/8 b'4 c''4 r4 ")
    auxjad.mutate(staff).auto_rewrite_meter()
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_auto_rewrite_meter_03():
    staff = abjad.Staff(r"c'16 d'8 e'16 f'8 g'4 a'4 b'8 "
                        r"c'16 d'4. e'16 f'8 g'4 a'16 b'16")
    abjad.mutate(staff).auto_rewrite_meter(prettify_rewrite_meter=False)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_auto_rewrite_meter_04():
    staff = abjad.Staff(r"\time 7/4 c'8 d'4 e'4 f'4 g'4 a'4 b'4 c''8 "
                        r"\time 5/4 d''8 e''4 f''4 g''4 a''4 b''8")
    auxjad.mutate(staff).auto_rewrite_meter()
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
        """)
    staff = abjad.Staff(r"\time 7/4 c'8 d'4 e'4 f'4 g'4 a'4 b'4 c''8 "
                        r"\time 5/4 d''8 e''4 f''4 g''4 a''4 b''8")
    meter_list = [abjad.Meter((7, 4), increase_monotonic=True),
                  abjad.Meter((5, 4), increase_monotonic=True),
                  ]
    auxjad.mutate(staff).auto_rewrite_meter(meter_list=meter_list)
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
        """)


def test_auto_rewrite_meter_06():
    staff = abjad.Staff(
        r"\time 3/4 c'8 d'4 e'4 f'8 "
        r"\time 5/8 g'4 a'4 r8 "
        r"\time 6/8 b'4 c''4 r4 "
        r"\time 4/4 d''8 e''4 f''8 g''16 a''4 r8."
    )
    abjad.mutate(staff).auto_rewrite_meter()
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_auto_rewrite_meter_07():
    staff = abjad.Staff(r"c'16 d'8 e'16 f'8 g'4 a'4 b'8")
    with pytest.raises(TypeError):
        assert auxjad.mutate(staff[:]).auto_rewrite_meter()


def test_auto_rewrite_meter_08():
    staff = abjad.Staff(
        r"\times 2/3 {c'4 ~ c'8} \times 2/3 {d'8 r4} "
        r"\times 2/3 {r8 r8 r8} \times 2/3 {<e' g'>8 ~ <e' g'>4}"
    )
    abjad.mutate(staff).auto_rewrite_meter()
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


def test_auto_rewrite_meter_09():
    staff = abjad.Staff(
        r"\times 2/3 {c'4 ~ c'8} \times 2/3 {d'8 r4} "
        r"\times 2/3 {r8 r8 r8} \times 2/3 {<e' g'>8 ~ <e' g'>4}"
    )
    abjad.mutate(staff).auto_rewrite_meter(extract_trivial_tuplets=False)
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


def test_auto_rewrite_meter_10():
    staff = abjad.Staff(r"\times 2/3 {c'2 d'1}"
                        r"\times 2/3 {e'2} \times 2/3 {f'1}"
                        )
    abjad.mutate(staff).auto_rewrite_meter()
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)
    staff = abjad.Staff(r"\times 2/3 {c'2 d'1}"
                        r"\times 2/3 {e'2} \times 2/3 {f'1}"
                        )
    abjad.mutate(staff).auto_rewrite_meter(merge_partial_tuplets=False)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_auto_rewrite_meter_11():
    staff = abjad.Staff(r"c'16 d'8 e'16 f'8 g'4 a'4 b'8")
    abjad.mutate(staff).auto_rewrite_meter()
    assert format(staff) == abjad.String.normalize(
        r"""
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
        }
        """)
