import abjad
import pytest

import auxjad


def test_virtual_fundamental_01():
    pitches = abjad.PitchSegment(r"c'' g''")
    fundamental = auxjad.get.virtual_fundamental(pitches)
    assert fundamental == abjad.NamedPitch(r"c'")


def test_virtual_fundamental_02():
    pitches = abjad.PitchSegment(r"c'' e'' g''")
    fundamental = auxjad.get.virtual_fundamental(pitches)
    assert fundamental == abjad.NamedPitch(r"c")


def test_virtual_fundamental_03():
    pitches = abjad.PitchSegment(r"c'' f'' g''")
    fundamental = auxjad.get.virtual_fundamental(pitches)
    assert fundamental == abjad.NamedPitch(r"f,")


def test_virtual_fundamental_04():
    pitches = abjad.PitchSegment(r"c'' d'' ef'' fs''")
    fundamental = auxjad.get.virtual_fundamental(pitches)
    assert fundamental == abjad.NamedPitch(r"bf,,")


def test_virtual_fundamental_05():
    pitches = abjad.PitchSegment(r"c'' cs'' d'' ef'' e'' fs''")
    fundamental = auxjad.get.virtual_fundamental(pitches)
    assert fundamental == abjad.NamedPitch(r"d,,")


def test_virtual_fundamental_06():
    chord = abjad.Chord(r"<c'' cs'' d'' ef'' e'' fs''>4")
    fundamental = auxjad.get.virtual_fundamental(chord)
    assert fundamental == abjad.NamedPitch(r"d,,")


def test_virtual_fundamental_07():
    staff = abjad.Staff(r"r4 <c'' cs'' d'' ef'' e'' fs''>4 r4")
    fundamental = auxjad.get.virtual_fundamental(staff[1])
    assert fundamental == abjad.NamedPitch(r"d,,")


def test_virtual_fundamental_08():
    pitches = abjad.PitchSegment(r"c'' cs'' d'' ef'' e'' fs''")
    fundamental = auxjad.get.virtual_fundamental(
        pitches,
        min_fundamental=abjad.NamedPitch(r"c,,,"),
    )
    assert fundamental == abjad.NamedPitch(r"d,,")


def test_virtual_fundamental_09():
    pitches = abjad.PitchSegment(r"c'' cs'' d'' ef'' e'' fs''")
    fundamental = auxjad.get.virtual_fundamental(
        pitches,
        min_fundamental=abjad.NumberedPitch(-48),
    )
    assert fundamental == abjad.NamedPitch(r"d,,")


def test_virtual_fundamental_10():
    pitches = abjad.PitchSegment(r"c'' cs'' d'' ef'' e'' fs''")
    with pytest.raises(ValueError):
        auxjad.get.virtual_fundamental(
            pitches,
            min_fundamental=abjad.NamedPitch(r"c'"),
        )


def test_virtual_fundamental_11():
    pitches = abjad.PitchSegment(r"c'' g''")
    fundamental = abjad.get.virtual_fundamental(pitches)
    assert fundamental == abjad.NamedPitch(r"c'")
