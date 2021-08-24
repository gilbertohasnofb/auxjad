import abjad
import pytest

import auxjad


def test_HarmonicNote_01():
    harm = auxjad.HarmonicNote(r"c''4")
    assert harm.style == "#'harmonic"
    assert abjad.lilypond(harm) == abjad.String.normalize(
        r"""
        \tweak style #'harmonic
        c''4
        """
    )


def test_HarmonicNote_02():
    harm1 = auxjad.HarmonicNote(r"c''4")
    harm2 = auxjad.HarmonicNote(r"c''", 1 / 4)
    harm3 = auxjad.HarmonicNote(12, 0.25)
    harm4 = auxjad.HarmonicNote(12, abjad.Duration(1, 4))
    harms = [harm1, harm2, harm3, harm4]
    for harm in harms:
        assert abjad.lilypond(harm) == abjad.String.normalize(
            r"""
            \tweak style #'harmonic
            c''4
            """
        )


def test_HarmonicNote_03():
    harm = auxjad.HarmonicNote(r"c''4",
                               style="#'harmonic-mixed",
                               )
    assert harm.style == "#'harmonic-mixed"
    assert abjad.lilypond(harm) == abjad.String.normalize(
        r"""
        \tweak style #'harmonic-mixed
        c''4
        """
    )


def test_HarmonicNote_04():
    harm = auxjad.HarmonicNote(r"c''4",
                               multiplier=(2, 3),
                               )
    assert harm.multiplier == abjad.Multiplier(2, 3)
    assert abjad.lilypond(harm) == abjad.String.normalize(
        r"""
        \tweak style #'harmonic
        c''4 * 2/3
        """
    )


def test_HarmonicNote_05():
    harm = auxjad.HarmonicNote(r"c''4")
    assert harm.written_pitch == "c''"
    assert harm.written_duration == 1 / 4
    assert harm.style == "#'harmonic"
    harm.written_pitch = 18
    harm.written_duration = abjad.Duration(1, 8)
    harm.style = "#'harmonic-mixed"
    assert harm.written_pitch == "fs''"
    assert harm.written_duration == 1 / 8
    assert harm.style == "#'harmonic-mixed"


def test_HarmonicNote_06():
    harm = auxjad.HarmonicNote(r"c''1",
                               style='flageolet',
                               )
    assert harm.style == 'flageolet'
    assert abjad.lilypond(harm) == abjad.String.normalize(
        r"""
        c''1
        \flageolet
        """
    )


def test_HarmonicNote_07():
    harm1 = auxjad.HarmonicNote(r"d''1")
    harm2 = auxjad.HarmonicNote(r"d''1",
                                markup='III.',
                                )
    harm3 = auxjad.HarmonicNote(r"d''1",
                                markup='III.',
                                direction=abjad.Down)
    staff = abjad.Staff([harm1, harm2, harm3])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \tweak style #'harmonic
            d''1
            \once \override TextScript.parent-alignment-X = 0
            \once \override TextScript.self-alignment-X = 0
            \tweak style #'harmonic
            d''1
            ^ \markup { III. }
            \once \override TextScript.parent-alignment-X = 0
            \once \override TextScript.self-alignment-X = 0
            \tweak style #'harmonic
            d''1
            _ \markup { III. }
        }
        """
    )


def test_HarmonicNote_08():
    harm = auxjad.HarmonicNote(r"d''1",
                               markup='III.',
                               )
    harm.markup = None
    assert abjad.lilypond(harm) == abjad.String.normalize(
        r"""
        \tweak style #'harmonic
        d''1
        """
    )


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
    assert abjad.lilypond(harm) == abjad.String.normalize(
        r"""
        \once \override TextScript.parent-alignment-X = 0
        \once \override TextScript.self-alignment-X = 0
        \tweak style #'harmonic
        d''1
        _ \markup { III. }
        """
    )
    harm.direction = abjad.Up
    assert harm.direction is abjad.Up
    assert abjad.lilypond(harm) == abjad.String.normalize(
        r"""
        \once \override TextScript.parent-alignment-X = 0
        \once \override TextScript.self-alignment-X = 0
        \tweak style #'harmonic
        d''1
        ^ \markup { III. }
        """
    )


def test_HarmonicNote_11():
    harm1 = auxjad.HarmonicNote(r"d''1")
    harm2 = auxjad.HarmonicNote(r"d''1",
                                markup='III.',
                                )
    harm3 = auxjad.HarmonicNote(r"d''1",
                                markup='III.',
                                centre_markup=True,
                                )
    harm4 = auxjad.HarmonicNote(r"d''1",
                                markup='III.',
                                centre_markup=False,
                                )
    assert abjad.lilypond(harm1) == abjad.String.normalize(
        r"""
        \tweak style #'harmonic
        d''1
        """
    )
    assert abjad.lilypond(harm2) == abjad.String.normalize(
        r"""
        \once \override TextScript.parent-alignment-X = 0
        \once \override TextScript.self-alignment-X = 0
        \tweak style #'harmonic
        d''1
        ^ \markup { III. }
        """
    )
    assert abjad.lilypond(harm3) == abjad.String.normalize(
        r"""
        \once \override TextScript.parent-alignment-X = 0
        \once \override TextScript.self-alignment-X = 0
        \tweak style #'harmonic
        d''1
        ^ \markup { III. }
        """
    )
    assert abjad.lilypond(harm4) == abjad.String.normalize(
        r"""
        \tweak style #'harmonic
        d''1
        ^ \markup { III. }
        """
    )


def test_HarmonicNote_12():
    harm = auxjad.HarmonicNote(r"c''1",
                               style='flageolet',
                               )
    assert harm.style == 'flageolet'
    assert abjad.lilypond(harm) == abjad.String.normalize(
        r"""
        c''1
        \flageolet
        """
    )
    harm = auxjad.HarmonicNote(r"c''1",
                               style=r'\flageolet',
                               )
    assert harm.style == r'\flageolet'
    assert abjad.lilypond(harm) == abjad.String.normalize(
        r"""
        c''1
        \flageolet
        """
    )
    harm = auxjad.HarmonicNote(r"c''1",
                               style="#'flageolet",
                               )
    assert harm.style == "#'flageolet"
    assert abjad.lilypond(harm) == abjad.String.normalize(
        r"""
        c''1
        \flageolet
        """
    )
