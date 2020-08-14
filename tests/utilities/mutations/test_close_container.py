import abjad
import pytest

import auxjad


def test_close_container_01():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
    container2 = abjad.Staff(r"c'4 d'4 e'4")
    container3 = abjad.Staff(r"c'4 d'4 e'4 f'4 | c'4")
    container4 = abjad.Staff(r"c'4 d'4 e'4 f'4 | c'4 d'4 e'4 f'4")
    auxjad.mutate(container1).close_container()
    auxjad.mutate(container2).close_container()
    auxjad.mutate(container3).close_container()
    auxjad.mutate(container4).close_container()
    assert format(container1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
        }
        """)
    assert format(container3) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
            \time 1/4
            c'4
        }
        """)
    assert format(container4) == abjad.String.normalize(
        r"""
        \new Staff
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


def test_close_container_02():
    container1 = abjad.Staff(r"\time 4/4 c'4 d'4 e'4 f'4 g'")
    container2 = abjad.Staff(r"\time 3/4 a2. \time 2/4 c'4")
    container3 = abjad.Staff(r"\time 5/4 g1 ~ g4 \time 4/4 af'2")
    auxjad.mutate(container1).close_container()
    auxjad.mutate(container2).close_container()
    auxjad.mutate(container3).close_container()
    assert format(container1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
            \time 1/4
            g'4
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            a2.
            \time 1/4
            c'4
        }
        """)
    assert format(container3) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 5/4
            g1
            ~
            g4
            \time 2/4
            af'2
        }
        """)


def test_close_container_03():
    container = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4 g'4")
    auxjad.mutate(container).close_container()
    assert format(container) == abjad.String.normalize(
        r"""
        {
            %%% \time 4/4 %%%
            c'4
            d'4
            e'4
            f'4
            %%% \time 1/4 %%%
            g'4
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
            \time 1/4
            g'4
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
                \time 1/4
                g'4
            }
        }
        """)


def test_close_container_04():
    container = abjad.Staff(r"c'4 d'4 e'4 f'4 g'4")
    time_signature = abjad.TimeSignature((3, 4), partial=(1, 4))
    abjad.attach(time_signature, container[0])
    auxjad.mutate(container).close_container()
    assert format(container) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \partial 4
            \time 3/4
            c'4
            d'4
            e'4
            f'4
            \time 1/4
            g'4
        }
        """)


def test_close_container_05():
    container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'1")
    with pytest.raises(ValueError):
        assert auxjad.mutate(container).close_container()
