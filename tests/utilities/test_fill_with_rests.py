import abjad
import pytest

import auxjad


def test_fill_with_rests_01():
    container1 = abjad.Container(r"c'4 d'4 e'4 f'4")
    container2 = abjad.Container(r"c'4 d'4 e'4")
    container3 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4")
    container4 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4 d'4 e'4 f'4")
    auxjad.fill_with_rests(container1)
    auxjad.fill_with_rests(container2)
    auxjad.fill_with_rests(container3)
    auxjad.fill_with_rests(container4)
    assert format(container1) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            r4
        }
        """)
    assert format(container3) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
            c'4
            r2.
        }
        """)
    assert format(container4) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
            c'4
            d'4
            e'4
            f'4
        }
        """)


def test_fill_with_rests_02():
    container1 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4 g'")
    container2 = abjad.Container(r"\time 3/4 a2. \time 2/4 c'4")
    container3 = abjad.Container(r"\time 5/4 g1 ~ g4 \time 4/4 af'2")
    auxjad.fill_with_rests(container1)
    auxjad.fill_with_rests(container2)
    auxjad.fill_with_rests(container3)
    assert format(container1) == abjad.String.normalize(
        r"""
        {
            %%% \time 4/4 %%%
            c'4
            d'4
            e'4
            f'4
            g'4
            r2.
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        {
            %%% \time 3/4 %%%
            a2.
            %%% \time 2/4 %%%
            c'4
            r4
        }
        """)
    assert format(container3) == abjad.String.normalize(
        r"""
        {
            %%% \time 5/4 %%%
            g1
            ~
            g4
            %%% \time 4/4 %%%
            af'2
            r2
        }
        """)


def test_fill_with_rests_03():
    container = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4 g'4")
    auxjad.fill_with_rests(container)
    assert format(container) == abjad.String.normalize(
        r"""
        {
            %%% \time 4/4 %%%
            c'4
            d'4
            e'4
            f'4
            g'4
            r2.
        }
        """)
    staff = abjad.Staff([container])
    assert format(container) == abjad.String.normalize(
        r"""
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
            g'4
            r2.
        }
        """)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 4/4
                c'4
                d'4
                e'4
                f'4
                g'4
                r2.
            }
        }
        """)


def test_fill_with_rests_04():
    container = abjad.Container(r"c'4 d'4 e'4 f'4 g'4")
    time_signature = abjad.TimeSignature((3, 4), partial=(1, 4))
    abjad.attach(time_signature, container[0])
    auxjad.fill_with_rests(container)
    assert format(container) == abjad.String.normalize(
        r"""
        {
            %%% \partial 4 %%%
            %%% \time 3/4 %%%
            c'4
            d'4
            e'4
            f'4
            g'4
            r4
            r4
        }
        """)


def test_fill_with_rests_05():
    container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'1")
    with pytest.raises(ValueError):
        assert auxjad.fill_with_rests(container)


def test_fill_with_rests_06():
    staff = abjad.Staff(r"\time 4/4 c'4 d'4 e'4 f'4 g'4 ~ g'16")
    auxjad.fill_with_rests(staff)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
            g'4
            ~
            g'16
            r8.
            r2
        }
        """)


def test_fill_with_rests_07():
    staff = abjad.Staff(r"\time 4/4 c'8 d'4 e'8")
    auxjad.fill_with_rests(staff)
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
            r2
        }
        """)
    staff = abjad.Staff(r"\time 4/4 c'8 d'4 e'8")
    auxjad.fill_with_rests(staff, disable_rewrite_meter=True)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'8
            d'4
            e'8
            r2
        }
        """)
