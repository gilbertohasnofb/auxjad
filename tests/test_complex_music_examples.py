import auxjad
import abjad
import random


def test_complex_music_example_02():
    random.seed(87435)
    container = abjad.Staff([
        auxjad.ArtificialHarmonic("<ds' gs'>4"),
        auxjad.ArtificialHarmonic("<b ds'>8."),
        auxjad.ArtificialHarmonic("<g c'>2.", is_parenthesized=True),
        abjad.Rest("r4"),
        abjad.Chord([0, 1, 7], (1, 8)),
        auxjad.ArtificialHarmonic("<d' a'>2.", is_parenthesized=True),
    ])
    # adding a time signature to the first note
    container_length = abjad.inspect(container).duration()
    abjad.attach(abjad.TimeSignature(container_length), container[0])
    # respelling augmented unisons
    auxjad.respell_container(container)
    assert format(container) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 37/16
            <
                ds'
                \tweak style #'harmonic
                gs'
            >4
            <
                b
                \tweak style #'harmonic
                ds'
            >8.
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >2.
            r4
            <c' df' g'>8
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                d'
                \tweak style #'harmonic
                a'
            >2.
        }
        """)
    # Using a looping window by elements 3 times
    looper = auxjad.LoopByNotes(container, window_size=4)
    staff = abjad.Staff()
    for _ in range(3):
        music = looper()
        staff.append(music)
    # shuffling the last output container by the looping window 3 times
    container = abjad.Container(looper.current_window)
    shuffler = auxjad.Shuffler(container, omit_time_signatures=True)
    for _ in range(3):
        music = shuffler()
        staff.append(music)
    # adding initial dynamics
    abjad.attach(abjad.Dynamic('ppp'), staff[0])
    assert format(container) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 23/16
            <
                ds'
                \tweak style #'harmonic
                gs'
            >4
            \ppp
            <
                b
                \tweak style #'harmonic
                ds'
            >8.
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >2.
            r4
            \time 21/16
            <
                b
                \tweak style #'harmonic
                ds'
            >8.
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >2.
            r4
            <c' df' g'>8
            \time 15/8
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >2.
            r4
            <c' df' g'>8
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                d'
                \tweak style #'harmonic
                a'
            >2.
            r4
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                d'
                \tweak style #'harmonic
                a'
            >4.
            ~
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                d'
                \tweak style #'harmonic
                a'
            >4.
            <c' df' g'>8
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >2.
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                d'
                \tweak style #'harmonic
                a'
            >2.
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >2
            ~
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >4
            r8
            r8
            <c' df' g'>8
            <c' df' g'>8
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >2
            ~
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >4
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                d'
                \tweak style #'harmonic
                a'
            >4.
            ~
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                d'
                \tweak style #'harmonic
                a'
            >4.
            r4
        }
        """)


def test_complex_music_example_02():
    random.seed(1242)
    # selectors of raw materials
    pitch_selector = auxjad.TenneySelector([0, 7, 8, 2, 3, 10])
    duration_selector = auxjad.CartographySelector([(2, 8), (3, 8), (5, 8)])
    dynamic_selector = auxjad.CartographySelector(['p', 'mp', 'mf', 'f'])
    articulation_selector = auxjad.CartographySelector([None, '-', '>'])
    # creating notes
    pitches = [pitch_selector() for _ in range(8)]
    durations = [duration_selector() for _ in range(8)]
    dynamics = [dynamic_selector() for _ in range(8)]
    articulations = [articulation_selector() for _ in range(8)]
    leaf_dyn_maker = auxjad.LeafDynMaker()
    notes = leaf_dyn_maker(pitches, durations, dynamics, articulations)
    container = abjad.Staff(notes)
    # adding a time signature to the first note
    container_length = abjad.inspect(container).duration()
    abjad.attach(abjad.TimeSignature(container_length), container[0])
    assert format(container) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 13/4
            c'2
            \mp
            - \tenuto
            ~
            c'8
            af'4.
            \mp
            bf'4.
            \mf
            - \tenuto
            c'4.
            \mp
            d'4.
            \mf
            - \accent
            ef'4
            \p
            - \accent
            af'2
            \mp
            ~
            af'8
            c'4
            \mp
            - \accent
        }
        """)
    # Using a looping window 3 times with the container created above as input
    looper = auxjad.LoopByWindow(container)
    staff = abjad.Staff()
    for _ in range(3):
        music = looper()
        staff.append(music)
    # shuffling the last output container by the looping window 3 times
    container = abjad.Container(looper.current_window)
    shuffler = auxjad.Shuffler(container, omit_time_signatures=True)
    for _ in range(3):
        music = shuffler()
        staff.append(music)
    # continuing with the looping process 3 more times using the last shuffled
    # container
    container = abjad.Container(shuffler.current_window)
    looper = auxjad.LoopByWindow(container, window_size=(3, 4))
    for _ in range(3):
        music = looper()
        staff.append(music)
    # removing repeated dynamics
    auxjad.remove_repeated_dynamics(staff)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'2
            \mp
            - \tenuto
            ~
            c'8
            af'4.
            c'2
            - \tenuto
            ~
            c'16
            af'8.
            ~
            af'8.
            bf'16
            \mf
            - \tenuto
            c'2
            \mp
            - \tenuto
            af'4.
            bf'8
            \mf
            - \tenuto
            bf'8
            - \tenuto
            c'8
            \mp
            - \tenuto
            ~
            c'4.
            af'4.
            c'2
            - \tenuto
            bf'8
            \mf
            - \tenuto
            af'4.
            \mp
            bf'8
            \mf
            - \tenuto
            c'8
            \mp
            - \tenuto
            ~
            c'4.
            af'4.
            \time 3/4
            bf'8
            \mf
            - \tenuto
            c'8
            \mp
            - \tenuto
            ~
            c'4.
            af'8
            bf'16
            \mf
            - \tenuto
            c'8.
            \mp
            - \tenuto
            ~
            c'4
            ~
            c'16
            af'8.
            c'2
            - \tenuto
            af'4
        }
        """)
