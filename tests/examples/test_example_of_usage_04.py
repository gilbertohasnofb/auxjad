import random

import abjad

import auxjad


def test_example_of_usage_04():
    random.seed(64993)
    container = abjad.Container(r"c'4-- c'8.-- c'16( c'8)-. c'8-. c'8-. r8")
    pitch_list = ["c'", "cs'", "d'", "ef'", "e'"]
    randomiser = auxjad.PitchRandomiser(container,
                                        pitches=pitch_list,
                                        )
    notes = randomiser.output_n(2)
    group_1 = abjad.Staff(notes)
    randomiser.pitches = ["a", "b", "bf'", "a''", "b''"]
    notes = randomiser.output_n(2)
    group_2 = abjad.Staff(notes)
    container = abjad.Container(
        r"\time 3/4 c'4--( ~ "
        r"\times 4/5 {c'16 c'16-. c'16-. c'16-. c'16-.)} "
        r"r8 c'8->"
    )
    randomiser.contents = container
    randomiser.weights = [6, 3, 2, 1, 1]
    notes = randomiser.output_n(2)
    group_3 = abjad.Staff(notes)
    staff = abjad.Staff()
    repeater = auxjad.Repeater(group_1, repeat_type='volta')
    notes = repeater(3)
    staff.append(notes)
    repeater.contents = group_2
    notes = repeater(5)
    staff.append(notes)
    repeater.contents = group_3
    notes = repeater(4)
    staff.append(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \repeat volta 3
            {
                d'4
                - \tenuto
                c'8.
                - \tenuto
                e'16
                (
                e'8
                - \staccato
                )
                cs'8
                - \staccato
                ef'8
                - \staccato
                r8
                cs'4
                - \tenuto
                ef'8.
                - \tenuto
                e'16
                (
                ef'8
                - \staccato
                )
                e'8
                - \staccato
                d'8
                - \staccato
                r8
                \tweak RehearsalMark.self-alignment-X #RIGHT
                \tweak RehearsalMark.break-visibility #begin-of-line-invisible
                \mark \markup{\box "3×"}
            }
            \repeat volta 5
            {
                a4
                - \tenuto
                a8.
                - \tenuto
                a16
                (
                b''8
                - \staccato
                )
                b''8
                - \staccato
                a''8
                - \staccato
                r8
                b''4
                - \tenuto
                b8.
                - \tenuto
                a16
                (
                a8
                - \staccato
                )
                bf'8
                - \staccato
                a8
                - \staccato
                r8
                \tweak RehearsalMark.self-alignment-X #RIGHT
                \tweak RehearsalMark.break-visibility #begin-of-line-invisible
                \mark \markup{\box "5×"}
            }
            \repeat volta 4
            {
                \time 3/4
                b4
                - \tenuto
                (
                ~
                \times 4/5
                {
                    b16
                    b16
                    - \staccato
                    a''16
                    - \staccato
                    b16
                    - \staccato
                    a''16
                    - \staccato
                    )
                }
                r8
                b''8
                - \accent
                bf'4
                - \tenuto
                (
                ~
                \times 4/5
                {
                    bf'16
                    a16
                    - \staccato
                    b16
                    - \staccato
                    a16
                    - \staccato
                    b16
                    - \staccato
                    )
                }
                r8
                b8
                - \accent
                \tweak RehearsalMark.self-alignment-X #RIGHT
                \tweak RehearsalMark.break-visibility #begin-of-line-invisible
                \mark \markup{\box "4×"}
            }
        }
        """
    )
