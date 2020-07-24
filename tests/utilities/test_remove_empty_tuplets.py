import abjad

import auxjad


def test_remove_empty_tuplets_01():
    container = abjad.Container(r"\times 2/3 {r2 r2 r2}")
    auxjad.remove_empty_tuplets(container)
    assert format(container) == abjad.String.normalize(
        r"""
        {
            r1
        }
        """)


def test_remove_empty_tuplets_02():
    container = abjad.Container(r"\times 4/5 {r2. \times 2/3 {r2 r4}}")
    auxjad.remove_empty_tuplets(container)
    assert format(container) == abjad.String.normalize(
        r"""
        {
            r1
        }
        """)


def test_remove_empty_tuplets_03():
    container = abjad.Container(
        r"r2 \times 2/3 {r2 r4} \times 4/5 {c'2. \times 2/3 {r2 r4}}")
    auxjad.remove_empty_tuplets(container)
    assert format(container) == abjad.String.normalize(
        r"""
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
    container = abjad.Container(r"\time 3/4 r2. \times 3/2 {r4 r4}")
    auxjad.remove_empty_tuplets(container)
    assert format(container) == abjad.String.normalize(
        r"""
        {
            %%% \time 3/4 %%%
            r2.
            r2.
        }
        """)
