import abjad
import pytest
import auxjad


def test_respell_chord_01():
    chord = abjad.Chord("<c' cs'>4")
    auxjad.respell_chord(chord)
    assert format(chord) == abjad.String.normalize(
        r"""
        <c' df'>4
        """)


def test_respell_chord_02():
    staff = abjad.Staff()
    for pitch in range(12):
        chord = abjad.Chord([pitch, pitch + 1], (1, 16))
        auxjad.respell_chord(chord)
        staff.append(chord)
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


def test_respell_chord_03():
    chord = abjad.Chord(r"<a c' cs' f'>1")
    auxjad.respell_chord(chord)
    assert format(chord) == abjad.String.normalize(
        r"""
        <a c' df' f'>1
        """)


def test_respell_chord_04():
    chord = abjad.Chord(r"<e' cs' g' ef'>1")
    auxjad.respell_chord(chord)
    assert format(chord) == abjad.String.normalize(
        r"""
        <cs' ds' e' g'>1
        """)


def test_respell_chord_05():
    chord = abjad.Chord(r"<c' cs''>1")
    auxjad.respell_chord(chord)
    assert format(chord) == abjad.String.normalize(
        r"""
        <c' cs''>1
        """)
    auxjad.respell_chord(chord, include_multiples=True)
    assert format(chord) == abjad.String.normalize(
        r"""
        <c' df''>1
        """)


def test_respell_chord_06():
    chord = abjad.Chord(r"<c' cs' cs''>1")
    auxjad.respell_chord(chord)
    assert format(chord) == abjad.String.normalize(
        r"""
        <c' df' cs''>1
        """)
    chord = abjad.Chord(r"<c' cs' cs''>1")
    auxjad.respell_chord(chord, respell_by_pitch_class=True)
    assert format(chord) == abjad.String.normalize(
        r"""
        <c' df' df''>1
        """)
