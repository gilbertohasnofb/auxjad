import auxjad
import abjad
import random


def test_complex_music_example_01():
    random.seed(87651)
    # containers of raw materials
    pitch_container = auxjad.TenneysContainer([0, 1, 2, 3, 4, 5])
    duration_container = auxjad.CartographyContainer([(1, 8), (2, 8), (3, 8)])
    dynamic_container = auxjad.CartographyContainer(['pp', 'p', 'mp'])
    articulation_container = auxjad.CartographyContainer([None, '.', '>'])
    # creating notes
    pitches = [pitch_container() for _ in range(8)]
    durations = [duration_container() for _ in range(8)]
    dynamics = [dynamic_container() for _ in range(8)]
    articulations = [articulation_container() for _ in range(8)]
    leaf_dyn_maker = auxjad.LeafDynMaker()
    notes = leaf_dyn_maker(pitches, durations, dynamics, articulations)
    container = abjad.Container(notes)
    # adding a time signature to the first note
    container_length = abjad.inspect(container).duration()
    abjad.attach(abjad.TimeSignature(container_length), container[0])
    # Using a looping window 3 times with the container created above as input
    looper = auxjad.LoopWindow(container)
    staff = abjad.Staff()
    for _ in range(3):
        music = looper()
        staff.append(music)
    # shuffling the last output container by the looping window 3 times
    container = abjad.Container(looper.current_window)
    shuffler = auxjad.LeafShuffler(container, omit_time_signatures=True)
    for _ in range(3):
        music = shuffler()
        staff.append(music)
    # continuing with the looping process 3 more times using the last shuffled
    # container
    container = abjad.Container(shuffler.current_container)
    looper = auxjad.LoopWindow(container, omit_time_signature=True)
    for _ in range(3):
        music = looper()
        staff.append(music)
    # removing repeated dynamics
    auxjad.remove_repeated_dynamics(staff)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 4/4
            f'8
            \p
            e'8
            \pp
            - \staccato
            ~
            e'8
            c'8
            \p
            ~
            c'8
            cs'4.
            f'16
            e'8.
            \pp
            - \staccato
            ~
            e'16
            c'8.
            \p
            ~
            c'16
            cs'8.
            ~
            cs'8.
            d'16
            \pp
            e'4
            - \staccato
            c'4
            \p
            cs'4.
            d'8
            \pp
            e'4
            - \staccato
            c'4
            \p
            d'8
            \pp
            cs'4.
            \p
            c'4
            d'8
            \pp
            e'8
            - \staccato
            ~
            e'8
            cs'4.
            \p
            c'4
            cs'4.
            e'8
            \pp
            - \staccato
            ~
            e'8
            d'8
            c'4
            \p
            cs'4.
            e'8
            \pp
            - \staccato
            ~
            e'8
            d'8
            c'8.
            \p
            cs'16
            ~
            cs'4
            ~
            cs'16
            e'8.
            \pp
            - \staccato
            ~
            e'16
            d'16
            ~
            d'16
            r16
            c'8
            \p
            cs'4.
            e'4
            \pp
            - \staccato
            d'8
            r8
        }
        ''')
