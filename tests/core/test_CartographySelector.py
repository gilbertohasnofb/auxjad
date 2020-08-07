import random

import pytest

import auxjad


def test_CartographySelector_01():
    random.seed(41298)
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    assert selector.contents == [0, 1, 2, 3, 4]
    assert format(selector) == "[0, 1, 2, 3, 4]"
    assert selector.weights == [1.0, 0.75, 0.5625, 0.421875, 0.31640625]
    assert selector.previous_index is None
    assert selector.previous_result is None
    assert len(selector) == 5
    result = ''
    for _ in range(30):
        result += str(selector())
    assert result == '203001402200011111101400310140'
    assert selector.previous_index == 0
    assert selector.previous_result == 0
    with pytest.raises(AttributeError):
        selector.previous_index = 3
        selector.previous_result = 7


def test_CartographySelector_02():
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4], decay_rate=0.5)
    assert selector.weights == [1.0, 0.5, 0.25, 0.125, 0.0625]


def test_CartographySelector_03():
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    selector.drop_first_and_append(5)
    assert selector.contents == [1, 2, 3, 4, 5]
    selector.drop_first_and_append(42)
    assert selector.contents == [2, 3, 4, 5, 42]


def test_CartographySelector_04():
    selector = auxjad.CartographySelector([10, 7, 14, 31, 98])
    selector.drop_n_and_append(100, 2)
    assert selector.contents == [10, 7, 31, 98, 100]


def test_CartographySelector_05():
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    selector.drop_last_and_prepend(-1)
    assert selector.contents == [-1, 0, 1, 2, 3]
    selector.drop_last_and_prepend(71)
    assert selector.contents == [71, -1, 0, 1, 2]


def test_CartographySelector_06():
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    selector.rotate()
    assert selector.contents == [1, 2, 3, 4, 0]
    selector.rotate(anticlockwise=True)
    assert selector.contents == [0, 1, 2, 3, 4]
    selector.rotate(anticlockwise=True)
    assert selector.contents == [4, 0, 1, 2, 3]


def test_CartographySelector_07():
    random.seed(15424)
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    selector.shuffle()
    assert selector.contents == [1, 4, 3, 0, 2]


def test_CartographySelector_08():
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4], decay_rate=0.5)
    assert len(selector) == 5
    selector.contents = [0, 1, 2, 3, 4]
    assert selector.weights == [1.0, 0.5, 0.25, 0.125, 0.0625]

    selector.contents = [10, 7, 14, 31, 98, 47, 32]
    assert len(selector) == 7
    assert selector.contents == [10, 7, 14, 31, 98, 47, 32]
    assert selector.weights == [1.0,
                                0.5,
                                0.25,
                                0.125,
                                0.0625,
                                0.03125,
                                0.015625,
                                ]


def test_CartographySelector_09():
    selector = auxjad.CartographySelector([10, 7, 14, 31, 98])
    selector[2] = 100
    assert selector.contents == [10, 7, 100, 31, 98]


def test_CartographySelector_10():
    random.seed(83552)
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    selector.decay_rate = 0.2
    assert selector.weights == [1.0,
                                0.2,
                                0.04000000000000001,
                                0.008000000000000002,
                                0.0016000000000000003,
                                ]
    result = ''
    for _ in range(30):
        result += str(selector())
    assert result == '000001002100000201001030000100'


def test_CartographySelector_11():
    random.seed(19844)
    selector = auxjad.CartographySelector([10, 7, 14, 31, 98])
    assert selector[1] == 7
    assert selector[1:4] == [7, 14, 31]
    assert selector[:] == [10, 7, 14, 31, 98]
    assert selector() == 31
    n = selector.previous_index
    assert n == 3
    assert selector[n] == 31
    del selector[2:4]
    assert selector.contents == [10, 7, 98]


def test_CartographySelector_12():
    random.seed(98743)
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    result = ''
    for _ in range(30):
        result += str(selector())
    assert result == '210431340000344203001220034203'
    result = ''
    for _ in range(30):
        result += str(selector(no_repeat=True))
    assert result == '210421021020304024230120241202'


def test_CartographySelector_13():
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    selector.mirror_swap(0)
    assert selector.contents == [4, 1, 2, 3, 0]
    selector.mirror_swap(0)
    assert selector.contents == [0, 1, 2, 3, 4]
    selector.mirror_swap(3)
    assert selector.contents == [0, 3, 2, 1, 4]
    selector.mirror_swap(2)
    assert selector.contents == [0, 3, 2, 1, 4]


def test_CartographySelector_14():
    random.seed(90129)
    selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
    selector.mirror_random_swap()
    assert selector.contents == [4, 1, 2, 3, 0]
    selector.mirror_random_swap()
    assert selector.contents == [4, 3, 2, 1, 0]
    selector.mirror_random_swap()
    assert selector.contents == [4, 1, 2, 3, 0]


def test_CartographySelector_15():
    random.seed(12387)
    selector = auxjad.CartographySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    result = ''
    result += selector.__next__()
    result += selector.__next__()
    result += selector.__next__()
    result += next(selector)
    result += next(selector)
    result += next(selector)
    assert result == 'CBBEAE'
