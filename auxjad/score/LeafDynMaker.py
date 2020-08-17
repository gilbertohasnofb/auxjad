from typing import Any

import abjad


class LeafDynMaker(abjad.LeafMaker):
    r"""This class creates leaves and logical ties from :obj:`list`'s of
    pitches, durations, dynamics, and articulations. It is an extension of
    |abjad.LeafMaker| which can take optional :obj:`list`'s of dynamics and
    articulations.

    Basic usage:
        Usage is similar to |abjad.LeafMaker|:

        >>> pitches = [0, 2, 4, 5, 7, 9]
        >>> durations = [(1, 32), (2, 32), (3, 32), (4, 32), (5, 32), (6, 32)]
        >>> dynamics = ['pp', 'p', 'mp', 'mf', 'f', 'ff']
        >>> articulations = ['.', '>', '-', '_', '^', '+']
        >>> leaf_dyn_maker = auxjad.LeafDynMaker()
        >>> notes = leaf_dyn_maker(pitches, durations, dynamics, articulations)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'32
            \pp
            -\staccato
            d'16
            \p
            -\accent
            e'16.
            \mp
            -\tenuto
            f'8
            \mf
            -\portato
            g'8
            \f
            -\marcato
            ~
            g'32
            a'8.
            \ff
            -\stopped
        }

        .. figure:: ../_images/LeafDynMaker-iv96zmptned.png

    ``pitches``:
        Tuple elements in ``pitches`` result in chords. None-valued elements
        in ``pitches`` result in rests:

        >>> pitches = [5, None, (0, 2, 7)]
        >>> durations = [(1, 4), (1, 8), (1, 16)]
        >>> dynamics = ['p', None, 'f']
        >>> articulations = ['staccato', None, 'tenuto']
        >>> leaf_dyn_maker = auxjad.LeafDynMaker()
        >>> notes = leaf_dyn_maker(pitches, durations, dynamics, articulations)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            f'4
            \p
            -\staccato
            r8
            <c' d' g'>16
            \f
            -\tenuto
        }

        .. figure:: ../_images/LeafDynMaker-odpaavswk29.png

    ``omit_repeated_dynamics``:
        Can omit repeated dynamics with the keyword argument
        ``omit_repeated_dynamics``:

        >>> pitches = [0, 2, 4, 5, 7, 9]
        >>> durations = [(1, 32), (2, 32), (3, 32), (4, 32), (5, 32), (6, 32)]
        >>> dynamics = ['pp', 'pp', 'mp', 'f', 'f', 'p']
        >>> leaf_dyn_maker = auxjad.LeafDynMaker()
        >>> notes = leaf_dyn_maker(pitches,
        ...                        durations,
        ...                        dynamics,
        ...                        omit_repeated_dynamics=True,
        ...                        )
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'32
            \pp
            d'16
            e'16.
            \mp
            f'8
            \f
            g'8
            ~
            g'32
            a'8.
            \p
        }

        .. figure:: ../_images/LeafDynMaker-jryhls4d6ic.png

    ``dynamics`` and ``articulations``:
        The lengths ``dynamics`` and ``articulations`` can be shorter than the
        lengths of ``pitches`` and ``durations`` (whatever is the greatest):

        >>> pitches = [0, 2, 4, 5, 7, 9, 11, 12]
        >>> durations = (1, 4)
        >>> dynamics = ['p', 'f', 'ff']
        >>> articulations = ['.', '>']
        >>> leaf_dyn_maker = auxjad.LeafDynMaker()
        >>> notes = leaf_dyn_maker(pitches, durations, dynamics, articulations)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \p
            -\staccato
            d'4
            \f
            -\accent
            e'4
            \ff
            f'4
            g'4
            a'4
            b'4
            c''4
        }

        .. figure:: ../_images/LeafDynMaker-1losyp9vc1di.png

    ``cyclic_dynamics`` and ``cyclic_articulations``:
        If the lengths of either ``dynamics`` and ``articulations`` are shorter
        than the lengths of ``pitches`` and ``durations`` (whatever is the
        greatest), use the optional keyword arguments ``cyclic_dynamics`` and
        ``cyclic_articulations`` to apply those parameters cyclically:

        >>> pitches = [0, 2, 4, 5, 7, 9, 11, 12]
        >>> durations = (1, 4)
        >>> dynamics = ['p', 'f', 'ff']
        >>> articulations = ['.', '>']
        >>> leaf_dyn_maker = auxjad.LeafDynMaker()
        >>> notes = leaf_dyn_maker(pitches,
        ...                        durations,
        ...                        dynamics,
        ...                        articulations,
        ...                        cyclic_dynamics=True,
        ...                        cyclic_articulations=True,
        ...                        )
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \p
            - \staccato
            d'4
            \f
            - \accent
            e'4
            \ff
            - \staccato
            f'4
            \p
            - \accent
            g'4
            \f
            - \staccato
            a'4
            \ff
            - \accent
            b'4
            \p
            - \staccato
            c''4
            \f
            - \accent
        }

        .. figure:: ../_images/LeafDynMaker-x8zhyel42i.png

    ``articulations`` and ``dynamics`` of length ``1``:
        If the length of ``articulations`` or ``dynamics`` is ``1``, they will
        be applied only to the first element.

        >>> pitches = [0, 2, 4, 5, 7, 9, 11, 12]
        >>> durations = (1, 4)
        >>> dynamics = 'p'
        >>> articulations = '.'
        >>> leaf_dyn_maker = auxjad.LeafDynMaker()
        >>> notes = leaf_dyn_maker(pitches, durations, dynamics, articulations)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \p
            -\staccato
            d'4
            e'4
            f'4
            g'4
            a'4
            b'4
            c''4
        }

        .. figure:: ../_images/LeafDynMaker-wwl4pcpmwhv232n7j7ws.png

    ``cyclic_dynamics`` and ``cyclic_articulations`` of length ``1``:
        To apply them to all elements, use the ``cyclic_dynamics`` and
        ``cyclic_articulations`` optioanl keywords.

        >>> pitches = [0, 2, 4, 5, 7, 9, 11, 12]
        >>> durations = (1, 4)
        >>> dynamics = 'p'
        >>> articulations = '.'
        >>> leaf_dyn_maker = auxjad.LeafDynMaker()
        >>> notes = leaf_dyn_maker(pitches,
        ...                        durations,
        ...                        dynamics,
        ...                        articulations,
        ...                        cyclic_articulations=True,
        ...                        )
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            \p
            -\staccato
            d'4
            -\staccato
            e'4
            -\staccato
            f'4
            -\staccato
            g'4
            -\staccato
            a'4
            -\staccato
            b'4
            - \staccato
            c''4
            - \staccato
        }

        .. figure:: ../_images/LeafDynMaker-s5ic146v4qb.png

    Accepted types:
        Similarly to Abjad's native classes, it accepts many types of elements
        in its input :obj:`list`'s:

        >>> pitches = [0,
        ...            "d'",
        ...            'E4',
        ...            abjad.NumberedPitch(5),
        ...            abjad.NamedPitch("g'"),
        ...            abjad.NamedPitch('A4'),
        ...            ]
        >>> durations = [(1, 32),
        ...              '2/32',
        ...              abjad.Duration('3/32'),
        ...              abjad.Duration(0.125),
        ...              abjad.Duration(5, 32),
        ...              abjad.Duration(6 / 32),
        ...              ]
        >>> dynamics = ['p',
        ...             abjad.Dynamic('f'),
        ...             ]
        >>> articulations = ['>',
        ...                  abjad.Articulation('-'),
        ...                  abjad.Staccato(),
        ...                  ]
        >>> leaf_dyn_maker = auxjad.LeafDynMaker()
        >>> notes = leaf_dyn_maker(pitches, durations, dynamics, articulations)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'32
            \p
            - \accent
            d'16
            \f
            - \tenuto
            e'16.
            \staccato
            f'8
            g'8
            ~
            g'32
            a'8.
        }

        .. figure:: ../_images/LeafDynMaker-79n2uz1n8j3.png
    """

    ### CLASS VARIABLES ###

    __slots__ = ('_omit_repeated_dynamics',
                 '_cyclic_dynamics',
                 '_cyclic_articulations',
                 )

    ### INITIALISER ###

    def __init__(self):
        r'Initialises self.'
        super().__init__()

    ### SPECIAL METHODS ###

    def __call__(self,
                 pitches,
                 durations,
                 dynamics=None,
                 articulations=None,
                 *,
                 omit_repeated_dynamics: bool = False,
                 cyclic_dynamics: bool = False,
                 cyclic_articulations: bool = False,
                 ) -> abjad.Selection:
        r"""Calls the leaf-maker on ``pitches``, ``durations``, ``dynamics``,
        and ``articulations``, returning an |abjad.Selection|.
        """
        if dynamics is not None:
            for dynamic in dynamics:
                if dynamic is not None:
                    if not isinstance(dynamic, (str, abjad.Dynamic)):
                        raise TypeError("dynamics must be 'str' or "
                                        "'abjad.Dynamic'")
        if articulations is not None:
            for articulation in articulations:
                if articulation is not None:
                    if not isinstance(articulation, (str,
                                                     abjad.Articulation,
                                                     abjad.Staccatissimo,
                                                     abjad.Staccato,
                                                     )):
                        raise TypeError("articulations must be 'str' or "
                                        "'abjad.Articulation'")
        if not isinstance(omit_repeated_dynamics, bool):
            raise TypeError("'omit_repeated_dynamics' must be 'bool")
        if not isinstance(cyclic_dynamics, bool):
            raise TypeError("'cyclic_dynamics' must be 'bool")
        if not isinstance(cyclic_articulations, bool):
            raise TypeError("'cyclic_articulations' must be 'bool")

        leaves = super().__call__(pitches, durations)
        dummy_container = abjad.Container(leaves)
        logical_ties = leaves.logical_ties()

        pitches_ = self._listify(pitches)
        durations_ = self._listify(durations)
        dynamics_ = self._listify(dynamics)
        articulations_ = self._listify(articulations)

        greatest_len = max(len(pitches_), len(durations_))
        self._fill_list(dynamics_,
                        greatest_len,
                        cyclic=cyclic_dynamics,
                        )
        self._fill_list(articulations_,
                        greatest_len,
                        cyclic=cyclic_articulations,
                        )

        self._add_dynamics_and_articulations(logical_ties,
                                             dynamics_,
                                             articulations_,
                                             omit_repeated_dynamics,
                                             )

        output = dummy_container[:]
        dummy_container[:] = []
        return output

    ### PRIVATE METHODS ###

    def _add_dynamics_and_articulations(self,
                                        logical_ties,
                                        dynamics_,
                                        articulations_,
                                        omit_repeated_dynamics,
                                        ):
        r'Adds dynamics and articulations to logical ties.'
        previous_dynamic = None
        for logical_tie, dynamic, articulation in zip(logical_ties,
                                                      dynamics_,
                                                      articulations_):
            if (dynamic is not None and (not omit_repeated_dynamics
                                         or dynamic != previous_dynamic)):
                abjad.attach(abjad.Dynamic(dynamic), logical_tie.head)
                previous_dynamic = dynamic
            if articulation is not None:
                if isinstance(articulation, str):
                    abjad.attach(abjad.Articulation(articulation),
                                 logical_tie.head,
                                 )
                else:
                    abjad.attach(articulation, logical_tie.head)

    @staticmethod
    def _listify(argument) -> list:
        r'Returns a :obj:`list` if argument is not a :obj:`list`.'
        if argument:
            if isinstance(argument, list):
                return argument
            else:
                return [argument]
        else:
            return []

    @staticmethod
    def _fill_list(input_list,
                   length: int,
                   cyclic: bool = False,
                   default: Any = None):
        r"""Extends a :obj:`list` to a certain length, filling it with a
        default value. If ``cyclic`` is ``True``, then it fills the :obj:`list`
        by cycling the original ``input_list``.
        """
        if not cyclic:
            while len(input_list) < length:
                input_list.append(default)
        else:
            original_length = len(input_list)
            while len(input_list) < length:
                current_length = len(input_list)
                input_list.append(input_list[current_length % original_length])
