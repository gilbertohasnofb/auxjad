import random

import auxjad


def test_GeneticAlgorithm_01():
    ga = auxjad.GeneticAlgorithm(
        target=['A', 'B', 'C', 'D', 'E'],
        genes=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    )
    assert format(ga) == "['A', 'B', 'C', 'D', 'E']"
    assert len(ga) == 5
    assert ga.initial_individual is None
    assert ga.population_size == 100
    assert ga.select_n_parents == 10
    assert ga.mutation_chance == 0.2
    assert ga.mutation_index == 0.1
    assert ga.evaluation_index == 0.2
    assert ga.target == ['A', 'B', 'C', 'D', 'E']


def test_GeneticAlgorithm_02():
    random.seed(87124)
    ga = auxjad.GeneticAlgorithm(
        target=['A', 'B', 'C', 'D', 'E'],
        genes=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    )
    assert ga.generation_number is None
    ga()
    assert ga.generation_number == 0
    assert ga.fittest_individual == ['D', 'C', 'A', 'D', 'E']
    ga()
    assert ga.generation_number == 1
    assert ga.fittest_individual == ['A', 'C', 'A', 'D', 'E']
    ga()
    assert ga.generation_number == 2
    assert ga.fittest_individual == ['A', 'C', 'C', 'D', 'E']


def test_GeneticAlgorithm_03():
    random.seed(55127)
    ga = auxjad.GeneticAlgorithm(
        target=['A', 'B', 'C', 'D', 'E'],
        genes=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
        population_size=4,
        select_n_parents=2,
    )
    ga()
    assert ga.population == [['A', 'J', 'J', 'B', 'H'],
                             ['D', 'A', 'E', 'A', 'F'],
                             ['F', 'F', 'A', 'F', 'F'],
                             ['F', 'F', 'E', 'J', 'C'],
                             ]
    assert ga.scores == [0.209603072,
                         0.0912,
                         0.05638400000000001,
                         0.016396800000000003,
                         ]


def test_GeneticAlgorithm_04():
    random.seed(60012)
    ga = auxjad.GeneticAlgorithm(
        target=['A', 'B', 'C', 'D', 'E'],
        genes=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
        population_size=50,
    )
    expected_results = [['A', 'J', 'B', 'E', 'E'],
                        ['A', 'H', 'C', 'D', 'J'],
                        ['A', 'C', 'D', 'D', 'E'],
                        ['A', 'C', 'D', 'D', 'E'],
                        ['A', 'C', 'D', 'D', 'E'],
                        ['A', 'C', 'C', 'D', 'E'],
                        ['A', 'C', 'C', 'D', 'E'],
                        ['A', 'C', 'C', 'D', 'E'],
                        ['A', 'C', 'C', 'D', 'E'],
                        ['A', 'C', 'C', 'D', 'E'],
                        ]
    expected_scores = [0.480000512,
                       0.6000768,
                       0.6799999999999999,
                       0.6799999999999999,
                       0.6799999999999999,
                       0.8400000000000001,
                       0.8400000000000001,
                       0.8400000000000001,
                       0.8400000000000001,
                       0.8400000000000001,
                       ]
    for i in range(10):
        ga()
        assert ga.generation_number == i
        assert ga.fittest_individual == expected_results[i]
        assert ga.fittest_individual_score == expected_scores[i]


def test_GeneticAlgorithm_05():
    random.seed(51902)
    ga = auxjad.GeneticAlgorithm(
        target=['A', 'B', 'C', 'D', 'E'],
        genes=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    )
    assert ga.fittest_individual is None
    assert ga.generation_number is None
    for _ in range(10):
        ga()
    assert ga.fittest_individual == ['A', 'B', 'C', 'D', 'E']
    assert ga.generation_number == 9
    ga.reset()
    assert ga.fittest_individual is None
    assert ga.generation_number is None


def test_GeneticAlgorithm_06():
    random.seed(51244)
    ga = auxjad.GeneticAlgorithm(
        target=['A', 'B', 'C', 'D', 'E'],
        genes=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
        initial_individual=['F', 'G', 'H', 'I', 'J'],
    )
    expected_results = [['F', 'G', 'H', 'I', 'J'],
                        ['F', 'B', 'H', 'I', 'J'],
                        ['F', 'B', 'H', 'I', 'E'],
                        ['F', 'B', 'H', 'I', 'E'],
                        ['A', 'B', 'H', 'I', 'E'],
                        ['A', 'B', 'E', 'I', 'E'],
                        ['A', 'B', 'E', 'D', 'E'],
                        ['A', 'B', 'E', 'D', 'E'],
                        ['A', 'B', 'E', 'D', 'E'],
                        ['A', 'B', 'D', 'D', 'E'],
                        ]
    for expected_result in expected_results:
        ga()
        assert ga.fittest_individual == expected_result


def test_GeneticAlgorithm_07():
    random.seed(51244)
    ga = auxjad.GeneticAlgorithm(
        target=['A', 'B', 'C', 'D', 'E'],
        genes=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    )
    assert ga.population_size == 100
    assert ga.select_n_parents == 10
    assert ga.keep_n_parents == 0
    assert ga.mutation_chance == 0.2
    assert ga.mutation_index == 0.1
    assert ga.evaluation_index == 0.2
    ga.population_size = 50
    ga.select_n_parents = 15
    ga.keep_n_parents = 3
    ga.mutation_chance = 0.75
    ga.mutation_index = 0.25
    ga.evaluation_index = 0.5
    assert ga.population_size == 50
    assert ga.select_n_parents == 15
    assert ga.keep_n_parents == 3
    assert ga.mutation_chance == 0.75
    assert ga.mutation_index == 0.25
    assert ga.evaluation_index == 0.5


def test_GeneticAlgorithm_08():
    random.seed(89226)
    ga = auxjad.GeneticAlgorithm(
        target=['A', 'B', 'C', 'D', 'E'],
        genes=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    )
    ga.__next__()
    assert ga.fittest_individual == ['A', 'C', 'D', 'D', 'D']
    ga.__next__()
    assert ga.fittest_individual == ['A', 'C', 'E', 'D', 'E']
    next(ga)
    assert ga.fittest_individual == ['A', 'C', 'E', 'D', 'E']
    next(ga)
    assert ga.fittest_individual == ['A', 'C', 'D', 'D', 'E']
