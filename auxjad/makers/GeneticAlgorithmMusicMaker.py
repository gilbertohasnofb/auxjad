from typing import Optional, Union

import abjad

from .. import mutate
from ..core.GeneticAlgorithm import GeneticAlgorithm


class GeneticAlgorithmMusicMaker():
    r"""Uses two :class:`auxjad.GeneticAlgorithm`'s, one for pitch and another
    for attack points, in order to create musical cells. At each call of
    :meth:`__call__`, it iterates the genetic algorithms by one generation, and
    returns an |abjad.Selection| created with the fittest pitch and attack
    point individuals.

    ..  note::

        Many of the properties of this class reflect the behaviour of
        properties of :class:`GeneticAlgorithm`. Some, such as
        :attr:`population_size`, :attr:`select_n_parents`,
        :attr:`keep_n_parents`, :attr:`mutation_chance`,
        :attr:`mutation_index`, and :attr:`evaluation_index`, have the same
        name as those in :class:`GeneticAlgorithm`. :attr:`pitch_target` and
        :attr:`attack_point_target`, :attr:`pitch_genes` and
        :attr:`attack_point_genes`, and :attr:`pitch_initial_individual` and
        :attr:`attack_point_initial_individual` work as
        :attr:`GeneticAlgorithm.target`, :attr:`GeneticAlgorithm.genes`, and
        :attr:`GeneticAlgorithm.initial_individual`, respectively.

        For the details of how these properties work, please refer to
        :class:`GeneticAlgorithm`'s documentation page.

    Basic usage:
        At its basic, this class needs a target and a list of genes for both
        pitches and attack points. The evaluation function will compare all
        individuals in the population against this target when scoring them.

        >>> maker = auxjad.GeneticAlgorithmMusicMaker(
        ...     pitch_target=["c'", "d'", "e'", "f'"],
        ...     pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        ...     attack_point_target=[0, 4, 8, 12],
        ...     attack_point_genes=list(range(16)),
        ... )
        >>> repr(maker)
        pitches: ["c'", "d'", "e'", "f'"]
        attack_points: [0, 4, 8, 12]
        >>> len(maker)
        4
        >>> notes = maker.target_music
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'4
                d'4
                e'4
                f'4
            }

        ..  figure:: ../_images/GeneticAlgorithmMusicMaker-ahfUfls3cq.png

        Calling the instance will apply the genetic algorithm process and
        output an |abjad.Selection| with the fittest  individual in the
        population.

        >>> notes = maker()
        >>> maker.generation_number
        0
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'4
                f'4
                ~
                f'8.
                e'16
                ~
                e'8
                a'8
            }

        ..  figure:: ../_images/GeneticAlgorithmMusicMaker-mIrHl4wwHA.png

        Subsequent calls will create new generations of individuals, always
        outputting the fittest measure.

        >>> notes = maker()
        >>> maker.generation_number
        1
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'4
                d'16
                e'8.
                ~
                e'4
                ~
                e'16
                g'8.
            }

        ..  figure:: ../_images/GeneticAlgorithmMusicMaker-hDxTq3Y2Ek.png

    :meth:`output_n`:
        The method :meth:`output_n` can be used to output `n` iterations of the
        process. They are output as a single |abjad.Selection|:

        >>> maker = auxjad.GeneticAlgorithmMusicMaker(
        ...     pitch_target=["c'", "d'", "e'", "f'"],
        ...     pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        ...     attack_point_target=[0, 4, 8, 12],
        ...     attack_point_genes=list(range(16)),
        ... )
        >>> notes = maker.output_n(5)
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 4/4
                r4
                r16
                c'8.
                d'16
                d'8.
                f'4
                c'2
                d'16
                c''8.
                f'4
                r16
                c'8.
                d'4
                f'4.
                f'8
                c'4
                d'8.
                e'16
                ~
                e'4
                e'4
                c'4
                d'4
                ~
                d'16
                e'8.
                e'4
            }

        ..  figure:: ../_images/GeneticAlgorithmMusicMaker-PrfaIjhEbL.png

    :attr:`pitch_genes`:
        While :attr:`attack_point_genes` must always take a :obj:`list` of
        :obj:`int`'s, :attr:`pitch_genes` can take a variety of object types.
        The implementation of this class uses |abjad.LeafMaker|, so pitches can
        take any objects accepted by that class. These include :obj:`int` and
        :obj:`str` for pitches, ``None`` for rests, :obj:`tuple` for chords,
        etc.

        >>> maker = auxjad.GeneticAlgorithmMusicMaker(
        ...     pitch_target=["c'", None, "e'", ("g'", "bf'")],
        ...     pitch_genes=[None,
        ...                  "c'",
        ...                  "d'",
        ...                  "e'",
        ...                  "f'",
        ...                  "g'",
        ...                  ("g'", "a'"),
        ...                  ("g'", "bf'"),
        ...                  ("g'", "c''"),
        ...                  ],
        ...     attack_point_target=[0, 4, 8, 12],
        ...     attack_point_genes=list(range(16)),
        ...     population_size=50,
        ... )
        >>> notes = maker.output_n(5)
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 4/4
                <g' c''>4
                g'4
                ~
                g'16
                <g' c''>8.
                <g' c''>4
                c'2
                e'8.
                r16
                r4
                c'4
                r4
                r16
                e'8.
                <g' a'>4
                c'4
                r4
                e'8.
                <g' a'>16
                ~
                <g' a'>4
                c'4
                r4
                e'8.
                <g' a'>16
                ~
                <g' a'>4
            }

        ..  figure:: ../_images/GeneticAlgorithmMusicMaker-etoHzdnAIu.png

        Which is equivalent to:

        >>> maker = auxjad.GeneticAlgorithmMusicMaker(
        ...     pitch_target=[0, None, 4, (7, 10)],
        ...     pitch_genes=[None, 0, 2, 4, 5, 7, (7, 9), (7, 10), (7, 12)],
        ...     attack_point_target=[0, 4, 8, 12],
        ...     attack_point_genes=list(range(16)),
        ...     population_size=50,
        ... )
        >>> notes = maker.output_n(5)
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 4/4
                <g' c''>4
                g'4
                ~
                g'16
                <g' c''>8.
                <g' c''>4
                c'2
                e'8.
                r16
                r4
                c'4
                r4
                r16
                e'8.
                <g' a'>4
                c'4
                r4
                e'8.
                <g' a'>16
                ~
                <g' a'>4
                c'4
                r4
                e'8.
                <g' a'>16
                ~
                <g' a'>4
            }

        ..  figure:: ../_images/GeneticAlgorithmMusicMaker-AfDY1QYNhW.png

    :attr:`units_per_window` and :attr:`duration_unit`:
        By default, there are ``16`` attack points in a window, each lasting
        for ``abjad.Duration((1, 16))``. These can be changed using
        :attr:`units_per_window` and :attr:`duration_unit`:

        >>> maker = auxjad.GeneticAlgorithmMusicMaker(
        ...     pitch_target=["c'", "d'", "e'", "f'"],
        ...     pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        ...     attack_point_target=[0, 8, 16, 24],
        ...     attack_point_genes=list(range(32)),
        ...     duration_unit=abjad.Duration((1, 32)),
        ...     units_per_window=32,
        ... )
        >>> notes = maker.output_n(5)
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'8.
                e'16
                ~
                e'16.
                e'32
                ~
                e'8
                ~
                e'32
                b'4...
                c'8.
                d'16
                ~
                d'2
                f'4
                c'4
                d'8..
                e'32
                ~
                e'4
                c'4
                c'4
                d'8..
                e'32
                ~
                e'4
                e'4
                c'4
                d'8..
                e'32
                ~
                e'4
                f'4
            }

        ..  figure:: ../_images/GeneticAlgorithmMusicMaker-AqHoQPgphf.png

    :attr:`omit_time_signature`:
        By default, a time signature is added to the output automatically:

        >>> maker = auxjad.GeneticAlgorithmMusicMaker(
        ...     pitch_target=["c'", "d'", "e'", "f'", "g'"],
        ...     pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        ...     attack_point_target=[0, 4, 8, 12, 16],
        ...     attack_point_genes=list(range(20)),
        ...     units_per_window=20,
        ... )
        >>> notes = maker.output_n(5)
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 5/4
                r8
                c'8
                d'8
                f'4.
                e'4..
                g'16
                c'8.
                d'16
                ~
                d'4
                ~
                d'16
                g'16
                f'8
                ~
                f'4
                g'4
                c'4
                d'8.
                e'16
                ~
                e'4
                a'4
                f'4
                c'4
                d'8.
                g'16
                ~
                g'4
                f'4
                g'4
                c'4
                d'4
                g'4
                f'4
                g'4
            }

        ..  figure:: ../_images/GeneticAlgorithmMusicMaker-bbsRWshiDI.png

        Setting :attr:`omit_time_signature` to ``True`` will result in no time
        signature. Note that the output might need to be cleaned up using
        |abjad.Meter.rewrite_meter()|.

        >>> maker = auxjad.GeneticAlgorithmMusicMaker(
        ...     pitch_target=["c'", "d'", "e'", "f'", "g'"],
        ...     pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        ...     attack_point_target=[0, 4, 8, 12, 16],
        ...     attack_point_genes=list(range(20)),
        ...     units_per_window=20,
        ...     omit_time_signature=True,
        ... )
        >>> notes = maker.output_n(5)
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                r8
                c'8
                d'8
                f'4.
                e'4..
                g'16
                c'8.
                d'4.
                g'16
                f'4.
                g'4
                c'4
                d'8.
                e'4
                ~
                e'16
                a'4
                f'4
                c'4
                d'8.
                g'4
                ~
                g'16
                f'4
                g'4
                c'4
                d'4
                g'4
                f'4
                g'4
            }

        ..  figure:: ../_images/GeneticAlgorithmMusicMaker-IVSrzPV4OT.png

    :attr:`time_signatures`:
        Time signatures can also be enforced in the output. Set
        :attr:`time_signatures` to a single |abjad.TimeSignature| or a
        :obj:`list` of |abjad.TimeSignature|'s as needed.

        A single |abjad.TimeSignature| is applied to all measures:

        >>> maker = auxjad.GeneticAlgorithmMusicMaker(
        ...     pitch_target=["c'", "d'", "e'", "f'"],
        ...     pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        ...     attack_point_target=[0, 4, 8, 12],
        ...     attack_point_genes=list(range(16)),
        ...     duration_unit=abjad.Duration((1, 32)),
        ...     time_signatures=abjad.TimeSignature((2, 2))
        ... )
        >>> notes = maker.output_n(5)
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 2/2
                r32
                c''16.
                ~
                c''32
                f'16.
                ~
                f'32
                e'16.
                f'8
                r2
                r32
                c'16.
                d'8
                ~
                d'16
                e'16
                e'8
                r2
                c'8.
                d'16
                e'8
                f'8
                r2
                r32
                c'16.
                d'8
                e'8
                f'8
                r2
                r32
                c'16.
                d'8
                e'8
                f'8
                r2
            }

        ..  figure:: ../_images/GeneticAlgorithmMusicMaker-Xc9iKXJoEx.png

        A :obj:`list` of |abjad.TimeSignature|'s is applied cyclically.

        >>> maker = auxjad.GeneticAlgorithmMusicMaker(
        ...     pitch_target=["c'", "d'", "e'", "f'", "g'"],
        ...     pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        ...     attack_point_target=[0, 4, 8, 12, 16],
        ...     attack_point_genes=list(range(20)),
        ...     duration_unit=abjad.Duration((1, 16)),
        ...     units_per_window=20,
        ...     time_signatures=[abjad.TimeSignature((2, 4)),
        ...                      abjad.TimeSignature((3, 4)),
        ...                      ],
        ... )
        >>> notes = maker.output_n(5)
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 2/4
                r8
                c'8
                d'8
                f'8
                ~
                \time 3/4
                f'4
                e'4..
                g'16
                \time 2/4
                c'8.
                d'16
                ~
                d'4
                ~
                \time 3/4
                d'16
                g'16
                f'4.
                g'4
                \time 2/4
                c'4
                d'8.
                e'16
                ~
                \time 3/4
                e'4
                a'4
                f'4
                \time 2/4
                c'4
                d'8.
                g'16
                ~
                \time 3/4
                g'4
                f'4
                g'4
                \time 2/4
                c'4
                d'4
                \time 3/4
                g'4
                f'4
                g'4
            }

        ..  figure:: ../_images/GeneticAlgorithmMusicMaker-lJCYtjGY52.png

    :attr:`pitch_score_bias`:
        Pitches and attack points are scored separately and, by default,
        contribute equally to the total score of each individual. To change the
        bias of the pitch score, set :attr:`pitch_score_bias` to a value
        between ``0.0`` and ``1.0``.

        This is the default output:

        >>> maker = auxjad.GeneticAlgorithmMusicMaker(
        ...     pitch_target=["c'", "d'", "e'", "f'"],
        ...     pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        ...     attack_point_target=[0, 4, 8, 12],
        ...     attack_point_genes=list(range(16)),
        ... )
        >>> notes = maker.output_n(5)
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 4/4
                r16
                c'8
                d'16
                ~
                d'4
                f'4
                d'4
                r16
                c'8.
                d'8
                e'8
                ~
                e'8.
                f'16
                ~
                f'4
                c'4
                d'4
                e'4
                f'4
                c'4
                d'4
                e'4
                f'4
                c'4
                d'4
                e'4
                f'4
            }

        ..  figure:: ../_images/GeneticAlgorithmMusicMaker-VEinjiTe3F.png

        With a high :attr:`pitch_score_bias`, pitch convergence will tend to be
        faster at the expense of attack points:

        >>> maker = auxjad.GeneticAlgorithmMusicMaker(
        ...     pitch_target=["c'", "d'", "e'", "f'"],
        ...     pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        ...     attack_point_target=[0, 4, 8, 12],
        ...     attack_point_genes=list(range(16)),
        ...     pitch_score_weight=0.95,
        ... )
        >>> notes = maker.output_n(5)
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 4/4
                r8
                c'16
                d'16
                ~
                d'4
                ~
                d'8
                e'4
                d'8
                r8
                c'16
                d'16
                ~
                d'2
                ~
                d'16
                e'8.
                c'16
                d'8.
                ~
                d'8.
                e'16
                ~
                e'4
                f'4
                c'16
                d'8.
                ~
                d'8.
                e'16
                ~
                e'4
                f'4
                c'4
                ~
                c'16
                d'8
                e'16
                ~
                e'4
                f'4
            }

        ..  figure:: ../_images/GeneticAlgorithmMusicMaker-iVD6l66hNl.png


        In contrast, a low :attr:`pitch_score_bias`, attack point convergence
        will tend to be  faster at the expense of pitches:

        >>> maker = auxjad.GeneticAlgorithmMusicMaker(
        ...     pitch_target=["c'", "d'", "e'", "f'"],
        ...     pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        ...     attack_point_target=[0, 4, 8, 12],
        ...     attack_point_genes=list(range(16)),
        ...     pitch_score_weight=0.05,
        ... )
        >>> notes = maker.output_n(5)
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 4/4
                e'16
                c''4..
                f'4
                c''4
                e'4
                d'4
                d'4
                f'4
                e'4
                d'4
                d'4
                f'4
                e'4
                d'4
                d'4
                f'4
                e'4
                d'4
                d'4
                f'4
            }

        ..  figure:: ../_images/GeneticAlgorithmMusicMaker-1Ex8sgcS2s.png

    :attr:`attack_points_mode`:
        When using this class in attack points mode, each note will last a
        single unit instead of being extended until the next attack point:

        >>> maker = auxjad.GeneticAlgorithmMusicMaker(
        ...     pitch_target=["c'", "d'", "e'", "f'"],
        ...     pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        ...     attack_point_target=[0, 4, 8, 12],
        ...     attack_point_genes=list(range(16)),
        ...     attack_points_mode=True,
        ... )
        >>> notes = maker.output_n(5)
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 4/4
                e'16
                r8.
                c'16
                r16
                r16
                g'16
                r4
                f'16
                r8.
                c'16
                r8.
                d'16
                r8.
                e'16
                c'16
                r4.
                c'16
                r8.
                d'16
                r16
                r16
                e'16
                r4
                f'16
                r8.
                c'16
                r8.
                d'16
                r8.
                e'16
                r8.
                f'16
                r8.
                c'16
                r8.
                d'16
                r8.
                e'16
                r8.
                f'16
                r8.
            }

        ..  figure:: ../_images/GeneticAlgorithmMusicMaker-5aInHHwMol.png
    """
    ### CLASS VARIABLES ###

    __slots__ = ('_pitch_target',
                 '_pitch_genes',
                 '_pitch_initial_individual',
                 '_attack_point_target',
                 '_attack_point_genes',
                 '_attack_point_initial_individual',
                 '_population_size',
                 '_select_n_parents',
                 '_mutation_chance',
                 '_mutation_index',
                 '_evaluation_index',
                 '_duration_unit',
                 '_units_per_window',
                 '_omit_time_signature',
                 '_time_signatures',
                 '_attack_points_mode',
                 '_pitch_score_bias',
                 '_pitch_ga',
                 '_attack_point_ga',
                 '_fittest_measure',
                 '_fittest_pitch_individual',
                 '_fittest_attack_point_individual',
                 '_pitch_population',
                 '_attack_point_population',
                 '_scores',
                 '_target_music',
                 '_total_duration',
                 )

    ### INITIALISER ###

    def __init__(self,
                 *,
                 pitch_target: list,
                 pitch_genes: list,
                 attack_point_target: list,
                 attack_point_genes: list,
                 duration_unit: abjad.Duration = abjad.Duration((1, 16)),
                 units_per_window: int = 16,
                 pitch_initial_individual: Optional[list] = None,
                 attack_point_initial_individual: Optional[list] = None,
                 population_size: int = 100,
                 select_n_parents: int = 10,
                 keep_n_parents: int = 0,
                 mutation_chance: float = 0.2,
                 mutation_index: float = 0.1,
                 evaluation_index: float = 0.2,
                 omit_time_signature: bool = False,
                 time_signatures: Optional[list] = None,
                 attack_points_mode: bool = False,
                 pitch_score_bias: float = 0.5,
                 ) -> None:
        r'Initialises self.'
        if len(pitch_target) != len(attack_point_target):
            raise ValueError("'pitch_target' and 'attack_point_target' must "
                             "have the same length")
        self._pitch_ga = GeneticAlgorithm(
            target=pitch_target,
            genes=pitch_genes,
            initial_individual=pitch_initial_individual,
            population_size=population_size,
            select_n_parents=select_n_parents,
            keep_n_parents=keep_n_parents,
            mutation_chance=mutation_chance,
            mutation_index=mutation_index,
            evaluation_index=evaluation_index,
        )
        self._attack_point_ga = GeneticAlgorithm(
            target=attack_point_target,
            genes=attack_point_genes,
            initial_individual=attack_point_initial_individual,
            population_size=population_size,
            select_n_parents=select_n_parents,
            keep_n_parents=keep_n_parents,
            mutation_chance=mutation_chance,
            mutation_index=mutation_index,
            evaluation_index=evaluation_index,
        )
        if not isinstance(duration_unit, abjad.Duration):
            raise TypeError("'duration_unit' must be 'abjad.Duration'")
        if not isinstance(units_per_window, int):
            raise TypeError("'units_per_window' must be 'int'")
        if units_per_window < max(self._attack_point_ga.genes):
            raise TypeError("'units_per_window' must be larger than the max "
                            "value in 'attack_point_genes'")
        self._duration_unit = duration_unit
        self._units_per_window = units_per_window
        self._total_duration = self._units_per_window * self._duration_unit
        self.omit_time_signature = omit_time_signature
        self.time_signatures = time_signatures
        self.attack_points_mode = attack_points_mode
        self.pitch_score_bias = pitch_score_bias
        self._target_individual_to_measure()

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        r"""Returns interpreter representation of :attr:`target`'s of both
        instances of the genetic algorithm (pitches and attack points).
        """
        string = 'pitches: ' + repr(self._pitch_ga._target) + '\n'
        string += 'attack_points: ' + repr(self._attack_point_ga._target)
        return string

    def __len__(self) -> int:
        r'Returns the number of genes in each individual.'
        return len(self._pitch_ga._target)

    def __call__(self) -> abjad.Selection:
        r"""Calls the genetic algorithm process for one iteration, returning an
        |abjad.Selection|. Generates a new generation of length
        :attr:`population_size` via reproduction and mutation processes and
        scores each individual using the evaluation function.
        """
        self._pitch_ga._generate_population()
        self._pitch_ga._score_population()
        self._attack_point_ga._generate_population()
        for attack_point_individual in self._attack_point_ga._population:
            attack_point_individual.sort()
        self._attack_point_ga._score_population()
        self._sort_population_by_evaluation()
        self._fittest_individual_to_measure()
        return self.fittest_measure

    def __next__(self) -> None:
        r"""Calls the genetic algorithm process for one iteration. Generates a
        new generation of length :attr:`population_size` via reproduction and
        mutation processes and scores each individual using the evaluation
        function.
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
        self._pitch_ga.reset()
        self._attack_point_ga.reset()

    def output_n(self,
                 n: int
                 ) -> abjad.Selection:
        r"""Goes through ``n`` iterations of the genetic algorithm process and
        outputs a single |abjad.Selection|.
        """
        if not isinstance(n, int):
            raise TypeError("first positional argument must be 'int'")
        if n < 1:
            raise ValueError("first positional argument must be a positive "
                             "'int'")
        dummy_container = abjad.Container()
        for _ in range(n):
            dummy_container.append(self.__call__())
        mutate.remove_repeated_time_signatures(dummy_container[:])
        output = dummy_container[:]
        dummy_container[:] = []
        return output

    ### PRIVATE METHODS ###

    def _sort_population_by_evaluation(self) -> None:
        r"""Sorts the population (and their scores) according to the evaluation
        of its individuals.
        """
        self._scores = []
        for pitch_score, attack_score in zip(self._pitch_ga._scores,
                                             self._attack_point_ga._scores):
            combined_score = pitch_score * self._pitch_score_bias
            combined_score += attack_score * (1.0 - self._pitch_score_bias)
            combined_score /= 2
            self._scores.append(combined_score)
        zipped_lists = list(zip(self._scores,
                                self._pitch_ga._population,
                                self._attack_point_ga._population,
                                ))
        zipped_lists.sort(
            key=lambda tuple_triple: tuple_triple[0],
            reverse=True,
        )
        self._pitch_population = [pitch_gene for _, pitch_gene, _
                                  in zipped_lists]
        self._attack_point_population = [attack_point_gene
                                         for _, _, attack_point_gene
                                         in zipped_lists]
        self._scores = [score for score, _, _ in zipped_lists]
        self._pitch_ga._population = self._pitch_population[:]
        self._attack_point_ga._population = self._attack_point_population[:]

    def _fittest_individual_to_measure(self) -> None:
        r"""Converts the fittest pitch and attack point individuals to a
        measure of music.
        """
        self._fittest_measure = self._make_measure(
            self.fittest_attack_point_individual[:],
            self.fittest_pitch_individual[:],
        )

    def _target_individual_to_measure(self) -> None:
        r"""Converts the target pitch and attack point individuals to a
        measure of music.
        """
        self._target_music = self._make_measure(
            self._attack_point_ga.target[:],
            self._pitch_ga.target[:],
        )

    @staticmethod
    def _sort_by_attack_point(attack_points: list,
                              pitches: list,
                              ) -> tuple:
        r'Sorts pitches and attack points.'
        zipped_lists = []
        # zipping while removing simultaneous attacks
        for attack_point, pitch in zip(attack_points, pitches):
            if attack_point not in (p for p, _ in zipped_lists):
                zipped_lists.append((attack_point, pitch))
        zipped_lists.sort(
            key=lambda tuple_pair: tuple_pair[0],
        )
        attack_points = [attack_point for attack_point, _ in zipped_lists]
        pitches = [pitch for _, pitch in zipped_lists]
        return attack_points, pitches

    def _convert_attack_points_to_durations(self,
                                            attack_points: list,
                                            pitches: list,
                                            ) -> tuple:
        r"""Converts attack points to effective durations. Adds an initial rest
        if first attack point is not at the 0-th position.
        """
        if attack_points[0] != 0:
            attack_points.insert(0, 0)
            pitches.insert(0, None)
        durations = []
        attack_points.append(self._units_per_window)
        for i in range(len(attack_points) - 1):
            difference = attack_points[i + 1] - attack_points[i]
            duration = difference * self.duration_unit
            durations.append(duration)
        return durations, pitches

    def _make_measure(self,
                      attack_points,
                      pitches,
                      ) -> None:
        r"""Converts a list of pitch and attack point individuals into a
        measure of music.
        """
        dummy_container = abjad.Container()
        sorted_attack_points, sorted_pitches = self._sort_by_attack_point(
            attack_points[:],
            pitches[:],
        )
        if not self._attack_points_mode:
            durations, pitches = self._convert_attack_points_to_durations(
                sorted_attack_points,
                sorted_pitches,
            )
            notes = abjad.LeafMaker()(
                pitches,
                durations,
            )
            dummy_container = abjad.Container(notes)
        else:
            notes = abjad.Selection()
            for i in range(self._units_per_window):
                if i in sorted_attack_points:
                    pitch_index = sorted_attack_points.index(i)
                    notes += abjad.LeafMaker()(
                        [sorted_pitches[pitch_index]],
                        [self._duration_unit],
                    )
                else:
                    rest = abjad.Rest(self._duration_unit)
                    notes += abjad.select(rest).leaves()
            dummy_container = abjad.Container(notes)
        # adding time signature
        if not self._omit_time_signature:
            if self._time_signatures is None:
                time_signature = abjad.TimeSignature((self._total_duration))
                time_signature.simplify_ratio()
                abjad.attach(time_signature,
                             dummy_container[0],
                             )
                mutate.auto_rewrite_meter(dummy_container)
            else:
                mutate.enforce_time_signature(
                    dummy_container,
                    self._time_signatures,
                )
        return dummy_container[:]

    ### PUBLIC PROPERTIES ###

    @property
    def duration_unit(self) -> abjad.Duration:
        r'Unit for the duration grid. Default is abjad.Duration((1, 16)).'
        return self._duration_unit

    @duration_unit.setter
    def duration_unit(self,
                      duration_unit: abjad.Duration,
                      ) -> None:
        if not isinstance(duration_unit, abjad.Duration):
            raise TypeError("'duration_unit' must be 'abjad.Duration'")
        self._duration_unit = duration_unit
        self._total_duration = self._units_per_window * self._duration_unit

    @property
    def units_per_window(self) -> int:
        r'Number of units per window. Default is 16.'
        return self._units_per_window

    @units_per_window.setter
    def units_per_window(self,
                         units_per_window: int,
                         ) -> None:
        if not isinstance(units_per_window, int):
            raise TypeError("'units_per_window' must be 'int'")
        if units_per_window < max(self._attack_point_ga.genes):
            raise TypeError("'units_per_window' must be larger than the max "
                            "value in 'attack_point_genes'")
        self._units_per_window = units_per_window
        self._total_duration = self._units_per_window * self._duration_unit

    @property
    def omit_time_signature(self) -> bool:
        r"""When ``True``, a time signature won't be added to the first leaf of
        the output."""
        return self._omit_time_signature

    @omit_time_signature.setter
    def omit_time_signature(self,
                            omit_time_signature: bool,
                            ) -> None:
        if not isinstance(omit_time_signature, bool):
            raise TypeError("'omit_time_signature' must be 'bool'")
        self._omit_time_signature = omit_time_signature

    @property
    def time_signatures(self) -> list:
        r"""List of time signatures to be enforced on output. It is important
        to note that :attr:`omit_time_signature` must be ``True`` for it to
        take effect.
        """
        return self._time_signatures

    @time_signatures.setter
    def time_signatures(self,
                        time_signatures: Optional[list],
                        ) -> None:
        if time_signatures is not None:
            if isinstance(time_signatures, abjad.TimeSignature):
                time_signatures = [time_signatures]
            elif not isinstance(time_signatures, list):
                raise TypeError("'time_signatures' must be a 'list' of "
                                "'abjad.TimeSignature' or 'None'")
            if not all(isinstance(ts, abjad.TimeSignature) for ts
                       in time_signatures):
                raise TypeError("'time_signatures' must be a 'list' of "
                                "'abjad.TimeSignature' or 'None'")
        self._time_signatures = time_signatures

    @property
    def attack_points_mode(self) -> bool:
        r"""When ``True``, each note will last only for the duration of the
        unit, instead of extending it to the next attack point."""
        return self._attack_points_mode

    @attack_points_mode.setter
    def attack_points_mode(self,
                           attack_points_mode: bool,
                           ) -> None:
        if not isinstance(attack_points_mode, bool):
            raise TypeError("'attack_points_mode' must be 'bool'")
        self._attack_points_mode = attack_points_mode

    @property
    def pitch_target(self) -> list:
        r'Target pitch individual used for evaluation.'
        return self._pitch_ga.target

    @pitch_target.setter
    def pitch_target(self,
                     pitch_target: list,
                     ) -> None:
        if len(pitch_target) != len(self._attack_point_ga.target):
            raise ValueError("'pitch_target' must be the same length as "
                             "'attack_point_target'")
        self._pitch_ga.target = pitch_target
        self._target_individual_to_measure()

    @property
    def pitch_genes(self) -> list:
        r'List of possible genes that make up all pitch individuals.'
        return self._pitch_ga.genes

    @pitch_genes.setter
    def pitch_genes(self,
                    pitch_genes: list,
                    ) -> None:
        self._pitch_ga.genes = pitch_genes

    @property
    def pitch_initial_individual(self) -> Union[list, None]:
        r'Optional initial pitch individual.'
        return self._pitch_ga.initial_individual

    @pitch_initial_individual.setter
    def pitch_initial_individual(self,
                                 pitch_initial_individual: Optional[list],
                                 ) -> None:
        self._pitch_ga.initial_individual = pitch_initial_individual

    @property
    def attack_point_target(self) -> list:
        r'Target attack point individual used for evaluation.'
        return self._attack_point_ga.target

    @attack_point_target.setter
    def attack_point_target(self,
                            attack_point_target: list,
                            ) -> None:
        if len(attack_point_target) != len(self._pitch_ga.target):
            raise ValueError("'attack_point_target' must be the same length "
                             "as 'pitch_target'")
        self._attack_point_ga.target = attack_point_target
        self._target_individual_to_measure()

    @property
    def attack_point_genes(self) -> list:
        r'List of possible genes that make up all attack point individuals.'
        return self._attack_point_ga.genes

    @attack_point_genes.setter
    def attack_point_genes(self,
                           attack_point_genes: list,
                           ) -> None:
        self._attack_point_ga.genes = attack_point_genes

    @property
    def attack_point_initial_individual(self) -> Union[list, None]:
        r'Optional initial attack point individual.'
        return self._attack_point_ga.initial_individual

    @attack_point_initial_individual.setter
    def attack_point_initial_individual(
        self,
        attack_point_initial_individual: Optional[list],
    ) -> None:
        self._attack_point_ga.initial_individual = (
            attack_point_initial_individual
        )

    @property
    def population_size(self) -> int:
        r'Number of individuals in any given generation.'
        return self._pitch_ga.population_size

    @population_size.setter
    def population_size(self,
                        population_size: int,
                        ) -> None:
        self._pitch_ga.population_size = population_size
        self._attack_point_ga.population_size = population_size

    @property
    def select_n_parents(self) -> int:
        r"""Number of the best-fit individuals that are selected to be parents
        of the next generation. They also survive into the next generation.
        """
        return self._pitch_ga.select_n_parents

    @select_n_parents.setter
    def select_n_parents(self,
                         select_n_parents: int,
                         ) -> None:
        self._pitch_ga.select_n_parents = select_n_parents
        self._attack_point_ga.select_n_parents = select_n_parents

    @property
    def keep_n_parents(self) -> int:
        r"""Number of the best-fit individuals that survive into the next
        generation. Default is ``0``.
        """
        return self._pitch_ga.keep_n_parents

    @keep_n_parents.setter
    def keep_n_parents(self,
                       keep_n_parents: int,
                       ) -> None:
        self._pitch_ga.keep_n_parents = keep_n_parents
        self._attack_point_ga.keep_n_parents = keep_n_parents

    @property
    def mutation_chance(self) -> float:
        r'Percentage of the total population who will experience mutation.'
        return self._pitch_ga.mutation_chance

    @mutation_chance.setter
    def mutation_chance(self,
                        mutation_chance: float,
                        ) -> None:
        self._pitch_ga.mutation_chance = mutation_chance
        self._attack_point_ga.mutation_chance = mutation_chance

    @property
    def mutation_index(self) -> float:
        r"""Given an individual selected to undergo mutation, this index gives
        the percentage of genes of that individual which will be mutated.
        """
        return self._pitch_ga.mutation_index

    @mutation_index.setter
    def mutation_index(self,
                       mutation_index: float,
                       ) -> None:
        self._pitch_ga.mutation_index = mutation_index
        self._attack_point_ga.mutation_index = mutation_index

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
        return self._pitch_ga.evaluation_index

    @evaluation_index.setter
    def evaluation_index(self,
                         evaluation_index: float,
                         ) -> None:
        self._pitch_ga.evaluation_index = evaluation_index
        self._attack_point_ga.evaluation_index = evaluation_index

    @property
    def pitch_score_bias(self) -> float:
        r"""By default, the score of each measure gives equal weight to pitches
        as it gives to attack points. Changing this to a different value will
        make the pitch score contribute more or less to the total score of a
        measure.
        """
        return self._pitch_score_bias

    @pitch_score_bias.setter
    def pitch_score_bias(self,
                         pitch_score_bias: float,
                         ) -> None:
        if not isinstance(pitch_score_bias, float):
            raise TypeError("'pitch_score_bias' must be 'float'")
        if pitch_score_bias < 0.0 or pitch_score_bias > 1.0:
            raise ValueError("'pitch_score_bias' must be between 0.0 and "
                             "1.0")
        self._pitch_score_bias = pitch_score_bias

    @property
    def fittest_measure(self) -> Union[abjad.Selection, None]:
        r"""Read-only property, returns the fittest individual of the current
        population as an |abjad.Selection|.
        """
        return abjad.mutate.copy(self._fittest_measure)

    @property
    def target_music(self) -> abjad.Selection:
        r'Read-only property, returns the target as an |abjad.Selection|.'
        return abjad.mutate.copy(self._target_music)

    @property
    def total_duration(self) -> list:
        r'Read-only property, returns the total duration of the window.'
        return self._total_duration

    @property
    def generation_number(self) -> list:
        r"""Read-only property, returns the number of the current generation
        (initial generation is `0`).
        """
        return self._pitch_ga._generation_number

    @property
    def pitch_population(self) -> Union[list, None]:
        r"""Read-only property, returns a list with all the population of the
        current generation.
        """
        return self._pitch_population

    @property
    def attack_point_population(self) -> Union[list, None]:
        r"""Read-only property, returns a list with all the population of the
        current generation.
        """
        return self._attack_point_population

    @property
    def scores(self) -> list:
        r"""Read-only property, returns the list of individual scores of the
        current population. Scores are normalised.
        """
        return self._scores

    @property
    def fittest_pitch_individual(self) -> Union[list, None]:
        r"""Read-only property, returns the fittest individual of the current
        population.
        """
        try:
            return self._pitch_population[0]
        except TypeError:
            return None

    @property
    def fittest_attack_point_individual(self) -> Union[list, None]:
        r"""Read-only property, returns the fittest individual of the current
        population.
        """
        try:
            return self._attack_point_population[0]
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
