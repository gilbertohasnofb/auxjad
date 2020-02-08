import abjad
import auxjad


def test_simplified_time_signature_ratio_01():
    ratio = auxjad.simplified_time_signature_ratio((4, 8))
    time_signature = abjad.TimeSignature(ratio)
    assert format(time_signature) == abjad.String.normalize(
        r'''abjad.TimeSignature((2, 4))''')


def test_simplified_time_signature_ratio_02():
    ratio = auxjad.simplified_time_signature_ratio((7, 8))
    time_signature = abjad.TimeSignature(ratio)
    assert format(time_signature) == abjad.String.normalize(
        r'''abjad.TimeSignature((7, 8))''')


def test_simplified_time_signature_ratio_03():
    ratio = auxjad.simplified_time_signature_ratio((4, 8), min_denominator=8)
    time_signature = abjad.TimeSignature(ratio)
    assert format(time_signature) == abjad.String.normalize(
        r'''abjad.TimeSignature((4, 8))''')


def test_simplified_time_signature_ratio_04():
    ratio = auxjad.simplified_time_signature_ratio((4, 8), min_denominator=2)
    time_signature = abjad.TimeSignature(ratio)
    assert format(time_signature) == abjad.String.normalize(
        r'''abjad.TimeSignature((1, 2))''')
