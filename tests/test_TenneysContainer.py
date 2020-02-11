import abjad
import auxjad
import random


def test_TenneysContainer_01():
    random.seed(43714)
    container = auxjad.TenneysContainer(['A', 'B', 'C', 'D', 'E', 'F'])
    assert container.contents == ['A', 'B', 'C', 'D', 'E', 'F']
    assert container.curvature == 1.0
    assert container.weights == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    assert container.probabilities == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    assert container.previous_index == None
    assert len(container) == 6
    result = ''
    for _ in range(30):
        result += container()
    assert result == 'BDAFCBEFCDFDBAEDFCABDEABCDEBFE'
    assert container.previous_index == 4
    assert container.weights == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    assert container.probabilities == [7.0, 2.0, 5.0, 4.0, 0.0, 1.0]


def test_TenneysContainer_02():
    random.seed(37248)
    container = auxjad.TenneysContainer(['A', 'B', 'C', 'D', 'E', 'F'],
                                        curvature=0.001,
                                        )
    result = ''
    for _ in range(30):
        result += container()
    assert result == 'CDCBFECBCEBCFCEDFACDBADCADCDFE'
    assert container.probabilities == [1.0016107337527294,
                                       1.002199640244188,
                                       1.001099215984204,
                                       1.0006933874625807,
                                       0.0,
                                       1.0,
                                       ]


def test_TenneysContainer_03():
   random.seed(76231)
   container = auxjad.TenneysContainer(['A', 'B', 'C', 'D', 'E', 'F'],
                                       curvature=15.2,
                                       )
   result = ''
   for _ in range(30):
       result += container()
   assert result == 'DFAECBDFAECBDFAECBDFAECBDFAECB'
   assert container.probabilities == [17874877.39956566,
                                      0.0,
                                      1.0,
                                      42106007735.02238,
                                      37640.547696542824,
                                      1416810830.8957152,
                                      ]


def test_TenneysContainer_04():
    random.seed(14625)
    container = auxjad.TenneysContainer(
        ['A', 'B', 'C', 'D', 'E', 'F'],
        weights=[1.0, 1.0, 5.0, 5.0, 10.0, 20.0],
    )
    assert container.weights == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    assert container.probabilities == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    result = ''
    for _ in range(30):
        result += container()
    assert result == 'FBEFECFDEADFEDFEDBFECDAFCEDCFE'
    assert container.weights == [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
    assert container.probabilities == [7.0, 12.0, 10.0, 15.0, 0.0, 20.0]


def test_TenneysContainer_05():
    random.seed(21169)
    container = auxjad.TenneysContainer(['A', 'B', 'C', 'D', 'E', 'F'])
    for _ in range(30):
        container()
    container.replace_element('foo', 2)
    assert container.contents == ['A', 'B', 'foo', 'D', 'E', 'F']
    assert container.probabilities == [3.0, 2.0, 1.0, 7.0, 5.0, 0.0]


def test_TenneysContainer_06():
    random.seed(54267)
    container = auxjad.TenneysContainer(['A', 'B', 'C', 'D', 'E', 'F'])
    for _ in range(30):
        container()
    assert container.probabilities == [2.0, 1.0, 4.0, 3.0, 0.0, 5.0]
    container.set_container([2, 4, 6, 8])
    assert container.contents == [2, 4, 6, 8]
    assert len(container) == 4
    assert container.weights == [1.0, 1.0, 1.0, 1.0]
    assert container.probabilities == [1.0, 1.0, 1.0, 1.0]


def test_TenneysContainer_07():
    container = auxjad.TenneysContainer(['A', 'B', 'C', 'D', 'E', 'F'])
    assert container.curvature == 1.0
    container.set_curvature(0.25)
    assert container.curvature == 0.25


def test_TenneysContainer_08():
    random.seed(99651)
    container = auxjad.TenneysContainer(['A', 'B', 'C', 'D', 'E', 'F'])
    for _ in range(30):
        container()
    assert container.probabilities == [4.0, 3.0, 1.0, 0.0, 5.0, 2.0]
    container.reset_probabilities()
    assert container.probabilities == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
