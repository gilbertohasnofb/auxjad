import abjad

import auxjad


def test_extract_trivial_tuplets_01():
    staff = abjad.Staff(r"\times 2/3 {r4 r2} \times 2/3 {c'8 ~ c'8 ~ c'2}")
    auxjad.mutate(staff[:]).extract_trivial_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r2
            c'2
        }
        """)


def test_extract_trivial_tuplets_02():
    staff = abjad.Staff(r"\times 4/5 {r2. \times 2/3 {r2 r4}}")
    auxjad.mutate(staff[:]).extract_trivial_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r1
        }
        """)


def test_extract_trivial_tuplets_03():
    staff = abjad.Staff(r"\times 4/5 {c'2. ~ \times 2/3 {c'2 ~ c'4}}")
    auxjad.mutate(staff[:]).extract_trivial_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
        }
        """)


def test_extract_trivial_tuplets_04():
    staff = abjad.Staff(r"\times 2/3 {<c' d'>1 ~ <c' d'>2}")
    auxjad.mutate(staff[:]).extract_trivial_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            <c' d'>1
        }
        """)


def test_extract_trivial_tuplets_05():
    staff = abjad.Staff(
        r"\times 2/3 {r2 r1} \times 4/5 {c'2. \times 2/3 {r2 r4}}"
    )
    auxjad.mutate(staff[:]).extract_trivial_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r1
            \times 4/5 {
                c'2.
                r2
            }
        }
        """)


def test_extract_trivial_tuplets_06():
    staff = abjad.Staff(r"\time 3/4 r2. \times 3/2 {r4 r4}")
    auxjad.mutate(staff[:]).extract_trivial_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            r2.
            r2.
        }
        """)


def test_extract_trivial_tuplets_07():
    staff = abjad.Staff(r"\times 2/3 {r2 r2 r2}")
    abjad.mutate(staff[:]).extract_trivial_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r1
        }
        """)


def test_extract_trivial_tuplets_08():
    staff = abjad.Staff(r"\times 2/3 {c'4} r2 \times 2/3 {d'2}"
                        r"\times 2/3 {e'1.}"
                        )
    abjad.mutate(staff[:]).extract_trivial_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'4
            }
            r2
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'2
            }
            e'1
        }
        """)


def test_extract_trivial_tuplets_09():
    staff = abjad.Staff(r"\time 6/4 c'4\f \times 5/6 {g1.\p}")
    abjad.mutate(staff[:]).extract_trivial_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 6/4
            c'4
            \f
            g1
            \p
            ~
            g4
        }
        """)
