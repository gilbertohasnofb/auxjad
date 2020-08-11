import abjad

import auxjad


def test_remove_repeated_time_signatures_01():
    staff = abjad.Staff(r"c'4 d'8 | c'4 d'8")
    abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
    abjad.attach(abjad.TimeSignature((3, 8)), staff[2])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            \time 3/8
            c'4
            d'8
        }
        """)
    auxjad.mutate(staff[:]).remove_repeated_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            c'4
            d'8
        }
        """)


def test_remove_repeated_time_signatures_02():
    staff = abjad.Staff(r"c'4 d'8 | e'4. | c'4 d'8")
    abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
    abjad.attach(abjad.TimeSignature((3, 8)), staff[3])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            e'4.
            \time 3/8
            c'4
            d'8
        }
        """)
    auxjad.mutate(staff[:]).remove_repeated_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            e'4.
            c'4
            d'8
        }
        """)


def test_remove_repeated_time_signatures_03():
    staff = abjad.Staff([abjad.Note("c'2"),
                         abjad.Chord("<d' f'>2"),
                         abjad.Tuplet((2, 3), "g2 a2 b2"),
                         ])
    abjad.attach(abjad.TimeSignature((2, 2)), staff[0])
    abjad.attach(abjad.TimeSignature((2, 2)), staff[2][0])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/2
            c'2
            <d' f'>2
            \times 2/3 {
                \time 2/2
                g2
                a2
                b2
            }
        }
        """)
    auxjad.mutate(staff[:]).remove_repeated_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/2
            c'2
            <d' f'>2
            \times 2/3 {
                g2
                a2
                b2
            }
        }
        """)


def test_remove_repeated_time_signatures_04():
    staff = abjad.Staff(r"c'2 d'2 | e'2 d'2")
    abjad.attach(abjad.TimeSignature((4, 4)), staff[2])
    auxjad.mutate(staff[:]).remove_repeated_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'2
            d'2
            e'2
            d'2
        }
        """)


def test_remove_repeated_time_signatures_05():
    staff = abjad.Staff(r"c'4 d'8 | c'4 d'8")
    abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
    abjad.attach(abjad.TimeSignature((3, 8)), staff[2])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            \time 3/8
            c'4
            d'8
        }
        """)
    abjad.mutate(staff[:]).remove_repeated_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            c'4
            d'8
        }
        """)
