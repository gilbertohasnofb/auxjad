import abjad
import pytest

import auxjad


def test_HarmonicNote_01():
    harm = auxjad.HarmonicNote(r"c''4")
    assert harm.style == 'harmonic'
    assert format(harm) == abjad.String.normalize(
        r"""
        \tweak style #'harmonic
        c''4
        """)


def test_HarmonicNote_02():
    harm1 = auxjad.HarmonicNote(r"c''4")
    harm2 = auxjad.HarmonicNote(r"c''", 1 / 4)
    harm3 = auxjad.HarmonicNote(12, 0.25)
    harm4 = auxjad.HarmonicNote(12, abjad.Duration(1, 4))
    harms = [harm1, harm2, harm3, harm4]
    for harm in harms:
        assert format(harm) == abjad.String.normalize(
            r"""
            \tweak style #'harmonic
            c''4
            """)


def test_HarmonicNote_03():
    harm = auxjad.HarmonicNote(r"c''4",
                               style='harmonic-mixed',
                               )
    assert harm.style == 'harmonic-mixed'
    assert format(harm) == abjad.String.normalize(
        r"""
        \tweak style #'harmonic-mixed
        c''4
        """)


def test_HarmonicNote_04():
    harm = auxjad.HarmonicNote(r"c''4",
                               multiplier=(2, 3),
                               )
    assert harm.multiplier == abjad.Multiplier(2, 3)
    assert format(harm) == abjad.String.normalize(
        r"""
        \tweak style #'harmonic
        c''4 * 2/3
        """)


def test_HarmonicNote_05():
    harm = auxjad.HarmonicNote(r"c''4")
    assert harm.written_pitch == "c''"
    assert harm.written_duration == 1 / 4
    assert harm.style == 'harmonic'
    harm.written_pitch = 18
    harm.written_duration = abjad.Duration(1, 8)
    harm.style = 'harmonic-mixed'
    assert harm.written_pitch == "fs''"
    assert harm.written_duration == 1 / 8
    assert harm.style == 'harmonic-mixed'


def test_HarmonicNote_06():
    harm = auxjad.HarmonicNote(r"c''1",
                               style='flageolet',
                               )
    assert harm.style == 'flageolet'
    assert format(harm) == abjad.String.normalize(
        r"""
        c''1
        \flageolet
        """)


def test_HarmonicNote_07():
    harm1 = auxjad.HarmonicNote(r"d''1")
    harm2 = auxjad.HarmonicNote(r"d''1",
                                markup='III.',
                                )
    harm3 = auxjad.HarmonicNote(r"d''1",
                                markup='III.',
                                direction=abjad.Down)
    staff = abjad.Staff([harm1, harm2, harm3])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \tweak style #'harmonic
            d''1
            \tweak style #'harmonic
            d''1
            ^ \markup { III. }
            \tweak style #'harmonic
            d''1
            _ \markup { III. }
        }
        """)


def test_HarmonicNote_08():
    harm = auxjad.HarmonicNote(r"d''1",
                               markup='III.',
                               )
    harm.markup = None
    assert format(harm) == abjad.String.normalize(
        r"""
        \tweak style #'harmonic
        d''1
        """)


def test_HarmonicNote_09():
    harm = auxjad.HarmonicNote(r"d''1")
    abjad.attach(abjad.Markup('test'), harm)
    harm.markup = 'III.'
    with pytest.raises(Exception):
        harm.markup = None


def test_HarmonicNote_10():
    harm = auxjad.HarmonicNote(r"d''1",
                               markup='III.',
                               direction=abjad.Down)
    assert harm.direction is abjad.Down
    assert format(harm) == abjad.String.normalize(
        r"""
        \tweak style #'harmonic
        d''1
        _ \markup { III. }
        """)
    harm.direction = abjad.Up
    assert harm.direction is abjad.Up
    assert format(harm) == abjad.String.normalize(
        r"""
        \tweak style #'harmonic
        d''1
        ^ \markup { III. }
        """)
