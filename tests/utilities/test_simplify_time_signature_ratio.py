import abjad

import auxjad


def test_simplify_time_signature_ratio_01():
    time_signature = auxjad.simplify_time_signature_ratio((4, 8))
    assert format(time_signature) == abjad.String.normalize(
        r'abjad.TimeSignature((2, 4))')


def test_simplify_time_signature_ratio_02():
    time_signature = auxjad.simplify_time_signature_ratio((7, 8))
    assert format(time_signature) == abjad.String.normalize(
        r'abjad.TimeSignature((7, 8))')


def test_simplify_time_signature_ratio_03():
    time_signature = auxjad.simplify_time_signature_ratio((4, 8),
                                                          min_denominator=8,
                                                          )
    assert format(time_signature) == abjad.String.normalize(
        r'abjad.TimeSignature((4, 8))')


def test_simplify_time_signature_ratio_04():
    time_signature = auxjad.simplify_time_signature_ratio((4, 8),
                                                          min_denominator=2,
                                                          )
    assert format(time_signature) == abjad.String.normalize(
        r'abjad.TimeSignature((1, 2))')


def test_simplify_time_signature_ratio_05():
    time_signature = auxjad.simplify_time_signature_ratio((1, 1))
    assert format(time_signature) == abjad.String.normalize(
        r'abjad.TimeSignature((4, 4))')


def test_simplify_time_signature_ratio_06():
    time_signature = auxjad.simplify_time_signature_ratio((1, 1),
                                                          min_denominator=1,
                                                          )
    assert format(time_signature) == abjad.String.normalize(
        r'abjad.TimeSignature((1, 1))')


def test_simplify_time_signature_ratio_07():
    arg = (4, 8)
    time_signature = auxjad.simplify_time_signature_ratio(arg)
    assert format(time_signature) == abjad.String.normalize(
        r'abjad.TimeSignature((2, 4))')
    arg = abjad.Duration((4, 8))
    time_signature = auxjad.simplify_time_signature_ratio(arg)
    assert format(time_signature) == abjad.String.normalize(
        r'abjad.TimeSignature((2, 4))')
    arg = abjad.Meter((4, 8))
    time_signature = auxjad.simplify_time_signature_ratio(arg)
    assert format(time_signature) == abjad.String.normalize(
        r'abjad.TimeSignature((2, 4))')
    arg = abjad.TimeSignature((4, 8))
    time_signature = auxjad.simplify_time_signature_ratio(arg)
    assert format(time_signature) == abjad.String.normalize(
        r'abjad.TimeSignature((2, 4))')
    arg = (4, 8)
    pair = auxjad.simplify_time_signature_ratio(arg,
                                                output_pair_of_int=True,
                                                )
    assert pair == (2, 4)
    arg = abjad.Duration((4, 8))
    pair = auxjad.simplify_time_signature_ratio(arg,
                                                output_pair_of_int=True,
                                                )
    assert pair == (2, 4)
    arg = abjad.Meter((4, 8))
    pair = auxjad.simplify_time_signature_ratio(arg,
                                                output_pair_of_int=True,
                                                )
    assert pair == (2, 4)
    arg = abjad.TimeSignature((4, 8))
    pair = auxjad.simplify_time_signature_ratio(arg,
                                                output_pair_of_int=True,
                                                )
    assert pair == (2, 4)
