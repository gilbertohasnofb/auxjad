import abjad
import pytest

import auxjad


def test_ArtificialHarmonic_01():
    harm = auxjad.ArtificialHarmonic(r"<g c'>4")
    assert harm.style == 'harmonic'
    assert format(harm) == abjad.String.normalize(
        r"""
        <
            g
            \tweak style #'harmonic
            c'
        >4
        """)


def test_ArtificialHarmonic_02():
    harm1 = auxjad.ArtificialHarmonic(r"<g c'>4")
    harm2 = auxjad.ArtificialHarmonic(["g", "c'"], 1 / 4)
    harm3 = auxjad.ArtificialHarmonic([-5, 0], 0.25)
    harm4 = auxjad.ArtificialHarmonic([-5, 0], abjad.Duration(1, 4))
    harms = [harm1, harm2, harm3, harm4]
    for harm in harms:
        assert format(harm) == abjad.String.normalize(
            r"""
            <
                g
                \tweak style #'harmonic
                c'
            >4
            """)


def test_ArtificialHarmonic_03():
    harm = auxjad.ArtificialHarmonic(r"<g c'>4",
                                     style='harmonic-mixed',
                                     )
    assert harm.style == 'harmonic-mixed'
    assert format(harm) == abjad.String.normalize(
        r"""
        <
            g
            \tweak style #'harmonic-mixed
            c'
        >4
        """)


def test_ArtificialHarmonic_04():
    harm = auxjad.ArtificialHarmonic(r"<g c'>4",
                                     is_parenthesized=True,
                                     )
    assert harm.is_parenthesized
    assert format(harm) == abjad.String.normalize(
        r"""
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >4
        """)


def test_ArtificialHarmonic_05():
    harm = auxjad.ArtificialHarmonic(r"<g c'>4",
                                     multiplier=(2, 3),
                                     )
    assert harm.multiplier == abjad.Multiplier(2, 3)
    assert format(harm) == abjad.String.normalize(
        r"""
        <
            g
            \tweak style #'harmonic
            c'
        >4 * 2/3
        """)


def test_ArtificialHarmonic_06():
    harm = auxjad.ArtificialHarmonic(r"<g c'>4")
    assert harm.written_pitches == abjad.PitchSegment(r"g c'")
    assert harm.written_duration == 1 / 4
    assert harm.style == 'harmonic'
    assert not harm.is_parenthesized
    harm.written_pitches = [-5, 2]
    harm.written_duration = abjad.Duration(1, 8)
    harm.style = 'harmonic-mixed'
    harm.is_parenthesized = True
    assert harm.written_pitches == abjad.PitchSegment(r"g d'")
    assert harm.written_duration == 1 / 8
    assert harm.style == 'harmonic-mixed'
    assert harm.is_parenthesized


def test_ArtificialHarmonic_07():
    with pytest.raises(ValueError):
        auxjad.ArtificialHarmonic(r"<g c' d'>4")


def test_ArtificialHarmonic_08():
    harmonics = [auxjad.ArtificialHarmonic(r"<g b>4").sounding_pitch(),
                 auxjad.ArtificialHarmonic(r"<g c'>4").sounding_pitch(),
                 auxjad.ArtificialHarmonic(r"<g d'>4").sounding_pitch(),
                 auxjad.ArtificialHarmonic(r"<g e'>4").sounding_pitch(),
                 auxjad.ArtificialHarmonic(r"<g g'>4").sounding_pitch(),
                 ]
    notes = [abjad.Note(r"b''4"),
             abjad.Note(r"g''4"),
             abjad.Note(r"d''4"),
             abjad.Note(r"b''4"),
             abjad.Note(r"g'4"),
             ]
    for harmonic_pitch, note in zip(harmonics, notes):
        assert harmonic_pitch == note.written_pitch


def test_ArtificialHarmonic_09():
    with pytest.raises(ValueError):
        auxjad.ArtificialHarmonic(r"<g ef'>4").sounding_pitch()


def test_ArtificialHarmonic_10():
    harmonics = [auxjad.ArtificialHarmonic(r"<g b>4").sounding_note(),
                 auxjad.ArtificialHarmonic(r"<g c'>4").sounding_note(),
                 auxjad.ArtificialHarmonic(r"<g d'>4").sounding_note(),
                 auxjad.ArtificialHarmonic(r"<g e'>4").sounding_note(),
                 auxjad.ArtificialHarmonic(r"<g g'>4").sounding_note(),
                 ]
    notes = [abjad.Note(r"b''4"),
             abjad.Note(r"g''4"),
             abjad.Note(r"d''4"),
             abjad.Note(r"b''4"),
             abjad.Note(r"g'4"),
             ]
    for harmonic, note in zip(harmonics, notes):
        assert harmonic.written_pitch == note.written_pitch
        assert harmonic.written_duration == note.written_duration


def test_ArtificialHarmonic_11():
    harm = auxjad.ArtificialHarmonic(r"<g c'>4-.\pp")
    assert format(harm.sounding_note()) == abjad.String.normalize(
        r"""
        g''4
        \pp
        - \staccato
        """)


def test_ArtificialHarmonic_12():
    with pytest.raises(ValueError):
        auxjad.ArtificialHarmonic(r"<g ef'>4").sounding_note()


def test_ArtificialHarmonic_13():
    harm = auxjad.ArtificialHarmonic(r"<g c'>4")
    assert harm.written_pitches == abjad.PitchSegment(r"g c'")
    harm.written_pitches = r"a d'"
    assert harm.written_pitches == abjad.PitchSegment(r"a d'")
    with pytest.raises(ValueError):
        harm.written_pitches = r"a d' e'"


def test_ArtificialHarmonic_14():
    harm1 = auxjad.ArtificialHarmonic(r"<a d'>1")
    harm2 = auxjad.ArtificialHarmonic(r"<a d'>1",
                                      markup='I.',
                                      )
    harm3 = auxjad.ArtificialHarmonic(r"<a d'>1",
                                      markup='I.',
                                      direction=abjad.Down)
    staff = abjad.Staff([harm1, harm2, harm3])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            <
                a
                \tweak style #'harmonic
                d'
            >1
            <
                a
                \tweak style #'harmonic
                d'
            >1
            ^ \markup { I. }
            <
                a
                \tweak style #'harmonic
                d'
            >1
            _ \markup { I. }
        }
        """)


def test_ArtificialHarmonic_15():
    harm = auxjad.ArtificialHarmonic(r"<a d'>1",
                                     markup='I.',
                                     )
    harm.markup = None
    assert format(harm) == abjad.String.normalize(
        r"""
        <
            a
            \tweak style #'harmonic
            d'
        >1
        """)


def test_ArtificialHarmonic_16():
    harm = auxjad.ArtificialHarmonic(r"<a d'>1")
    abjad.attach(abjad.Markup('test'), harm)
    harm.markup = 'I.'
    with pytest.raises(Exception):
        harm.markup = None


def test_ArtificialHarmonic_17():
    harm = auxjad.ArtificialHarmonic(r"<a d'>1",
                                     markup='I.',
                                     direction=abjad.Down)
    assert harm.direction is abjad.Down
    assert format(harm) == abjad.String.normalize(
        r"""
        <
            a
            \tweak style #'harmonic
            d'
        >1
        _ \markup { I. }
        """)
    harm.direction = abjad.Up
    assert harm.direction is abjad.Up
    assert format(harm) == abjad.String.normalize(
        r"""
        <
            a
            \tweak style #'harmonic
            d'
        >1
        ^ \markup { I. }
        """)
