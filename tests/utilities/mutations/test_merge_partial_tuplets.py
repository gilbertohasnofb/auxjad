import abjad

import auxjad


def test_merge_partial_tuplets_01():
    staff = abjad.Staff(r"\times 2/3 {c'1} \times 2/3 {d'2}")
    auxjad.mutate(staff[:]).merge_partial_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                c'1
                d'2
            }
        }
        """)


def test_merge_partial_tuplets_02():
    staff = abjad.Staff(r"\times 2/3 {r4} \times 2/3 {c'2} "
                        r"\times 4/5 {d'2~} \times 4/5{d'8}")
    auxjad.mutate(staff[:]).merge_partial_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                r4
                c'2
            }
            \times 4/5 {
                d'2
                ~
                d'8
            }
        }
        """)


def test_merge_partial_tuplets_03():
    staff = abjad.Staff(r"\times 2/3 {c'2} \times 2/3 {d'2} \times 2/3 {e'2}")
    auxjad.mutate(staff[:]).merge_partial_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                c'2
                d'2
                e'2
            }
        }
        """)


def test_merge_partial_tuplets_04():
    staff = abjad.Staff(r"\times 2/3 {c'2\p\< d'2} \times 2/3 {e'2\ff}")
    auxjad.mutate(staff[:]).merge_partial_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                c'2
                \p
                \<
                d'2
                e'2
                \ff
            }
        }
        """)


def test_merge_partial_tuplets_05():
    staff = abjad.Staff(
        r"\times 2/3 {c'4 d'4 e'4} \times 2/3 {f'4} \times 2/3 {g'4 a'4}"
    )
    auxjad.mutate(staff[:]).merge_partial_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                c'4
                d'4
                e'4
            }
            \times 2/3 {
                f'4
                g'4
                a'4
            }
        }
        """)


def test_merge_partial_tuplets_06():
    staff = abjad.Staff(r"\time 3/4 c'2. "
                        r"\times 2/3 {d'4} r4 \times 2/3 {e'2} "
                        r"\times 2/3 {f'4} r4 \times 2/3 {g'2}")
    auxjad.mutate(staff[:]).merge_partial_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2.
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'4
            }
            r4
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                e'2
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                f'4
            }
            r4
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                g'2
            }
        }
        """)
    staff = abjad.Staff(r"\time 3/4 c'2. "
                        r"\times 2/3 {d'4} r4 \times 2/3 {e'2} "
                        r"\times 2/3 {f'4} r4 \times 2/3 {g'2}")
    auxjad.mutate(staff[:]).merge_partial_tuplets(merge_across_barlines=True)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2.
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'4
            }
            r4
            \times 2/3 {
                e'2
                f'4
            }
            r4
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                g'2
            }
        }
        """)


def test_merge_partial_tuplets_07():
    staff = abjad.Staff(r"\times 2/3 {c'1} \times 2/3 {d'2}")
    abjad.mutate(staff[:]).merge_partial_tuplets()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                c'1
                d'2
            }
        }
        """)
