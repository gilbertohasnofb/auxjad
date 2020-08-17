import random

import abjad

import auxjad


def test_example_of_usage_03():
    random.seed(12432)
    pitch_selector = auxjad.TenneySelector([0, 7, 8, 2, 3, 10])
    duration_selector = auxjad.CartographySelector([(2, 8), (3, 8), (5, 8)])
    dynamic_selector = auxjad.CartographySelector(['p', 'mp', 'mf', 'f'])
    articulation_selector = auxjad.CartographySelector([None, '-', '>'])
    pitches = [pitch_selector() for _ in range(8)]
    durations = [duration_selector() for _ in range(8)]
    dynamics = [dynamic_selector() for _ in range(8)]
    articulations = [articulation_selector() for _ in range(8)]
    leaf_dyn_maker = auxjad.LeafDynMaker()
    notes = leaf_dyn_maker(pitches, durations, dynamics, articulations)
    container = abjad.Container(notes)
    looper = auxjad.WindowLooper(container,
                                 window_size=(5, 4),
                                 step_size=(1, 4),
                                 )
    staff = abjad.Staff()
    notes = looper.output_n(6)
    staff.append(notes)
    looper.step_size = (1, 16)
    notes = looper.output_n(6)
    staff.append(notes)
    abjad.mutate(staff[:]).remove_repeated_time_signatures()
    looper.window_size = (3, 4)
    notes = looper.output_n(6)
    staff.append(notes)
    abjad.mutate(staff[:]).remove_repeated_dynamics()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 5/4
            bf'4.
            \f
            g'4.
            af'4
            \mf
            c'4
            - \tenuto
            bf'8
            \f
            g'4.
            af'4
            \mf
            c'4.
            - \tenuto
            g'8
            \f
            g'4
            af'4
            \mf
            c'4
            - \tenuto
            ~
            c'8
            g'4
            \f
            ef'8
            \p
            af'4
            \mf
            c'4.
            - \tenuto
            g'8
            \f
            ~
            g'8
            ef'4.
            \p
            c'4.
            \mf
            - \tenuto
            g'4
            \f
            ef'8
            \p
            ~
            ef'4
            bf'4
            c'8
            \mf
            - \tenuto
            g'4
            \f
            ef'4.
            \p
            bf'2
            c'16
            \mf
            - \tenuto
            g'8.
            \f
            ~
            g'16
            ef'8.
            \p
            ~
            ef'8.
            bf'16
            ~
            bf'4..
            ~
            bf'16
            g'4
            \f
            ef'4.
            \p
            bf'8
            ~
            bf'4.
            ~
            bf'8
            g'8.
            \f
            ef'16
            \p
            ~
            ef'4
            ~
            ef'16
            bf'8.
            ~
            bf'4
            ~
            bf'16
            ~
            bf'8
            af'16
            - \tenuto
            g'8
            \f
            ef'4.
            \p
            bf'4
            ~
            bf'4
            ~
            bf'8
            af'8
            - \tenuto
            g'16
            \f
            ef'8.
            \p
            ~
            ef'8.
            bf'16
            ~
            bf'4
            ~
            bf'4
            ~
            bf'16
            af'8.
            - \tenuto
            ef'4.
            bf'4.
            ~
            bf'4
            af'4
            - \tenuto
            \time 3/4
            ef'4
            ~
            ef'16
            bf'4..
            ef'4
            bf'2
            ef'8.
            bf'16
            ~
            bf'2
            ef'8
            bf'8
            ~
            bf'2
            ef'16
            bf'8.
            ~
            bf'4..
            af'16
            - \tenuto
            bf'2
            ~
            bf'8
            af'8
            - \tenuto
        }
        """)
