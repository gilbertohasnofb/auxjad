import abjad

import auxjad


def test_double_barlines_before_time_signatures_01():
    staff = abjad.Staff(
        r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
    )
    auxjad.mutate(staff[:]).double_barlines_before_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2.
            \bar "||"
            \time 4/4
            d'1
            e'1
            \bar "||"
            \time 6/4
            f'2.
            g'2.
        }
        """)


def test_double_barlines_before_time_signatures_02():
    staff = abjad.Staff(
        r"\time 3/4 R1 * 3/4 \time 4/4 R1 * 2 \time 6/4 R1 * 6/4 \time 4/4 R1"
    )
    auxjad.mutate(staff[:]).double_barlines_before_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            R1 * 3/4
            \bar "||"
            \time 4/4
            R1 * 2
            \bar "||"
            \time 6/4
            R1 * 3/2
            \bar "||"
            \time 4/4
            R1
        }
        """)


def test_double_barlines_before_time_signatures_03():
    staff = abjad.Staff(
        r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
    )
    abjad.attach(abjad.BarLine('||'), staff[2])
    auxjad.mutate(staff[:]).double_barlines_before_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2.
            \bar "||"
            \time 4/4
            d'1
            e'1
            \bar "||"
            \time 6/4
            f'2.
            g'2.
        }
        """)


def test_double_barlines_before_time_signatures_04():
    staff = abjad.Staff(
        r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
    )
    abjad.attach(abjad.BarLine('||'), staff[2])
    auxjad.mutate(staff[:]).double_barlines_before_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2.
            \bar "||"
            \time 4/4
            d'1
            e'1
            \bar "||"
            \time 6/4
            f'2.
            g'2.
        }
        """)


def test_double_barlines_before_time_signatures_05():
    staff = abjad.Staff(
        r"R1 "
        r"\time 3/4 c'2. "
        r"\time 4/4 d'1 "
        r"e'1 "
        r"\time 6/4 f'2. g'2. "
        r"\time 2/4 a'2"
    )
    abjad.attach(abjad.BarLine('.|:'), staff[0])
    abjad.attach(abjad.BarLine(':|.'), staff[1])
    abjad.attach(abjad.BarLine('|'), staff[3])
    abjad.attach(abjad.BarLine('!'), staff[5])
    auxjad.mutate(staff[:]).double_barlines_before_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            R1
            \bar ".|:"
            \time 3/4
            c'2.
            \bar ":|."
            \time 4/4
            d'1
            e'1
            \bar "||"
            \time 6/4
            f'2.
            g'2.
            \bar "!"
            \time 2/4
            a'2
        }
        """)
