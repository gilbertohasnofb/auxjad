import random

import pytest

import auxjad


def test_TenneySelector_01():
    random.seed(43714)
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    assert selector.contents == ['A', 'B', 'C', 'D', 'E', 'F']
    assert format(selector) == "['A', 'B', 'C', 'D', 'E', 'F']"
    assert selector.curvature == 1.0
    assert selector.weights == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    assert selector.probabilities == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    assert selector.previous_index is None
    assert selector.previous_result is None
    assert len(selector) == 6
    result = ''
    for _ in range(30):
        result += selector()
    assert result == 'BDAFCBEFCDFDBAEDFCABDEABCDEBFE'
    assert selector.previous_index == 4
    assert selector.previous_result == 'E'
    with pytest.raises(AttributeError):
        selector.previous_index = 3
        selector.previous_result = 'C'
    assert selector.weights == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    assert selector.probabilities == [7.0, 2.0, 5.0, 4.0, 0.0, 1.0]


def test_TenneySelector_02():
    random.seed(37248)
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'],
                                     curvature=0.001,
                                     )
    result = ''
    for _ in range(30):
        result += selector()
    assert result == 'CDCBFECBCEBCFCEDFACDBADCADCDFE'
    assert selector.probabilities == [1.0016107337527294,
                                      1.002199640244188,
                                      1.001099215984204,
                                      1.0006933874625807,
                                      0.0,
                                      1.0,
                                      ]


def test_TenneySelector_03():
    random.seed(76231)
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'],
                                     curvature=15.2,
                                     )
    result = ''
    for _ in range(30):
        result += selector()
    assert result == 'DFAECBDFAECBDFAECBDFAECBDFAECB'
    assert selector.probabilities == [17874877.39956566,
                                      0.0,
                                      1.0,
                                      42106007735.02238,
                                      37640.547696542824,
                                      1416810830.8957152,
                                      ]


def test_TenneySelector_04():
    random.seed(14625)
    selector = auxjad.TenneySelector(
        ['A', 'B', 'C', 'D', 'E', 'F'],
        weights=[1.0, 1.0, 5.0, 5.0, 10.0, 20.0],
    )
    assert selector.weights == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    assert selector.probabilities == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    result = ''
    for _ in range(30):
        result += selector()
    assert result == 'FBEFECFDEADFEDFEDBFECDAFCEDCFE'
    assert selector.weights == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    assert selector.probabilities == [7.0, 12.0, 10.0, 15.0, 0.0, 20.0]


def test_TenneySelector_05():
    random.seed(21169)
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    for _ in range(30):
        selector()
    assert selector.probabilities == [3.0, 2.0, 1.0, 7.0, 5.0, 0.0]
    assert selector[2] == 'C'
    assert selector[1:4] == ['B', 'C', 'D']
    selector[2] = 'foo'
    assert selector[:] == ['A', 'B', 'foo', 'D', 'E', 'F']
    selector[:] = ['foo', 'bar', 'X', 'Y', 'Z', '...']
    assert selector.contents == ['foo', 'bar', 'X', 'Y', 'Z', '...']
    assert selector.probabilities == [3.0, 2.0, 1.0, 7.0, 5.0, 0.0]
    del selector[0:2]
    assert selector.contents == ['X', 'Y', 'Z', '...']
    assert selector.probabilities == [1.0, 7.0, 5.0, 0.0]
    assert 'X' in selector
    assert 'A' not in selector


def test_TenneySelector_06():
    random.seed(54267)
    selector = auxjad.TenneySelector(
        ['A', 'B', 'C', 'D', 'E', 'F'],
        weights=[1.0, 1.0, 5.0, 5.0, 10.0, 20.0],
    )
    for _ in range(30):
        selector()
    assert len(selector) == 6
    assert selector.contents == ['A', 'B', 'C', 'D', 'E', 'F']
    assert selector.weights == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    assert selector.probabilities == [8.0, 2.0, 5.0, 15.0, 50.0, 0.0]

    selector.contents = [2, 4, 6, 8]
    assert len(selector) == 4
    assert selector.contents == [2, 4, 6, 8]
    assert selector.weights == [1.0, 1.0, 1.0, 1.0]
    assert selector.probabilities == [1.0, 1.0, 1.0, 1.0]

    selector.weights = [1.2, 3.0, 2.5, 1.3]
    assert selector.weights == [1.2, 3.0, 2.5, 1.3]


def test_TenneySelector_07():
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    assert selector.curvature == 1.0
    selector.curvature = 0.25
    assert selector.curvature == 0.25


def test_TenneySelector_08():
    random.seed(99651)
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    for _ in range(30):
        selector()
    assert selector.probabilities == [4.0, 3.0, 1.0, 0.0, 5.0, 2.0]
    selector.reset_probabilities()
    assert selector.probabilities == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def test_TenneySelector_09():
    random.seed(12387)
    selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
    result = ''
    result += selector.__next__()
    result += selector.__next__()
    result += selector.__next__()
    result += next(selector)
    result += next(selector)
    result += next(selector)
    assert result == 'DBDFAE'


def test_TenneySelector_10():
    selector = auxjad.TenneySelector(
        ['A', 'B', 'C', 'D', 'E', 'F'],
        weights=[1.0, 1.0, 5.0, 5.0, 10.0, 20.0],
    )
    assert selector.weights == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    selector.weights = None
    assert selector.weights == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
