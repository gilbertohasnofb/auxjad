import abjad

import auxjad


def test_TimeSignature_01():
    time_signature = auxjad.TimeSignature((4, 8))
    time_signature.simplify_ratio()
    assert time_signature.pair == (2, 4)


def test_TimeSignature_02():
    time_signature = auxjad.TimeSignature((7, 8))
    time_signature.simplify_ratio()
    assert time_signature.pair == (7, 8)


def test_TimeSignature_03():
    time_signature = auxjad.TimeSignature((10, 16))
    time_signature.simplify_ratio()
    assert time_signature.pair == (5, 8)


def test_TimeSignature_04():
    time_signature = auxjad.TimeSignature((4, 8))
    time_signature.simplify_ratio(min_denominator=8)
    assert time_signature.pair == (4, 8)


def test_TimeSignature_05():
    time_signature = auxjad.TimeSignature((4, 8))
    time_signature.simplify_ratio(min_denominator=2)
    assert time_signature.pair == (1, 2)


def test_TimeSignature_06():
    time_signature = auxjad.TimeSignature((1, 1))
    time_signature.simplify_ratio()
    assert time_signature.pair == (4, 4)


def test_TimeSignature_07():
    time_signature = auxjad.TimeSignature((1, 1))
    time_signature.simplify_ratio(min_denominator=1)
    assert time_signature.pair == (1, 1)


def test_TimeSignature_08():
    time_signature = auxjad.TimeSignature((8, 8))
    time_signature.simplify_ratio()
    assert time_signature.pair == (4, 4)


def test_TimeSignature_09():
    assert (auxjad.TimeSignature.simplify_ratio
            is abjad.TimeSignature.simplify_ratio)
