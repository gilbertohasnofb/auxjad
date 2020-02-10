import abjad
import auxjad
import random


def test_CartographyContainer_01():
    random.seed(41298)
    container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
    assert container.contents == [0, 1, 2, 3, 4]
    assert container.weights == [1.0, 0.75, 0.5625, 0.421875, 0.31640625]
    assert len(container) == 5
    result = ''
    for _ in range(30):
        result += str(container())
    assert result == '203001402200011111101400310140'


def test_CartographyContainer_02():
    container = auxjad.CartographyContainer([0, 1, 2, 3, 4], decay_rate=0.5)
    assert container.weights == [1.0, 0.5, 0.25, 0.125, 0.0625]


def test_CartographyContainer_03():
    container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
    container.append(5)
    assert container.contents == [1, 2, 3, 4, 5]
    container.append(42)
    assert container.contents == [2, 3, 4, 5, 42]


def test_CartographyContainer_04():
    container = auxjad.CartographyContainer([10, 7, 14, 31, 98])
    container.append_keeping_n(100, 2)
    assert container.contents == [10, 7, 31, 98, 100]


def test_CartographyContainer_05():
    container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
    container.prepend(-1)
    assert container.contents == [-1, 0, 1, 2, 3]
    container.prepend(71)
    assert container.contents == [71, -1, 0, 1, 2]


def test_CartographyContainer_06():
    container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
    container.rotate()
    assert container.contents == [1, 2, 3, 4, 0]
    container.rotate(anticlockwise=True)
    assert container.contents == [0, 1, 2, 3, 4]
    container.rotate(anticlockwise=True)
    assert container.contents == [4, 0, 1, 2, 3]


def test_CartographyContainer_07():
    random.seed(15424)
    container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
    container.randomise()
    assert container.contents == [1, 4, 3, 0, 2]


def test_CartographyContainer_08():
    container = auxjad.CartographyContainer([0, 1, 2, 3, 4], decay_rate=0.5)
    assert len(container) == 5
    assert container.weights == [1.0, 0.5, 0.25, 0.125, 0.0625]
    container.set_container([10, 7, 14, 31, 98, 47, 32])
    assert container.contents == [10, 7, 14, 31, 98, 47, 32]
    assert len(container) == 7
    assert container.weights == [1.0,
                                 0.5,
                                 0.25,
                                 0.125,
                                 0.0625,
                                 0.03125,
                                 0.015625,
                                 ]


def test_CartographyContainer_09():
    container = auxjad.CartographyContainer([10, 7, 14, 31, 98])
    container.replace_element(100, 2)
    assert container.contents == [10, 7, 100, 31, 98]


def test_CartographyContainer_10():
    random.seed(83552)
    container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
    container.set_decay_rate(0.2)
    assert container.weights == [1.0,
                                 0.2,
                                 0.04000000000000001,
                                 0.008000000000000002,
                                 0.0016000000000000003,
                                 ]
    result = ''
    for _ in range(30):
        result += str(container())
    assert result == '000001002100000201001030000100'


def test_CartographyContainer_11():
    random.seed(19844)
    container = auxjad.CartographyContainer([10, 7, 14, 31, 98])
    assert container() == 31
    n = container.previous_index
    assert n == 3
    assert container.get_element(n) == 31
