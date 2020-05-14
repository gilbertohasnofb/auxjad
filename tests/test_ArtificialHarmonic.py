import abjad
import pytest
import auxjad


def test_ArtificialHarmonic_01():
    chord = auxjad.ArtificialHarmonic("<g c'>4")
    assert chord.style == 'harmonic'
    assert format(chord) == abjad.String.normalize(
    r'''
    <
        g
        \tweak style #'harmonic
        c'
    >4
    ''')


def test_ArtificialHarmonic_02():
    chord1 = auxjad.ArtificialHarmonic("<g c'>4")
    chord2 = auxjad.ArtificialHarmonic(["g", "c'"], 1/4)
    chord3 = auxjad.ArtificialHarmonic([-5, 0], 0.25)
    chord4 = auxjad.ArtificialHarmonic([-5, 0], abjad.Duration(1, 4))
    chords = [chord1, chord2, chord3, chord4]
    for chord in chords:
        assert format(chord) == abjad.String.normalize(
        r'''
        <
            g
            \tweak style #'harmonic
            c'
        >4
        ''')


def test_ArtificialHarmonic_03():
    chord = auxjad.ArtificialHarmonic("<g c'>4",
                                      style='harmonic-mixed',
                                      )
    assert chord.style == 'harmonic-mixed'
    assert format(chord) == abjad.String.normalize(
    r'''
    <
        g
        \tweak style #'harmonic-mixed
        c'
    >4
    ''')


def test_ArtificialHarmonic_04():
    chord = auxjad.ArtificialHarmonic("<g c'>4",
                                      is_parenthesized=True,
                                      )
    assert chord.is_parenthesized
    assert format(chord) == abjad.String.normalize(
    r'''
    <
        \parenthesize
        \tweak ParenthesesItem.font-size #-4
        g
        \tweak style #'harmonic
        c'
    >4
    ''')


def test_ArtificialHarmonic_05():
    chord = auxjad.ArtificialHarmonic("<g c'>4",
                                      multiplier=(2, 3),
                                      )
    assert chord.multiplier == abjad.Multiplier(2, 3)
    assert format(chord) == abjad.String.normalize(
    r'''
    <
        g
        \tweak style #'harmonic
        c'
    >4 * 2/3
    ''')


def test_ArtificialHarmonic_06():
    chord = auxjad.ArtificialHarmonic("<g c'>4")
    assert chord.written_pitches == abjad.PitchSegment("g c'")
    assert chord.written_duration == 1/4
    assert chord.style == 'harmonic'
    assert not chord.is_parenthesized
    chord.written_pitches = [-5, 2]
    chord.written_duration = abjad.Duration(1, 8)
    chord.style = 'harmonic-mixed'
    chord.is_parenthesized = True
    assert chord.written_pitches == abjad.PitchSegment("g d'")
    assert chord.written_duration == 1/8
    assert chord.style == 'harmonic-mixed'
    assert chord.is_parenthesized


def test_ArtificialHarmonic_07():
    with pytest.raises(ValueError):
        assert auxjad.ArtificialHarmonic("<g c' d'>4")


def test_ArtificialHarmonic_08():
    harmonics = [auxjad.ArtificialHarmonic("<g b>4").sounding_pitch(),
                 auxjad.ArtificialHarmonic("<g c'>4").sounding_pitch(),
                 auxjad.ArtificialHarmonic("<g d'>4").sounding_pitch(),
                 auxjad.ArtificialHarmonic("<g e'>4").sounding_pitch(),
                 auxjad.ArtificialHarmonic("<g g'>4").sounding_pitch(),
                 ]
    notes = [abjad.Note("b''4"),
             abjad.Note("g''4"),
             abjad.Note("d''4"),
             abjad.Note("b''4"),
             abjad.Note("g'4"),
             ]
    for harmonic_pitch, note in zip(harmonics, notes):
        assert harmonic_pitch == note.written_pitch


def test_ArtificialHarmonic_09():
    with pytest.raises(KeyError):
        auxjad.ArtificialHarmonic("<g ef'>4").sounding_pitch()


def test_ArtificialHarmonic_10():
    harmonics = [auxjad.ArtificialHarmonic("<g b>4").sounding_note(),
                 auxjad.ArtificialHarmonic("<g c'>4").sounding_note(),
                 auxjad.ArtificialHarmonic("<g d'>4").sounding_note(),
                 auxjad.ArtificialHarmonic("<g e'>4").sounding_note(),
                 auxjad.ArtificialHarmonic("<g g'>4").sounding_note(),
                 ]
    notes = [abjad.Note("b''4"),
             abjad.Note("g''4"),
             abjad.Note("d''4"),
             abjad.Note("b''4"),
             abjad.Note("g'4"),
             ]
    for harmonic, note in zip(harmonics, notes):
        assert harmonic.written_pitch == note.written_pitch
        assert harmonic.written_duration == note.written_duration


def test_ArtificialHarmonic_11():
    note = auxjad.ArtificialHarmonic(r"<g c'>4-.\pp")
    assert format(note.sounding_note()) ==  abjad.String.normalize(
    r'''
    g''4
    \pp
    - \staccato
    ''')


def test_ArtificialHarmonic_12():
    with pytest.raises(KeyError):
        auxjad.ArtificialHarmonic("<g ef'>4").sounding_note()
