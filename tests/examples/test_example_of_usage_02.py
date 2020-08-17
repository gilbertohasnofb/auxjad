import random

import abjad

import auxjad


def test_example_of_usage_02():
    random.seed(18762)
    pitch_selector = auxjad.TenneySelector(["c'", "fs'", "bf'",
                                            "e''", "a''", "d'''"])
    duration_selector = auxjad.TenneySelector([(1, 16),
                                               (2, 16),
                                               (3, 16),
                                               (4, 16),
                                               (5, 16),
                                               (6, 16),
                                               ])
    pitches = []
    durations = []
    for _ in range(12):
        pitches.append(pitch_selector())
        durations.append(duration_selector())
    notes = abjad.LeafMaker()(pitches, durations)
    container = abjad.Container(notes)
    looper = auxjad.LeafLooper(container, window_size=4)
    staff = abjad.Staff(looper.output_n(7))
    looper.window_size = 2
    staff.append(looper.output_n(4))
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 11/16
            a''16
            d'''8
            ~
            d'''8.
            c'16
            ~
            c'8.
            e''16
            \time 7/8
            d'''4
            ~
            d'''16
            c'16
            ~
            c'8.
            e''16
            bf'4
            \time 3/4
            c'4
            e''16
            bf'8.
            ~
            bf'16
            fs'8.
            \time 5/8
            e''16
            bf'16
            ~
            bf'8.
            fs'16
            ~
            fs'8
            a''8
            \time 7/8
            bf'4
            fs'8
            ~
            fs'16
            a''8
            d'''16
            ~
            d'''4
            \time 11/16
            fs'8.
            a''8
            d'''4
            ~
            d'''16
            c'16
            \time 3/4
            a''8
            d'''8
            ~
            d'''8.
            c'16
            d'''4
            \time 3/8
            d'''4
            ~
            d'''16
            c'16
            \time 5/16
            c'16
            d'''4
            \time 5/8
            d'''4
            a''4.
            \time 11/16
            a''4.
            e''16
            ~
            e''4
        }
        """)
