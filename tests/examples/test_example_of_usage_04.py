import random

import abjad

import auxjad


def test_example_of_usage_04():
    random.seed(98611)
    container = abjad.Container(r"c'4 ~ c'16 r8 c'16 c'4 c'16 r8.")
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches=[0, 1, 2, 3, 4, 5, 6],
                                        )
    staff = abjad.Staff()
    notes = randomiser.output_n(3)
    staff.append(notes)
    randomiser.pitches = [13, 14, 16, 17, 21]
    notes = randomiser.output_n(3)
    staff.append(notes)
    randomiser.weights = [6, 3, 2, 1, 1]
    notes = randomiser.output_n(3)
    staff.append(notes)
    hocketer = auxjad.Hocketer(staff,
                               n_voices=3,
                               )
    music = hocketer()
    score = abjad.Score(music)
    assert format(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                f'4
                ~
                f'16
                r4..
                cs'16
                r8.
                R1
                R1
                f''4
                ~
                f''16
                r16
                r16
                f''16
                r2
                R1
                a''4
                ~
                a''16
                r8.
                e''4
                r4
                r2.
                d''16
                r8.
                r4..
                cs''16
                r2
                r4..
                cs''16
                r4
                cs''16
                r8.
            }
            \new Staff
            {
                r2
                d'4
                r4
                fs'4
                ~
                fs'16
                r8.
                r2
                c'4
                ~
                c'16
                r16
                r16
                ef'16
                r4
                cs'16
                r8.
                r2.
                f''16
                r8.
                f''4
                ~
                f''16
                r16
                r16
                a''16
                e''4
                f''16
                r8.
                r4..
                cs''16
                r2
                r4..
                d''16
                r2
                d''4
                ~
                d''16
                r4..
                a''16
                r8.
                R1
            }
            \new Staff
            {
                r4..
                fs'16
                r2
                r4..
                cs'16
                ef'4
                e'16
                r8.
                r2
                c'4
                r4
                r2
                cs''4
                r4
                R1
                r2.
                f''16
                r8.
                cs''4
                ~
                cs''16
                r8.
                d''4
                r4
                r2
                d''4
                r4
                d''4
                ~
                d''16
                r8.
                d''4
                r4
            }
        >>
        """)
