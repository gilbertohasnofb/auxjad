import random

import abjad

import auxjad


def test_example_of_usage_03():
    random.seed(12432)
    pitch_selector = auxjad.TenneySelector(["c'",
                                            ("fs'", "g'"),
                                            "ef''",
                                            "a''",
                                            ("b", "bf''"),
                                            ])
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
                                 window_size=(4, 4),
                                 step_size=(1, 16),
                                 after_rest=(1, 4),
                                 after_rest_in_new_measure=True,
                                 )
    staff = abjad.Staff()
    notes = looper.output_n(4)
    staff.append(notes)
    looper.step_size = (1, 4)
    notes = looper.output_n(4)
    staff.append(notes)
    looper.window_size = (7, 8)
    looper.step_size = (1, 16)
    looper.after_rest = 0
    notes = looper.output_n(6)
    staff.append(notes)
    score = abjad.Score([staff])
    score.add_final_bar_line()
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                <b bf''>4.
                \f
                c'8
                ~
                c'4
                ef''4
                \mf
                \time 1/4
                R1 * 1/4
                \time 4/4
                <b bf''>4
                \f
                ~
                <b bf''>16
                c'8.
                ~
                c'8.
                ef''16
                \mf
                ~
                ef''8.
                c'16
                - \tenuto
                \time 1/4
                R1 * 1/4
                \time 4/4
                <b bf''>4
                \f
                c'4
                ~
                c'8
                ef''4
                \mf
                c'8
                - \tenuto
                \time 1/4
                R1 * 1/4
                \time 4/4
                <b bf''>8.
                \f
                c'16
                ~
                c'4
                ~
                c'16
                ef''8.
                \mf
                ~
                ef''16
                c'8.
                - \tenuto
                \time 1/4
                R1 * 1/4
                \time 4/4
                c'4
                \f
                ~
                c'16
                ef''8.
                \mf
                ~
                ef''16
                c'8.
                - \tenuto
                ~
                c'8.
                <fs' g'>16
                \f
                \time 1/4
                R1 * 1/4
                \time 4/4
                c'16
                ef''8.
                \mf
                ~
                ef''16
                c'8.
                - \tenuto
                ~
                c'8.
                <fs' g'>16
                \f
                ~
                <fs' g'>8.
                a''16
                \p
                \time 1/4
                R1 * 1/4
                \time 4/4
                ef''16
                \mf
                c'8.
                - \tenuto
                ~
                c'8.
                <fs' g'>16
                \f
                ~
                <fs' g'>8.
                a''16
                \p
                ~
                a''4
                \time 1/4
                R1 * 1/4
                \time 4/4
                c'8.
                \mf
                - \tenuto
                <fs' g'>16
                \f
                ~
                <fs' g'>8.
                a''16
                \p
                ~
                a''4
                ~
                a''16
                <b bf''>8.
                \time 1/4
                R1 * 1/4
                \time 7/8
                c'8
                \mf
                - \tenuto
                <fs' g'>4
                \f
                a''4.
                \p
                <b bf''>8
                c'16
                \mf
                - \tenuto
                <fs' g'>16
                \f
                ~
                <fs' g'>8.
                a''16
                \p
                ~
                a''4
                ~
                a''16
                <b bf''>8.
                <fs' g'>4
                \f
                a''4.
                \p
                <b bf''>4
                <fs' g'>8.
                \f
                a''8.
                \p
                ~
                a''8.
                <b bf''>16
                ~
                <b bf''>4
                <fs' g'>8
                \f
                a''4
                \p
                ~
                a''8
                <b bf''>4.
                <fs' g'>16
                \f
                a''16
                \p
                ~
                a''4
                ~
                a''16
                <b bf''>4..
                \bar "|."
            }
        >>
        """
    )
