import abjad
import auxjad


def test_containers_are_equal_01():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    assert auxjad.containers_are_equal(container1, container2)


def test_containers_are_equal_02():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"\times 3/2 {c'4 d'4 e'4} f'4 <g' a'>2 r2")
    assert not auxjad.containers_are_equal(container1, container2)


def test_containers_are_equal_03():
    container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    assert auxjad.containers_are_equal(container1, container2)


def test_containers_are_equal_04():
    container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    assert not auxjad.containers_are_equal(container1,
                                           container2,
                                           include_indicators=True,
                                           )


def test_containers_are_equal_05():
    container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
    container2 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
    assert auxjad.containers_are_equal(container1,
                                       container2,
                                       include_indicators=True,
                                       )


def test_containers_are_equal_06():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{d'4} e'4 f'4 <g' a'>2 r2")
    assert not auxjad.containers_are_equal(container1, container2)


def test_containers_are_equal_07():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2")
    assert not auxjad.containers_are_equal(container1, container2)


def test_containers_are_equal_08():
    container1 = abjad.Staff(r"c'4 \grace{c''16} d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{c''16} d'4 e'4 f'4 <g' a'>2 r2")
    assert auxjad.containers_are_equal(container1, container2)


def test_containers_are_equal_09():
    container1 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{c''8} d'4 e'4 f'4 <g' a'>2 r2")
    assert not auxjad.containers_are_equal(container1, container2)


def test_containers_are_equal_10():
    container1 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{b4} d'4 e'4 f'4 <g' a'>2 r2")
    assert not auxjad.containers_are_equal(container1, container2)
