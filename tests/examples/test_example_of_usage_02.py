import random

import abjad

import auxjad


def test_example_of_usage_02():
    random.seed(18762)
    pitch_selector = auxjad.TenneySelector(["d'",
                                            ("c'", "d'", "e'"),
                                            ("b", "d'", "g'"),
                                            ("bf", "d'", "a'"),
                                            ("a", "d'", "b'"),
                                            ])
    duration_selector = auxjad.TenneySelector([(1, 16),
                                               (2, 16),
                                               (3, 16),
                                               (4, 16),
                                               ])
    pitches = []
    durations = []
    for _ in range(14):
        pitches.append(pitch_selector())
        durations.append(duration_selector())
    notes = abjad.LeafMaker()(pitches, durations)
    container = abjad.Container(notes)
    looper = auxjad.LeafLooper(container,
                               window_size=4,
                               after_rest=(1, 2),
                               after_rest_in_new_measure=True,
                               )
    staff = abjad.Staff(looper.output_n(7))
    looper.window_size = 3
    looper.after_rest = (3, 16)
    staff.append(looper.output_n(5))
    staff.pop(-1)
    score = abjad.Score([staff])
    score.add_final_bar_line()
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 9/16
                <bf d' a'>16
                <a d' b'>8
                ~
                <a d' b'>16
                d'8
                ~
                d'8
                <b d' g'>16
                \time 2/4
                R1 * 1/2
                \time 5/8
                <a d' b'>8.
                d'8.
                ~
                d'16
                <b d' g'>16
                <bf d' a'>8
                \time 2/4
                R1 * 1/2
                \time 5/8
                d'4
                <b d' g'>16
                <bf d' a'>16
                ~
                <bf d' a'>16
                <c' d' e'>8.
                \time 2/4
                R1 * 1/2
                \time 7/16
                <b d' g'>16
                <bf d' a'>8
                <c' d' e'>8.
                <a d' b'>16
                \time 2/4
                R1 * 1/2
                \time 5/8
                <bf d' a'>8
                <c' d' e'>8.
                <a d' b'>16
                <bf d' a'>4
                \time 2/4
                R1 * 1/2
                \time 9/16
                <c' d' e'>8.
                <a d' b'>16
                <bf d' a'>8
                ~
                <bf d' a'>8
                d'16
                \time 2/4
                R1 * 1/2
                <a d' b'>16
                <bf d' a'>8.
                ~
                <bf d' a'>16
                d'16
                <a d' b'>8
                R1 * 1/2
                \time 7/16
                <bf d' a'>4
                d'16
                <a d' b'>8
                \time 3/16
                R1 * 3/16
                \time 7/16
                d'16
                <a d' b'>8
                <bf d' a'>4
                \time 3/16
                R1 * 3/16
                \time 9/16
                <a d' b'>8
                <bf d' a'>4
                <b d' g'>8.
                \time 3/16
                R1 * 3/16
                \time 2/4
                <bf d' a'>4
                <b d' g'>8.
                <c' d' e'>16
                \time 3/16
                R1 * 3/16
                \time 3/8
                <b d' g'>8.
                <c' d' e'>16
                <bf d' a'>8
                \bar "|."
            }
        >>
        """
    )
