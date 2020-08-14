import abjad

import auxjad


def test_LeafDynMaker_01():
    pitches = [0, 2, 4, 5, 7, 9]
    durations = [(1, 32), (2, 32), (3, 32), (4, 32), (5, 32), (6, 32)]
    dynamics = ['pp', 'p', 'mp', 'mf', 'f', 'ff']
    articulations = ['.', '>', '-', '_', '^', '+']
    leaf_dyn_maker = auxjad.LeafDynMaker()
    notes = leaf_dyn_maker(pitches, durations, dynamics, articulations)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'32
            \pp
            - \staccato
            d'16
            \p
            - \accent
            e'16.
            \mp
            - \tenuto
            f'8
            \mf
            - \portato
            g'8
            \f
            - \marcato
            ~
            g'32
            a'8.
            \ff
            - \stopped
        }
        """)


def test_LeafDynMaker_02():
    pitches = [5, None, (0, 2, 7)]
    durations = [(1, 4), (1, 8), (1, 16)]
    dynamics = ['p', None, 'f']
    articulations = ['staccato', None, 'tenuto']
    leaf_dyn_maker = auxjad.LeafDynMaker()
    notes = leaf_dyn_maker(pitches, durations, dynamics, articulations)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            f'4
            \p
            - \staccato
            r8
            <c' d' g'>16
            \f
            - \tenuto
        }
        """)


def test_LeafDynMaker_03():
    pitches = [0, 2, 4, 5, 7, 9]
    durations = [(1, 32), (2, 32), (3, 32), (4, 32), (5, 32), (6, 32)]
    dynamics = ['pp', 'pp', 'mp', 'f', 'f', 'p']
    leaf_dyn_maker = auxjad.LeafDynMaker()
    notes = leaf_dyn_maker(pitches,
                           durations,
                           dynamics,
                           omit_repeated_dynamics=True,
                           )
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_LeafDynMaker_04():
    pitches = [0, 2, 4, 5, 7, 9, 11, 12]
    durations = (1, 4)
    dynamics = ['p', 'f', 'ff']
    articulations = ['.', '>']
    leaf_dyn_maker = auxjad.LeafDynMaker()
    notes = leaf_dyn_maker(pitches, durations, dynamics, articulations)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
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
            f'4
            g'4
            a'4
            b'4
            c''4
        }
        """)


def test_LeafDynMaker_05():
    pitches = [0, 2, 4, 5, 7, 9, 11, 12]
    durations = (1, 4)
    dynamics = ['p', 'f', 'ff']
    articulations = ['.', '>']
    leaf_dyn_maker = auxjad.LeafDynMaker()
    notes = leaf_dyn_maker(pitches,
                           durations,
                           dynamics,
                           articulations,
                           cyclic_dynamics=True,
                           cyclic_articulations=True,
                           )
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_LeafDynMaker_06():
    pitches = [0, 2, 4, 5, 7, 9, 11, 12]
    durations = (1, 4)
    dynamics = 'p'
    articulations = '.'
    leaf_dyn_maker = auxjad.LeafDynMaker()
    notes = leaf_dyn_maker(pitches, durations, dynamics, articulations)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \p
            - \staccato
            d'4
            e'4
            f'4
            g'4
            a'4
            b'4
            c''4
        }
        """)


def test_LeafDynMaker_07():
    pitches = [0, 2, 4, 5, 7, 9, 11, 12]
    durations = (1, 4)
    dynamics = 'p'
    articulations = '.'
    leaf_dyn_maker = auxjad.LeafDynMaker()
    notes = leaf_dyn_maker(pitches,
                           durations,
                           dynamics,
                           articulations,
                           cyclic_articulations=True,
                           )
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \p
            - \staccato
            d'4
            - \staccato
            e'4
            - \staccato
            f'4
            - \staccato
            g'4
            - \staccato
            a'4
            - \staccato
            b'4
            - \staccato
            c''4
            - \staccato
        }
        """)


def test_LeafDynMaker_08():
    pitches = [0,
               "d'",
               'E4',
               abjad.NumberedPitch(5),
               abjad.NamedPitch("g'"),
               abjad.NamedPitch('A4'),
               ]
    durations = [(1, 32),
                 '2/32',
                 abjad.Duration('3/32'),
                 abjad.Duration(0.125),
                 abjad.Duration(5, 32),
                 abjad.Duration(6 / 32),
                 ]
    dynamics = ['p',
                abjad.Dynamic('f'),
                ]
    articulations = ['>',
                     abjad.Articulation('-'),
                     abjad.Staccato(),
                     ]
    leaf_dyn_maker = auxjad.LeafDynMaker()
    notes = leaf_dyn_maker(pitches, durations, dynamics, articulations)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_LeafDynMaker_09():
    leaf_dyn_maker = auxjad.LeafDynMaker()
    note = leaf_dyn_maker(0, (1, 4), 'p', '-')
    staff = abjad.Staff([note])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \p
            - \tenuto
        }
        """)
