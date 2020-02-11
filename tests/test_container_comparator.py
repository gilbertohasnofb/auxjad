import abjad
import auxjad


def test_container_comparator_01():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    assert auxjad.container_comparator(container1, container2) == True


def test_container_comparator_02():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"\times 3/2 {c'4 d'4 e'4} f'4 <g' a'>2 r2")
    assert auxjad.container_comparator(container1, container2) == False


def test_container_comparator_03():
    container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    assert auxjad.container_comparator(container1, container2) == True


def test_container_comparator_04():
    container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
    container2 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    assert auxjad.container_comparator(container1,
                                       container2,
                                       include_indicators=True,
                                       ) == False


def test_container_comparator_05():
    container1 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
    container2 = abjad.Staff(r"c'4\pp d'4 e'4-. f'4 <g' a'>2-> r2")
    assert auxjad.container_comparator(container1,
                                       container2,
                                       include_indicators=True,
                                       ) == True


def test_container_comparator_06():
   container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
   container2 = abjad.Staff(r"c'4 \grace{d'4} e'4 f'4 <g' a'>2 r2")
   assert auxjad.container_comparator(container1, container2) == False


def test_container_comparator_07():
    container1 = abjad.Staff(r"c'4 d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2")
    assert auxjad.container_comparator(container1, container2) == False


def test_container_comparator_08():
    container1 = abjad.Staff(r"c'4 \grace{c''16} d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{c''16} d'4 e'4 f'4 <g' a'>2 r2")
    assert auxjad.container_comparator(container1, container2) == True


def test_container_comparator_09():
    container1 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{c''8} d'4 e'4 f'4 <g' a'>2 r2")
    assert auxjad.container_comparator(container1, container2) == False


def test_container_comparator_10():
    container1 = abjad.Staff(r"c'4 \grace{c''4} d'4 e'4 f'4 <g' a'>2 r2")
    container2 = abjad.Staff(r"c'4 \grace{b4} d'4 e'4 f'4 <g' a'>2 r2")
    assert auxjad.container_comparator(container1, container2) == False
