import abjad

import auxjad


def test_remove_empty_tuplets_01():
    staff = abjad.Staff(r"\times 2/3 {r2 r2 r2}")
    auxjad.remove_empty_tuplets(staff[:])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r1
        }
        """)


def test_remove_empty_tuplets_02():
    staff = abjad.Staff(r"\times 4/5 {r2. \times 2/3 {r2 r4}}")
    auxjad.remove_empty_tuplets(staff[:])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r1
        }
        """)


def test_remove_empty_tuplets_03():
    staff = abjad.Staff(
        r"r2 \times 2/3 {r2 r4} \times 4/5 {c'2. \times 2/3 {r2 r4}}")
    auxjad.remove_empty_tuplets(staff[:])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r2
            r2
            \times 4/5 {
                c'2.
                r2
            }
        }
        """)


def test_remove_empty_tuplets_04():
    staff = abjad.Staff(r"\time 3/4 r2. \times 3/2 {r4 r4}")
    auxjad.remove_empty_tuplets(staff[:])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            r2.
            r2.
        }
        """)


def test_remove_empty_tuplets_05():
    staff = abjad.Staff(r"\times 2/3 {r2 r2 r2}")
    abjad.mutate(staff[:]).remove_empty_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r1
        }
        """)
