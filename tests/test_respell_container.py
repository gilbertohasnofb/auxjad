import abjad
import pytest
import auxjad


def test_respell_container_01():
    container = abjad.Container(r"c'4 r4 <ef' e'>4 g'4 <c' cs'>4 r2.")
    auxjad.respell_container(container)
    assert format(container) == abjad.String.normalize(
        r"""
        {
            c'4
            r4
            <ds' e'>4
            g'4
            <c' df'>4
            r2.
        }
        """)


def test_respell_container_02():
    staff = abjad.Staff()
    for pitch in range(12):
        staff.append(abjad.Chord([pitch, pitch + 1], (1, 16)))
    auxjad.respell_container(staff)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            <c' df'>16
            <cs' d'>16
            <d' ef'>16
            <ds' e'>16
            <e' f'>16
            <f' gf'>16
            <fs' g'>16
            <g' af'>16
            <gs' a'>16
            <a' bf'>16
            <as' b'>16
            <b' c''>16
        }
        """)


def test_respell_container_03():
    container = abjad.Container(r"<a c' cs' f'>1")
    auxjad.respell_container(container)
    assert format(container) == abjad.String.normalize(
        r"""
        {
            <a c' df' f'>1
        }
        """)


def test_respell_container_04():
    container = abjad.Container(r"<e' cs' g' ef'>1")
    auxjad.respell_container(container)
    assert format(container) == abjad.String.normalize(
        r"""
        {
            <cs' ds' e' g'>1
        }
        """)


def test_respell_container_05():
    container = abjad.Container(r"<c' cs''>1")
    auxjad.respell_container(container)
    assert format(container) == abjad.String.normalize(
        r"""
        {
            <c' cs''>1
        }
        """)
    auxjad.respell_container(container, include_multiples=True)
    assert format(container) == abjad.String.normalize(
        r"""
        {
            <c' df''>1
        }
        """)


def test_respell_container_06():
    container = abjad.Container(r"<c' cs' cs''>1")
    auxjad.respell_container(container)
    assert format(container) == abjad.String.normalize(
        r"""
        {
            <c' df' cs''>1
        }
        """)
    container = abjad.Container(r"<c' cs' cs''>1")
    auxjad.respell_container(container, respell_by_pitch_class=True)
    assert format(container) == abjad.String.normalize(
        r"""
        {
            <c' df' df''>1
        }
        """)
