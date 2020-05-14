import abjad
import pytest
import auxjad


def test_HarmonicNote_01():
    note = auxjad.HarmonicNote("c''4")
    assert note.style == 'harmonic'
    assert format(note) == abjad.String.normalize(
    r'''
    \tweak style #'harmonic
    c''4
    ''')


def test_HarmonicNote_02():
    note1 = auxjad.HarmonicNote("c''4")
    note2 = auxjad.HarmonicNote("c''", 1/4)
    note3 = auxjad.HarmonicNote(12, 0.25)
    note4 = auxjad.HarmonicNote(12, abjad.Duration(1, 4))
    notes = [note1, note2, note3, note4]
    for note in notes:
        assert format(note) == abjad.String.normalize(
        r'''
        \tweak style #'harmonic
        c''4
        ''')


def test_HarmonicNote_03():
    note = auxjad.HarmonicNote("c''4",
                               style='harmonic-mixed',
                               )
    assert note.style == 'harmonic-mixed'
    assert format(note) == abjad.String.normalize(
    r'''
    \tweak style #'harmonic-mixed
    c''4
    ''')


def test_HarmonicNote_04():
    note = auxjad.HarmonicNote("c''4",
                               multiplier=(2, 3),
                               )
    assert note.multiplier == abjad.Multiplier(2, 3)
    assert format(note) == abjad.String.normalize(
    r'''
    \tweak style #'harmonic
    c''4 * 2/3
    ''')


def test_HarmonicNote_05():
    note = auxjad.HarmonicNote("c''4")
    assert note.written_pitch == "c''"
    assert note.written_duration == 1/4
    assert note.style == 'harmonic'
    note.written_pitch = 18
    note.written_duration = abjad.Duration(1, 8)
    note.style = 'harmonic-mixed'
    assert note.written_pitch == "fs''"
    assert note.written_duration == 1/8
    assert note.style == 'harmonic-mixed'


def test_HarmonicNote_06():
    note = auxjad.HarmonicNote("c''1",
                               style='flageolet',
                               )
    assert note.style == 'flageolet'
    assert format(note) == abjad.String.normalize(
    r'''
    c''1
    \flageolet
    ''')
