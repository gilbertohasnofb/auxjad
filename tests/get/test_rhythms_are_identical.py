import abjad

import auxjad


def test_rhythms_are_identical_01():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
    container2 = abjad.Staff(r"c''4 b'4 a'4 g'4")
    selections = [container1[:], container2[:]]
    assert auxjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_02():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
    container2 = abjad.Staff(r"c''4. b'8 a'4 g'4")
    selections = [container1[:], container2[:]]
    assert not auxjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_03():
    container1 = abjad.Staff(r"c'4. d'8 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c''4. r8 <b' a'>4 r4 g'2 f'2")
    selections = [container1[:], container2[:]]
    assert auxjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_04():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c''4 r4 <b' a'>4 r4 g'2 f'2")
    container3 = abjad.Staff(r"c'''4 c'''4 b''4 b''4 a''2 a''2")
    container4 = abjad.Staff(r"c4 d4 e4 f4 g2 a2")
    selections = [container1[:], container2[:], container3[:], container4[:]]
    assert auxjad.get.rhythms_are_identical(selections)
    container3 = abjad.Staff(r"c'''1 b''1")
    selections = [container1[:], container2[:], container3[:], container4[:]]
    assert not auxjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_05():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"\times 3/2 {c'4 d'4 e'4} f'4 <g' a'>2 r2")
    selections = [container1[:], container2[:]]
    assert not auxjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_06():
    container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    selections = [container1[:], container2[:]]
    assert auxjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_07():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{d'4} e'4 f'4 <g' a'>2 r2")
    selections = [container1[:], container2[:]]
    assert not auxjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_08():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2")
    selections = [container1[:], container2[:]]
    assert not auxjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_09():
    container1 = abjad.Staff(r"c'4 \grace{c''16} d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{c''16} d'4 e'4 f'4 <g' a'>2 r2")
    selections = [container1[:], container2[:]]
    assert auxjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_10():
    container1 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{c''8} d'4 e'4 f'4 <g' a'>2 r2")
    selection1 = abjad.select(container1)  # x[:] doesn't include graces
    selection2 = abjad.select(container2)
    selections = [selection1, selection2]
    assert not auxjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_11():
    container1 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{b4} d'4 e'4 f'4 <g' a'>2 r2")
    selection1 = abjad.select(container1)  # x[:] doesn't include graces
    selection2 = abjad.select(container2)
    selections = [selection1, selection2]
    assert auxjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_12():
    container1 = abjad.Container(r"c'4 d'4 e'4 f'4")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4")
    selections = [container1[:], container2[:]]
    assert auxjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_13():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    selections = [container1[:], container2[:]]
    assert abjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_14():
    container1 = abjad.Staff(r"c'4 ~ c'16 d'8. ~ d'4 e'4")
    container2 = abjad.Staff(r"c''4 ~ c''16 b'8. ~ b'4 a'4")
    selections = [container1[:], container2[:]]
    assert auxjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_15():
    container1 = abjad.Staff(r"c'4 ~ c'16 r8. r8. <d' e'>16 ~ <d' e'>4")
    container2 = abjad.Staff(r"r4 r16 c''8. ~ c''8. b'16 ~ b'4")
    selections = [container1[:], container2[:]]
    assert auxjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_16():
    container1 = abjad.Staff(r"c'4 ~ c'16 r8. r8. <d' e'>16 ~ <d' e'>4")
    container2 = abjad.Staff(r"r4 r16 c''8. b'8. a'16 ~ a'4")
    selections = [container1[:], container2[:]]
    assert not auxjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_17():
    container1 = abjad.Staff(r"c'4 ~ c'16 r8. r8. <d' e'>16 ~ <d' e'>4")
    container2 = abjad.Staff(r"r4 d''16 c''8. b'8. a'16 ~ a'4")
    selections = [container1[:], container2[:]]
    assert not auxjad.get.rhythms_are_identical(selections)


def test_rhythms_are_identical_18():
    container1 = abjad.Container(r"c'4\mp ~ c'16 r8.\< d'8\mf-. e'4.")
    container2 = abjad.Container(r"c''4\ff\> ~ c''16 b'8.-> a'8-> g'4.\ppp")
    selections = [container1[:], container2[:]]
    assert auxjad.get.rhythms_are_identical(selections)
