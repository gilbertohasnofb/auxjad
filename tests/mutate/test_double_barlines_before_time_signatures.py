import abjad

import auxjad


def test_double_barlines_before_time_signatures_01():
    staff = abjad.Staff(
        r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
    )
    auxjad.mutate.double_barlines_before_time_signatures(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    auxjad.mutate.double_barlines_before_time_signatures(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    auxjad.mutate.double_barlines_before_time_signatures(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    auxjad.mutate.double_barlines_before_time_signatures(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    auxjad.mutate.double_barlines_before_time_signatures(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
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


def test_double_barlines_before_time_signatures_06():
    staff_1 = abjad.Staff(r"\time 4/4 c'1 d'1 \time 6/4 e'1.")
    staff_2 = abjad.Staff(r"\time 4/4 \clef bass c1 d1 \time 6/4 e1.")
    score = abjad.Score([staff_1, staff_2])
    auxjad.mutate.double_barlines_before_time_signatures(
        staff_1[:],
        context='Staff',
    )
    auxjad.mutate.double_barlines_before_time_signatures(
        staff_2[:],
        context='Staff',
    )
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                c'1
                d'1
                \bar "||"
                \time 6/4
                e'1.
            }
            \new Staff
            {
                \time 4/4
                \clef "bass"
                c1
                d1
                \bar "||"
                \time 6/4
                e1.
            }
        >>
        """)
    assert abjad.lilypond(staff_1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            d'1
            \bar "||"
            \time 6/4
            e'1.
        }
        """)
    assert abjad.lilypond(staff_2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            \clef "bass"
            c1
            d1
            \bar "||"
            \time 6/4
            e1.
        }
        """)
