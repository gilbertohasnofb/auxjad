import abjad

import auxjad


def test_selections_are_identical_01():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    selections = [container1[:], container2[:]]
    assert auxjad.get.selections_are_identical(selections)


def test_selections_are_identical_02():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container3 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container4 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    selections = [container1[:], container2[:], container3[:], container4[:]]
    assert auxjad.get.selections_are_identical(selections)
    container3 = abjad.Staff(r"cs'''4 d'4 e'4 f'4 <g' a'>2 r2")
    selections = [container1[:], container2[:], container3[:], container4[:]]
    assert not auxjad.get.selections_are_identical(selections)


def test_selections_are_identical_03():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"\times 3/2 {c'4 d'4 e'4} f'4 <g' a'>2 r2")
    selections = [container1[:], container2[:]]
    assert not auxjad.get.selections_are_identical(selections)


def test_selections_are_identical_04():
    container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    selections = [container1[:], container2[:]]
    assert not auxjad.get.selections_are_identical(selections)


def test_selections_are_identical_05():
    container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    selections = [container1[:], container2[:]]
    assert auxjad.get.selections_are_identical(
        selections,
        include_indicators=False,
    )


def test_selections_are_identical_06():
    container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
    container2 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
    selections = [container1[:], container2[:]]
    assert auxjad.get.selections_are_identical(
        selections,
        include_indicators=True,
    )


def test_selections_are_identical_07():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{d'4} e'4 f'4 <g' a'>2 r2")
    selections = [container1[:], container2[:]]
    assert not auxjad.get.selections_are_identical(selections)


def test_selections_are_identical_08():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2")
    selections = [container1[:], container2[:]]
    assert not auxjad.get.selections_are_identical(selections)


def test_selections_are_identical_09():
    container1 = abjad.Staff(r"c'4 \grace{c''16} d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{c''16} d'4 e'4 f'4 <g' a'>2 r2")
    selections = [container1[:], container2[:]]
    assert auxjad.get.selections_are_identical(selections)


def test_selections_are_identical_10():
    container1 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{c''8} d'4 e'4 f'4 <g' a'>2 r2")
    selection1 = abjad.select(container1)  # x[:] doesn't include graces
    selection2 = abjad.select(container2)
    selections = [selection1, selection2]
    assert not auxjad.get.selections_are_identical(selections)


def test_selections_are_identical_11():
    container1 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{b4} d'4 e'4 f'4 <g' a'>2 r2")
    selection1 = abjad.select(container1)  # x[:] doesn't include graces
    selection2 = abjad.select(container2)
    selections = [selection1, selection2]
    assert not auxjad.get.selections_are_identical(selections)


def test_selections_are_identical_12():
    container1 = abjad.Container(r"c'4 d'4 e'4 f'4")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4")
    selections = [container1[:], container2[:]]
    assert auxjad.get.selections_are_identical(selections)


def test_selections_are_identical_13():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    selections = [container1[:], container2[:]]
    assert abjad.get.selections_are_identical(selections)


def test_selections_are_identical_14():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4")
    abjad.piano_pedal(container1[:])
    abjad.piano_pedal(container2[:])
    selections = [container1[:], container2[:]]
    assert auxjad.get.selections_are_identical(selections)


def test_selections_are_identical_15():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4")
    abjad.piano_pedal(container1[:])
    abjad.piano_pedal(container2[:-2])
    selections = [container1[:], container2[:]]
    assert not auxjad.get.selections_are_identical(selections)


def test_selections_are_identical_16():
    container1 = abjad.Staff(r"c'4 c'4 d'4 e'4")
    container2 = abjad.Staff(r"c'4 ~ c'4 d'4 e'4")
    selections = [container1[:], container2[:]]
    assert not auxjad.get.selections_are_identical(selections)
    selections = [container2[:], container1[:]]
    assert not auxjad.get.selections_are_identical(selections)
