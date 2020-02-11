import abjad


class LeafDynMaker(abjad.LeafMaker):
    r"""An extension of abjad.LeafMaker which can also take optional lists of
    dynamics and articulations.

    ..  container:: example

        Usage is similar to LeafMaker:

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

    ..  container:: example

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

    ..  container:: example

        Can omit repeated dynamics with the keyword argument ``no_repeat``:

        >>> pitches = [0, 2, 4, 5, 7, 9]
        >>> durations = [(1, 32), (2, 32), (3, 32), (4, 32), (5, 32), (6, 32)]
        >>> dynamics = ['pp', 'pp', 'mp', 'f', 'f', 'p']
        >>> leaf_dyn_maker = auxjad.LeafDynMaker()
        >>> notes = leaf_dyn_maker(pitches,
        ...                        durations,
        ...                        dynamics,
        ...                        no_repeat=True,
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

    ..  container:: example

        The lengths of both ``dynamics`` and ``articulations`` can be shorter
        than the lengths of ``pitches`` and ``durations`` (whatever is the
        greatest):

        >>> pitches = [0, 2, 4, 5, 7, 9]
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
        }

    ..  container:: example

        If the length of ``articulations`` is 1, it will apply to all elements.
        If the length of ``dynamics`` is 1, it will apply to the first element
        only:

        >>> pitches = [0, 2, 4, 5, 7, 9]
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
            -\staccato
            e'4
            -\staccato
            f'4
            -\staccato
            g'4
            -\staccato
            a'4
            -\staccato
        }

    ..  container:: example

        Similarly to abjad's native classes, it accepts many types of elements
        in its input lists:

        >>> pitches = [0,
        ...            "d'",
        ...            'E4',
        ...            abjad.Pitch(5),
        ...            abjad.Pitch("g'"),
        ...            abjad.Pitch("A4"),
        ...            ]
        >>> durations = [1/32,
        ...              (2, 32),
        ...              0.09375,
        ...              abjad.Duration(0.125),
        ...              abjad.Duration((5, 32)),
        ...              abjad.Duration(6/32),
        ...              ]
        >>> leaf_dyn_maker = auxjad.LeafDynMaker()
        >>> notes = leaf_dyn_maker(pitches, durations)
        >>> staff = abjad.Staff(notes)
        \new Staff
        {
            c'32
            d'16
            e'16.
            f'8
            g'8
            ~
            g'32
            a'8.
        }
    """

    def __call__(self,
                 pitches,
                 durations,
                 dynamics=None,
                 articulations=None,
                 *,
                 no_repeat=False
                 ) -> abjad.Selection:
        for pitch in pitches:
            if pitch is not None:
                assert isinstance(pitch,
                                  (int, float, str, tuple, abjad.Pitch),
                                  ), repr(pitch)
        for duration in durations:
            if duration is not None:
                assert isinstance(duration,
                                  (int, float, tuple, str, abjad.Duration),
                                  ), repr(duration)
        if dynamics:
            for dynamic in dynamics:
                if dynamic is not None:
                    assert isinstance(dynamic,
                                      (str, abjad.Dynamic),
                                      ), repr(dynamic)
        if articulations:
            for articulation in articulations:
                if articulation is not None:
                    assert isinstance(articulation,
                                      (str, abjad.Articulation),
                                      ), repr(articulation)
        # TODO: rewrite type checks above by raising exceptions.

        leaves = super().__call__(pitches, durations)
        logical_ties = leaves.logical_ties()
        # TODO: logical_ties() is broken: it only identifies logical ties in
        # a selection when the selection belongs to a container; but if I
        # attribute it to a container, the leaves become associated to it
        # and cannot be used elsewhere.

        dynamics_ = self._listify(dynamics)
        articulations_ = self._listify(articulations)
        greatest_len = max(len(pitches), len(durations))
        self._fill_list(dynamics_, greatest_len)
        self._fill_list(articulations_,
                        greatest_len,
                        default=self._single_element_or_none(articulations_),
                        )

        previous_dynamic = None
        for logical_tie, dynamic, articulation in zip(logical_ties,
                                                    dynamics_,
                                                    articulations_):
            if (not no_repeat or dynamic != previous_dynamic) and dynamic:
                abjad.attach(abjad.Dynamic(dynamic), logical_tie.head)
                previous_dynamic = dynamic
            if articulation:
                abjad.attach(abjad.Articulation(articulation), logical_tie.head)

        return abjad.Selection(leaves)

    @staticmethod
    def _listify(argument):
        if argument:
            if isinstance(argument, list):
                return argument
            else:
                return [argument]
        else:
            return []

    @staticmethod
    def _single_element_or_none(input_list):
        if len(input_list) == 1:
            return input_list[0]
        else:
            return None

    @staticmethod
    def _fill_list(input_list, length, default=None):
        while len(input_list) < length:
            input_list.append(default)
