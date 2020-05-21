import abjad
import pytest
import auxjad


def test_repeat_container_01():
    container = abjad.Container(r"c'4 d'4 e'4")
    output_container = auxjad.repeat_container(container, 3)
    assert format(output_container) == abjad.String.normalize(
        r"""
        {
            %%% \time 3/4 %%%
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
        }
        """)
    staff = abjad.Staff([output_container])
    assert format(output_container) == abjad.String.normalize(
        r"""
        {
            \time 3/4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
        }
        """)


def test_repeat_container_02():
    container = abjad.Container(r"\time 3/4 c'2. \time 2/4 r2 g'2")
    output_container = auxjad.repeat_container(container, 3)
    assert format(output_container) == abjad.String.normalize(
        r"""
        {
            %%% \time 3/4 %%%
            c'2.
            %%% \time 2/4 %%%
            r2
            g'2
            %%% \time 3/4 %%%
            c'2.
            %%% \time 2/4 %%%
            r2
            g'2
            %%% \time 3/4 %%%
            c'2.
            %%% \time 2/4 %%%
            r2
            g'2
        }
        """)


def test_repeat_container_03():
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 f'2")
    output_container = auxjad.repeat_container(container, 2)
    assert format(output_container) == abjad.String.normalize(
        r"""
        {
            %%% \time 3/4 %%%
            c'4
            d'4
            e'4
            %%% \time 2/4 %%%
            f'2
            %%% \time 3/4 %%%
            c'4
            d'4
            e'4
            %%% \time 2/4 %%%
            f'2
        }
        """)


def test_repeat_container_04():
    container = abjad.Container(r"c'4 d'4 e'4")
    output_container = auxjad.repeat_container(container,
                                               3,
                                               omit_all_time_signatures=True,
                                               )
    assert format(output_container) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
        }
        """)


def test_repeat_container_05():
    container = abjad.Container(r"\time 5/4 c'2. d'4 e'4")
    output_container = auxjad.repeat_container(
        container,
        3,
        force_identical_time_signatures=True,
    )
    assert format(output_container) == abjad.String.normalize(
        r"""
        {
            %%% \time 5/4 %%%
            c'2.
            d'4
            e'4
            %%% \time 5/4 %%%
            c'2.
            d'4
            e'4
            %%% \time 5/4 %%%
            c'2.
            d'4
            e'4
        }
        """)


def test_repeat_container_06():
    container = abjad.Staff(r"c'4 d'4 e'4")
    output_staff = auxjad.repeat_container(container, 3)
    assert format(output_staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
        }
        """)


def test_repeat_container_07():
    container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'1")
    with pytest.raises(ValueError):
        assert auxjad.repeat_container(container, 4)
