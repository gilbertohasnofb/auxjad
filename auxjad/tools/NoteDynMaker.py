import abjad


class NoteDynMaker(abjad.NoteMaker):
    r"""An extansion of NoteMaker which also takes one dynamic per note.

    ..  container:: example

        Usage is similar to NoteMaker:

        >>> pitches = [0, 2, 4, 5, 7, 9]
        >>> durations = [(1, 32), (2, 32), (3, 32), (4, 32), (5, 32), (6, 32)]
        >>> dynamics = ['pp', 'p', 'mp', 'mf', 'f', 'ff']
        >>> note_dyn_maker = NoteDynMaker()
        >>> notes = note_dyn_maker(pitches, durations, dynamics)
        >>> staff = abjad.Staff(notes)

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'32
                \pp
                d'16
                \p
                e'16.
                \mp
                f'8
                \mf
                g'8
                \f
                ~
                g'32
                a'8.
                \ff
            }


    ..  container:: example

        Can omit repeated dynamics with the keyword argument no_repeat:

        >>> pitches = [0, 2, 4, 5, 7, 9]
        >>> durations = [(1, 32), (2, 32), (3, 32), (4, 32), (5, 32), (6, 32)]
        >>> dynamics = ['pp', 'pp', 'mp', 'f', 'f', 'p']
        >>> note_dyn_maker = NoteDynMaker()
        >>> notes = note_dyn_maker(pitches,
        ...                        durations,
        ...                        dynamics,
        ...                        no_repeat=True,
        ...                        )
        >>> staff = abjad.Staff(notes)

        ..  docs::
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

        The list of dynamics can be shorter than the pitches and durations:

        >>> pitches = [0, 2, 4, 5, 7, 9]
        >>> durations = (1, 4)
        >>> dynamics = ['p', 'f', 'ff']
        >>> note_dyn_maker = NoteDynMaker()
        >>> notes = note_dyn_maker(pitches, durations, dynamics)
        >>> staff = abjad.Staff(notes)

        ..  docs::
            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                \p
                d'4
                \f
                e'4
                \ff
                f'4
                g'4
                a'4
            }

    """

    def __call__(self, pitches, durations, dynamics,
                 *, no_repeat=False) -> abjad.Selection:
        note_maker = abjad.NoteMaker()
        result = note_maker(pitches, durations)
        tied_leaves = abjad.select(result).logical_ties()
        previous_dyn = ''
        dynamics_ = dynamics[:]
        while len(dynamics_) < max(len(pitches), len(durations)):
            dynamics_.append(None)
        for item, dynamic in zip(tied_leaves, dynamics_):
            if (not no_repeat or dyn != previous_dyn) and dynamic:
                abjad.attach(abjad.Dynamic(dynamic), item[0])
                previous_dyn = dynamic
        return abjad.Selection(result)

