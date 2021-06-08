import random
from typing import Optional, Union


class GeneticAlgorithm():
    r"""An implementation of a genetic algorithm. Takes a :attr:`target` list
    and a list of :attr:`genes` to prod`uce generations of individuals at each
    :meth:`__call__`. Fittest individual of the current generation can be
    accessed directly using the property :attr:`fittest_individual`.

    Basic usage:
        The genetic algorithm should be initialised with two :obj:`list`'s of
        objects. The elements of these :obj:`list` can be of any type. The
        first one is the :attr:`target` list used to evaluate the individuals
        in the population. The second is the :attr:`genes` list which should
        contain all possible elements that can make up an individual. All
        elements of :attr:`target` must also be present in :attr:`genes`. For
        this example, :attr:`population_size` will be set to a very small value
        of ``4``, though in practice it's better to use substantially larger
        numbers (default value is ``100``). :attr:`select_n_parents` also needs
        to be decreased, as it must always be smaller than
        :attr:`population_size`.

        >>> ga = auxjad.GeneticAlgorithm(
        ...     target=['A', 'B', 'C', 'D', 'E'],
        ...     genes=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
        ...     population_size=4,
        ...     select_n_parents=2,
        ... )

        Calling the GA generator will generate a :attr:`population` of
        individuals, each of wich will also be awarded a score according to an
        evaluation function. :attr:`population` and :attr:`scores` are always
        ordered from the fittest to the least fit.

        >>> ga()
        >>> ga.population
        [['A', 'J', 'J', 'B', 'H'],
         ['D', 'A', 'E', 'A', 'F'],
         ['F', 'F', 'A', 'F', 'F'],
         ['F', 'F', 'E', 'J', 'C'],
         ]
        >>> ga.scores
        [0.209603072,
         0.0912,
         0.05638400000000001,
         0.016396800000000003,
         ]

        Each subsequent call will generate a new generation of individuals
        which will become increasingly fit.

    :attr:`fittest_individual` and :attr:`fittest_individual_score`:
        The fittest individual of the whole population can be directly
        accessed using the property :attr:`fittest_individual`:

        >>> ga = auxjad.GeneticAlgorithm(
        ...     target=['A', 'B', 'C', 'D', 'E'],
        ...     genes=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
        ...     population_size=4,
        ...     select_n_parents=2,
        ... )
        >>> ga()
        >>> ga.fittest_individual
        ['A', 'J', 'J', 'B', 'H']

        Its score is also directly accessible using
        :attr:`fittest_individual_score`:

        >>> ga.fittest_individual_score
        0.209603072

    Evolution:
        As expected, each generation will become increasingly fitter in
        relation to the :attr:`target`. The example below shows the fittest
        individual of each of ``10`` generations, with a
        :attr:`population_size` to  ``50``:

        >>> ga = auxjad.GeneticAlgorithm(
        ...     target=['A', 'B', 'C', 'D', 'E'],
        ...     genes=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
        ...     population_size=50,
        ... )
        >>> for _ in range(10):
        ...     ga()
        ...     print(ga.fittest_individual, ga.fittest_individual_score)
        ['A', 'J', 'B', 'E', 'E'] 0.480000512
        ['A', 'H', 'C', 'D', 'J'] 0.6000768
        ['A', 'C', 'D', 'D', 'E'] 0.6799999999999999
        ['A', 'C', 'D', 'D', 'E'] 0.6799999999999999
        ['A', 'C', 'D', 'D', 'E'] 0.6799999999999999
        ['A', 'C', 'C', 'D', 'E'] 0.8400000000000001
        ['A', 'C', 'C', 'D', 'E'] 0.8400000000000001
        ['A', 'C', 'C', 'D', 'E'] 0.8400000000000001
        ['A', 'C', 'C', 'D', 'E'] 0.8400000000000001
        ['A', 'C', 'C', 'D', 'E'] 0.8400000000000001

    Evaluation function and :attr:`evaluation_index`:
        The evaluation function gives out a score between ``0.0`` to ``1.0`` to
        each individual in the population. For each given individual, this
        function compares each element of its elements with the element in the
        :attr:`target` at the same index. As to accomodate arbitrary objects
        being used as genes (as opposed to numbers only), this comparison uses
        the distance between the current individual and target genes using the
        :attr:`genes` property. Consider the following example, where the
        available genes are ``['A', 'B', 'C', 'D', 'E', 'F']`` and the target
        is ``['B', 'A', 'A', 'C']``. Suppose an individual has the genes
        ``['D', 'D', 'A', 'B']``.

        To evaluate this individual, first the algorithm finds the indices of
        both the target's genes (in this case, ``[1, 0, 0, 2]``) and also of
        the individual to be evaluated (in this case, ``[3, 3, 0, 1]``). It
        then scores each element of this individual against the target using:

        .. code-block::

            difference = abs(target_gene_index - individual_gene_index)
            element_score = evaluation_index ** difference

        Thus, when the difference is ``0``, the score of this element is
        ``1.0``. The higher the difference, the smaller the value; this decay
        can be controlled using the property :attr:`evaluation_index`, whose
        default value is ``0.2``. Thus when the difference is ``1`` or ``-1``,
        the score is ``0.2 ** 1 = 0.2``, when the difference is ``2`` or
        ``-2``, the score is ``0.2 ** 2 = 0.04``, and so on. The total score of
        an individual will be given by the normalised sum of the evaluation of
        each of its genes.

    :attr:`select_n_parents` and :attr:`keep_n_parents`:
        When creating a new generation of individuals, the algorithm will
        select the fittest individuals to be parents for the next generation.
        The number of parents is given by :attr:`select_n_parents`, whose
        default value is ``10``. These parents generate offspring by being
        recombined through a crossover process, in which the first half of a
        random parent and a second half of another random parent are combined
        into a new individual. Parents are not kept in the next generation by
        default and are solely used in this crossover process. To 'clone'
        parents into the next generation, set the property
        :attr:`keep_n_parents` to a value larger than ``0`` (its default
        value).

    :attr:`mutation_chance` and :attr:`mutation_index`:
        After the crossover process, an individual can go through random
        mutations. The chance of this occuring on a given individual is given
        by :attr:`mutation_chance`, whose value should range between ``0.0``
        and ``1.0`` (default is ``0.2``). If an individual is selected to
        undergo a random mutation, then each of its genes will have a chance of
        being mutated, which in turn is given by the property
        :attr:`mutation_index` (default value is ``0.1``).

    :attr:`initial_individual`:
        Instead of starting with a random population of individuals, it's
        possible to set a custom initial individual as a starting point. This
        can be used to 'morph' fittest individual from this initial one to a
        fit one according to the target.

        >>> ga = auxjad.GeneticAlgorithm(
        ...     target=['A', 'B', 'C', 'D', 'E'],
        ...     genes=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
        ...     initial_individual=['F', 'G', 'H', 'I', 'J'],
        ... )
        >>> for _ in range(10):
        ...     ga()
        ...     ga.fittest_individual
        ['F', 'G', 'H', 'I', 'J']
        ['F', 'B', 'H', 'I', 'J']
        ['F', 'B', 'H', 'I', 'E']
        ['F', 'B', 'H', 'I', 'E']
        ['A', 'B', 'H', 'I', 'E']
        ['A', 'B', 'E', 'I', 'E']
        ['A', 'B', 'E', 'D', 'E']
        ['A', 'B', 'E', 'D', 'E']
        ['A', 'B', 'E', 'D', 'E']
        ['A', 'B', 'D', 'D', 'E']

    :meth:`reset`:
        Use the :meth:`reset` method to reset the genetic algorithm at any
        point:

        >>> ga = auxjad.GeneticAlgorithm(
        ...     target=['A', 'B', 'C', 'D', 'E'],
        ...     genes=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
        ... )
        >>> ga.fittest_individual
        None
        >>> ga.generation_number
        None
        >>> for _ in range(10):
        ...     ga()
        >>> ga.fittest_individual
        ['C', 'B', 'C', 'D', 'E']
        >>> ga.generation_number
        9
        >>> ga.reset()
        >>> ga.fittest_individual
        None
        >>> ga.generation_number
        None
    """

    ### CLASS VARIABLES ###

    __slots__ = ('_target',
                 '_genes',
                 '_initial_individual',
                 '_population_size',
                 '_select_n_parents',
                 '_keep_n_parents',
                 '_mutation_chance',
                 '_mutation_index',
                 '_evaluation_index',
                 '_target_indices',
                 '_scores',
                 '_generation_number',
                 '_population',
                 )

    ### INITIALISER ###

    def __init__(self,
                 *,
                 target: list,
                 genes: list,
                 initial_individual: Optional[list] = None,
                 population_size: int = 100,
                 select_n_parents: int = 10,
                 keep_n_parents: int = 0,
                 mutation_chance: float = 0.2,
                 mutation_index: float = 0.1,
                 evaluation_index: float = 0.2,
                 ) -> None:
        r'Initialises self.'
        if not isinstance(genes, list):
            raise TypeError("'genes' must be 'list'")
        if not isinstance(target, list):
            raise TypeError("'target' must be 'list'")
        if any(value not in genes for value in target):
            raise ValueError("'target' must only contain elements present in "
                             "'genes'")
        self._genes = genes
        self._target = target
        self._target_indices = [self._genes.index(gene) for gene
                                in self._target]
        self.initial_individual = initial_individual
        self.population_size = population_size
        self.select_n_parents = select_n_parents
        self.keep_n_parents = keep_n_parents
        self.mutation_chance = mutation_chance
        self.mutation_index = mutation_index
        self.evaluation_index = evaluation_index
        self._generation_number = None
        self._population = None
        self._scores = None

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        r'Returns interpreter representation of :attr:`target`.'
        return repr(self._target)

    def __len__(self) -> int:
        r'Returns the number of genes in each individual.'
        return len(self._target)

    def __call__(self) -> None:
        r"""Calls the genetic algorithm process for one iteration. Creates a
        new generation of length :attr:`population_size` via reproduction and
        mutation processes and scores each individual using the evaluation
        function. Sorts the population according to their scores.
        """
        self._generate_population()
        self._score_population()
        self._sort_population_by_evaluation()

    def __next__(self) -> None:
        r"""Calls the genetic algorithm process for one iteration. Creates a
        new generation of length :attr:`population_size` via reproduction and
        mutation processes and scores each individual using the evaluation
        function. Sorts the population according to their scores.
        """
        try:
            return self.__call__()
        except RuntimeError:
            raise StopIteration

    def __iter__(self) -> None:
        r'Returns an iterator, allowing instances to be used as iterators.'
        return self

    ### PUBLIC METHODS ###

    def reset(self) -> None:
        r'Resets that genetic algorithm.'
        self._generation_number = None
        self._population = None
        self._scores = None

    ### PRIVATE METHODS ###

    def _generate_population(self) -> None:
        r"""Calls the genetic algorithm process for one iteration. Creates a
        new generation of length :attr:`population_size` via reproduction and
        mutation processes and scores each individual using the evaluation
        function.
        """
        if self._generation_number is None:
            self._generation_number = 0
            self._generate_initial_individual()
        else:
            self._generation_number += 1
            self._crossover_population()
            self._mutate_population()

    def _generate_initial_individual(self) -> None:
        r"""Generates a random initial population of size
        :attr:`population_size` and whose genes are randomly chosen from
        :attr:`genes`.
        """
        self._population = []
        for _ in range(self._population_size):
            if self._initial_individual is None:
                individual = [random.choice(self._genes) for _
                              in range(self.__len__())]
            else:
                individual = self._initial_individual[:]
            self._population.append(individual)

    def _evaluate(self,
                  individual: list,
                  ) -> float:
        r"""Evaluates all genes of a given individual, returning a
        :obj:`float`. The higher the value, the fitter the individual is, with
        `1.0` being a perfect fit. Use :attr:`evaluation_index` to tweak the
        behaviour of this function.
        """
        individual_score = 0
        individual_indices = [self.genes.index(gene) for gene in individual]
        for gene, target_gene in zip(individual_indices, self._target_indices):
            difference = abs(gene - target_gene)
            individual_score += self._evaluation_index ** difference
        individual_score /= self.__len__()
        return individual_score

    def _sort_population_by_evaluation(self) -> None:
        r"""Sorts the population (and their scores) according to the evaluation
        of its individuals.
        """
        zipped_lists = list(zip(self._scores, self._population))
        zipped_lists.sort(
            key=lambda tuple_pair: tuple_pair[0],
            reverse=True,
        )
        self._population = [gene for _, gene in zipped_lists]
        self._scores = [score for score, _ in zipped_lists]

    def _score_population(self) -> None:
        r"""Generates the list of score for each individual of the current
        generation.
        """
        self._scores = []
        for individual in self._population:
            score = self._evaluate(individual)
            self._scores.append(score)

    def _crossover_population(self) -> None:
        r'Crossover process used to generate offsprings.'
        selected_parents = self._population[:self._select_n_parents]
        if self._keep_n_parents > 0:
            new_generation = self._population[:self._keep_n_parents]
        else:
            new_generation = []
        for _ in range(self._population_size - self._keep_n_parents):
            parents = random.sample(range(len(selected_parents)),
                                    k=2,
                                    )
            half_index = int(self.__len__() / 2)
            parent_A = selected_parents[parents[0]]
            parent_B = selected_parents[parents[1]]
            individual = parent_A[:half_index] + parent_B[half_index:]
            new_generation.append(individual)
        self._population = new_generation[:]

    def _mutate_population(self) -> None:
        r"""Mutates some individuals of the current generation according to
        :attr:`mutation_chance` and :attr:`mutation_index`.
        """
        for index, individual in enumerate(self._population):
            if random.random() < self._mutation_chance:
                mutated_individual = individual[:]
                for i in range(self.__len__()):
                    if random.random() < self._mutation_index:
                        mutated_individual[i] = random.choice(self._genes)
                self._population[index] = mutated_individual

    ### PUBLIC PROPERTIES ###

    @property
    def target(self) -> list:
        r'Target individual used for evaluation.'
        return self._target

    @target.setter
    def target(self,
               target: list,
               ) -> None:
        if not isinstance(target, list):
            raise TypeError("'target' must be 'list'")
        if any(value not in self._genes for value in target):
            raise ValueError("'target' must only contain elements present in "
                             "'genes'")
        self._target = target
        self._target_indices = [self._genes.index(gene) for gene
                                in self._target]

    @property
    def genes(self) -> list:
        r'List of possible genes that make up all individuals.'
        return self._genes

    @genes.setter
    def genes(self,
              genes: list,
              ) -> None:
        if not isinstance(genes, list):
            raise TypeError("'genes' must be 'list'")
        self._genes = genes
        self._target_indices = [self._genes.index(gene) for gene
                                in self._target]

    @property
    def initial_individual(self) -> Union[list, None]:
        r'Optional initial individual (instead of random initial population).'
        return self._initial_individual

    @initial_individual.setter
    def initial_individual(self,
                           initial_individual: Optional[list],
                           ) -> None:
        if initial_individual is not None:
            if not isinstance(initial_individual, list):
                raise TypeError("'initial_individual' must be 'list' or "
                                "'None'")
            if len(initial_individual) != self.__len__():
                raise ValueError("'initial_individual' must have the same "
                                 "length as 'target'")
            if any(value not in self._genes for value in initial_individual):
                raise ValueError("'initial_individual' must only contain "
                                 "elements present in 'genes'")
        self._initial_individual = initial_individual

    @property
    def population_size(self) -> int:
        r'Number of individuals in any given generation.'
        return self._population_size

    @population_size.setter
    def population_size(self,
                        population_size: int,
                        ) -> None:
        if not isinstance(population_size, int):
            raise TypeError("'population_size' must be 'int'")
        self._population_size = population_size

    @property
    def select_n_parents(self) -> int:
        r"""Number of the best-fit individuals that are selected to be the
        parents for the next generation.
        """
        return self._select_n_parents

    @select_n_parents.setter
    def select_n_parents(self,
                         select_n_parents: int,
                         ) -> None:
        if not isinstance(select_n_parents, int):
            raise TypeError("'select_n_parents' must be 'int'")
        if select_n_parents > self._population_size:
            raise ValueError("'select_n_parents' must be equal to or smaller "
                             "than 'population_size'")
        self._select_n_parents = select_n_parents

    @property
    def keep_n_parents(self) -> int:
        r"""Number of the best-fit individuals that survive into the next
        generation. Default is ``0``.
        """
        return self._keep_n_parents

    @keep_n_parents.setter
    def keep_n_parents(self,
                       keep_n_parents: int,
                       ) -> None:
        if not isinstance(keep_n_parents, int):
            raise TypeError("'keep_n_parents' must be 'int'")
        if keep_n_parents > self._population_size:
            raise ValueError("'keep_n_parents' must be equal to or smaller "
                             "than 'population_size'")
        self._keep_n_parents = keep_n_parents

    @property
    def mutation_chance(self) -> float:
        r'The chance of any given individual experiencing mutation.'
        return self._mutation_chance

    @mutation_chance.setter
    def mutation_chance(self,
                        mutation_chance: float,
                        ) -> None:
        if not isinstance(mutation_chance, float):
            raise TypeError("'mutation_chance' must be 'float'")
        if mutation_chance < 0.0:
            raise ValueError("'mutation_chance' must be a positive `float`")
        elif mutation_chance > 1.0:
            raise ValueError("'mutation_chance' cannot be larger than `1.0`")
        self._mutation_chance = mutation_chance

    @property
    def mutation_index(self) -> float:
        r"""Given an individual selected to undergo mutation, this index gives
        the percentage of genes of that individual which will be mutated.
        """
        return self._mutation_index

    @mutation_index.setter
    def mutation_index(self,
                       mutation_index: float,
                       ) -> None:
        if not isinstance(mutation_index, float):
            raise TypeError("'mutation_index' must be 'float'")
        if mutation_index < 0.0:
            raise ValueError("'mutation_index' must be a positive `float`")
        elif mutation_index > 1.0:
            raise ValueError("'mutation_index' cannot be larger than `1.0`")
        self._mutation_index = mutation_index

    @property
    def evaluation_index(self) -> float:
        r"""The index used in the evaluation function. This index will be
        raised by the difference between indices of the target value and the
        current value. Consider the following example, where the available
        genes are ``['A', 'B', 'C', 'D', 'E', 'F']`` and the target is
        ``['B', 'A', 'A', 'C']``. Suppose an individual has the genes
        ``['D', 'D', 'A', 'B']``.

        To evaluate this individual, first the algorithm finds the indices of
        both the target's genes (in this case, ``[1, 0, 0, 2]``) and also of
        the individual to be evaluated (in this case, ``[3, 3, 0, 1]``). It
        then scores each element of this individual against the target using:

        .. code-block::

            difference = abs(target_gene_index - individual_gene_index)
            element_score = evaluation_index ** difference

        Thus, when the difference is ``0``, the score of this element is
        ``1.0``. The higher the difference, the smaller the value; this decay
        can be controlled using this very property, whose default value is
        ``0.2``. Thus when the difference is ``1`` or ``-1``, the score is
        ``0.2 ** 1 = 0.2``, when the difference is ``2`` or ``-2``, the score
        is ``0.2 ** 2 = 0.04``, and so on. The total score of an individual
        will be given by the normalised sum of the evaluation of each of its
        genes.
        """
        return self._evaluation_index

    @evaluation_index.setter
    def evaluation_index(self,
                         evaluation_index: float,
                         ) -> None:
        if not isinstance(evaluation_index, float):
            raise TypeError("'evaluation_index' must be 'float'")
        if evaluation_index <= 0.0:
            raise ValueError("'evaluation_index' must be a greater than 0.0")
        elif evaluation_index >= 1.0:
            raise ValueError("'evaluation_index' must be less than `1.0`")
        self._evaluation_index = evaluation_index

    @property
    def generation_number(self) -> Union[int, None]:
        r"""Read-only property, returns the number of the current generation
        (initial generation is ``0``).
        """
        return self._generation_number

    @property
    def population(self) -> Union[list, None]:
        r"""Read-only property, returns a list with all the population of the
        current generation.
        """
        return self._population

    @property
    def scores(self) -> list:
        r"""Read-only property, returns the list of individual scores of the
        current population. Scores are normalised.
        """
        return self._scores

    @property
    def fittest_individual(self) -> Union[list, None]:
        r"""Read-only property, returns the fittest individual of the current
        population.
        """
        try:
            return self._population[0]
        except TypeError:
            return None

    @property
    def fittest_individual_score(self) -> Union[list, float]:
        r"""Read-only property, returns the score of the fittest individual of
        the current population.
        """
        try:
            return self._scores[0]
        except TypeError:
            return None
