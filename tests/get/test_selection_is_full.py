import abjad
import pytest

import auxjad


def test_selection_is_full_01():
    container1 = abjad.Container(r"c'4 d'4 e'4 f'4")
    container2 = abjad.Container(r"c'4 d'4 e'4")
    container3 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4")
    container4 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4 d'4 e'4 f'4")
    assert auxjad.get.selection_is_full(container1[:])
    assert not auxjad.get.selection_is_full(container2[:])
    assert not auxjad.get.selection_is_full(container3[:])
    assert auxjad.get.selection_is_full(container4[:])


def test_selection_is_full_02():
    container1 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4")
    container2 = abjad.Container(r"\time 3/4 a2. \time 2/4 r2")
    container3 = abjad.Container(r"\time 5/4 g1 ~ g4 \time 4/4 af'2")
    container4 = abjad.Container(r"\time 6/8 c'2 ~ c'8")
    assert auxjad.get.selection_is_full(container1[:])
    assert auxjad.get.selection_is_full(container2[:])
    assert not auxjad.get.selection_is_full(container3[:])
    assert not auxjad.get.selection_is_full(container4[:])


def test_selection_is_full_03():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    time_signature = abjad.TimeSignature((3, 4), partial=(1, 4))
    abjad.attach(time_signature, container[0])
    assert auxjad.get.selection_is_full(container[:])


def test_selection_is_full_04():
    container1 = abjad.Container(r"R1")
    container2 = abjad.Container(r"\time 3/4 R1 * 3/4 \time 2/4 r2")
    container3 = abjad.Container(r"\time 5/4 R1 * 5/4 \time 4/4 g''4")
    container4 = abjad.Container(r"\time 6/8 R1 * 1/2")
    assert auxjad.get.selection_is_full(container1[:])
    assert auxjad.get.selection_is_full(container2[:])
    assert not auxjad.get.selection_is_full(container3[:])
    assert not auxjad.get.selection_is_full(container4[:])


def test_selection_is_full_05():
    container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'1")
    with pytest.raises(ValueError):
        auxjad.get.selection_is_full(container[:])


def test_selection_is_full_06():
    container1 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4")
    container2 = abjad.Container(r"\time 3/4 a2. \time 2/4 r2")
    container3 = abjad.Container(r"\time 5/4 g1 ~ g4 \time 4/4 af'2")
    container4 = abjad.Container(r"\time 6/8 c'2 ~ c'8")
    assert abjad.get.selection_is_full(container1[:])
    assert abjad.get.selection_is_full(container2[:])
    assert not abjad.get.selection_is_full(container3[:])
    assert not abjad.get.selection_is_full(container4[:])
