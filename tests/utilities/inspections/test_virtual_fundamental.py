import abjad
import pytest

import auxjad


def test_virtual_fundamental_01():
    pitches = abjad.PitchSegment(r"c'' g''")
    fundamental = auxjad.inspect(pitches).virtual_fundamental()
    assert fundamental == abjad.NamedPitch(r"c'")


def test_virtual_fundamental_02():
    pitches = abjad.PitchSegment(r"c'' e'' g''")
    fundamental = auxjad.inspect(pitches).virtual_fundamental()
    assert fundamental == abjad.NamedPitch(r"c")


def test_virtual_fundamental_03():
    pitches = abjad.PitchSegment(r"c'' f'' g''")
    fundamental = auxjad.inspect(pitches).virtual_fundamental()
    assert fundamental == abjad.NamedPitch(r"f,")


def test_virtual_fundamental_04():
    pitches = abjad.PitchSegment(r"c'' d'' ef'' fs''")
    fundamental = auxjad.inspect(pitches).virtual_fundamental()
    assert fundamental == abjad.NamedPitch(r"bf,,")


def test_virtual_fundamental_05():
    pitches = abjad.PitchSegment(r"c'' cs'' d'' ef'' e'' fs''")
    fundamental = auxjad.inspect(pitches).virtual_fundamental()
    assert fundamental == abjad.NamedPitch(r"d,,")


def test_virtual_fundamental_06():
    chord = abjad.Chord(r"<c'' cs'' d'' ef'' e'' fs''>4")
    fundamental = auxjad.inspect(chord).virtual_fundamental()
    assert fundamental == abjad.NamedPitch(r"d,,")


def test_virtual_fundamental_07():
    staff = abjad.Staff(r"r4 <c'' cs'' d'' ef'' e'' fs''>4 r4")
    fundamental = auxjad.inspect(staff[1]).virtual_fundamental()
    assert fundamental == abjad.NamedPitch(r"d,,")


def test_virtual_fundamental_08():
    pitches = abjad.PitchSegment(r"c'' cs'' d'' ef'' e'' fs''")
    fundamental = auxjad.inspect(pitches).virtual_fundamental(
        min_fundamental=abjad.NamedPitch(r"c,,,")
    )
    assert fundamental == abjad.NamedPitch(r"d,,")


def test_virtual_fundamental_09():
    pitches = abjad.PitchSegment(r"c'' cs'' d'' ef'' e'' fs''")
    fundamental = auxjad.inspect(pitches).virtual_fundamental(
        min_fundamental=abjad.NumberedPitch(-48)
    )
    assert fundamental == abjad.NamedPitch(r"d,,")


def test_virtual_fundamental_10():
    pitches = abjad.PitchSegment(r"c'' cs'' d'' ef'' e'' fs''")
    with pytest.raises(ValueError):
        auxjad.inspect(pitches).virtual_fundamental(
            min_fundamental=abjad.NamedPitch(r"c'")
        )
