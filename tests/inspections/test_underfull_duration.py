import abjad
import pytest

import auxjad


def test_underfull_duration_01():
    container1 = abjad.Container(r"c'4 d'4 e'4 f'4")
    container2 = abjad.Container(r"c'4 d'4 e'4")
    container3 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4")
    container4 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4 d'4 e'4 f'4")
    assert auxjad.inspect(container1[:]).underfull_duration() == 0
    assert auxjad.inspect(container2[:]).underfull_duration() == 1 / 4
    assert auxjad.inspect(container3[:]).underfull_duration() == 3 / 4
    assert auxjad.inspect(container4[:]).underfull_duration() == 0


def test_underfull_duration_02():
    container1 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4")
    container2 = abjad.Container(r"\time 3/4 a2. \time 2/4 r2")
    container3 = abjad.Container(r"\time 5/4 g1 ~ g4 \time 4/4 af'2")
    container4 = abjad.Container(r"\time 6/8 c'2 ~ c'8")
    assert auxjad.inspect(container1[:]).underfull_duration() == 0
    assert auxjad.inspect(container2[:]).underfull_duration() == 0
    assert auxjad.inspect(container3[:]).underfull_duration() == 1 / 2
    assert auxjad.inspect(container4[:]).underfull_duration() == 1 / 8


def test_underfull_duration_03():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    time_signature = abjad.TimeSignature((3, 4), partial=(1, 4))
    abjad.attach(time_signature, container[0])
    assert auxjad.inspect(container[:]).underfull_duration() == 0


def test_underfull_duration_04():
    container1 = abjad.Container(r"R1")
    container2 = abjad.Container(r"\time 3/4 R1*3/4 \time 2/4 r2")
    container3 = abjad.Container(r"\time 5/4 R1*5/4 \time 4/4 g''4")
    container4 = abjad.Container(r"\time 6/8 R1*1/2")
    assert auxjad.inspect(container1[:]).underfull_duration() == 0
    assert auxjad.inspect(container2[:]).underfull_duration() == 0
    assert auxjad.inspect(container3[:]).underfull_duration() == 3 / 4
    assert auxjad.inspect(container4[:]).underfull_duration() == 1 / 4


def test_underfull_duration_05():
    container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'1")
    with pytest.raises(ValueError):
        assert auxjad.inspect(container[:]).underfull_duration()


def test_underfull_duration_06():
    container1 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4")
    container2 = abjad.Container(r"\time 3/4 a2. \time 2/4 r2")
    container3 = abjad.Container(r"\time 5/4 g1 ~ g4 \time 4/4 af'2")
    container4 = abjad.Container(r"\time 6/8 c'2 ~ c'8")
    assert abjad.inspect(container1[:]).underfull_duration() == 0
    assert abjad.inspect(container2[:]).underfull_duration() == 0
    assert abjad.inspect(container3[:]).underfull_duration() == 1 / 2
    assert abjad.inspect(container4[:]).underfull_duration() == 1 / 8
