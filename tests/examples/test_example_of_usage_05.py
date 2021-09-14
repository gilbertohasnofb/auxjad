import random

import abjad

import auxjad


def test_example_of_usage_05():
    random.seed(77124)
    container = abjad.Container([
        auxjad.ArtificialHarmonic(r"<ef' af'>4"),
        auxjad.ArtificialHarmonic(r"<b e'>8."),
        auxjad.ArtificialHarmonic(r"<g c'>16", is_parenthesized=True),
        abjad.Rest(r"r4"),
        abjad.Chord([-5, 8, 9], (1, 8)),
        auxjad.ArtificialHarmonic(r"<d' a'>8", is_parenthesized=True),
    ])
    abjad.mutate.respell_augmented_unisons(container[:])
    shuffler = auxjad.Shuffler(container)
    staff = abjad.Staff()
    notes = shuffler.shuffle_n(4)
    staff.append(notes)
    container = abjad.Container(shuffler.current_window)
    fader = auxjad.Fader(container, mode='out')
    notes = fader.output_all()
    staff.append(notes)
    abjad.mutate.remove_repeated_time_signatures(staff[:])
    staff.pop(-1)
    score = abjad.Score([staff])
    score.add_final_bar_line()
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    g
                    \tweak style #'harmonic
                    c'
                >16
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    d'
                    \tweak style #'harmonic
                    a'
                >8
                <g gs' a'>16
                ~
                <g gs' a'>16
                r8.
                r16
                <
                    b
                    \tweak style #'harmonic
                    e'
                >8.
                <
                    ef'
                    \tweak style #'harmonic
                    af'
                >4
                r4
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    g
                    \tweak style #'harmonic
                    c'
                >16
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    d'
                    \tweak style #'harmonic
                    a'
                >8
                <g gs' a'>16
                ~
                <g gs' a'>16
                <
                    b
                    \tweak style #'harmonic
                    e'
                >8.
                <
                    ef'
                    \tweak style #'harmonic
                    af'
                >4
                <
                    ef'
                    \tweak style #'harmonic
                    af'
                >4
                r4
                <
                    b
                    \tweak style #'harmonic
                    e'
                >8.
                <g gs' a'>16
                ~
                <g gs' a'>16
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    d'
                    \tweak style #'harmonic
                    a'
                >8
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    g
                    \tweak style #'harmonic
                    c'
                >16
                <
                    ef'
                    \tweak style #'harmonic
                    af'
                >4
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    g
                    \tweak style #'harmonic
                    c'
                >16
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    d'
                    \tweak style #'harmonic
                    a'
                >8
                <
                    b
                    \tweak style #'harmonic
                    e'
                >16
                ~
                <
                    b
                    \tweak style #'harmonic
                    e'
                >8
                <g gs' a'>8
                r4
                <
                    ef'
                    \tweak style #'harmonic
                    af'
                >4
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    g
                    \tweak style #'harmonic
                    c'
                >16
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    d'
                    \tweak style #'harmonic
                    a'
                >8
                <
                    b
                    \tweak style #'harmonic
                    e'
                >16
                ~
                <
                    b
                    \tweak style #'harmonic
                    e'
                >8
                <g gs' a'>8
                r4
                <
                    ef'
                    \tweak style #'harmonic
                    af'
                >4
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    g
                    \tweak style #'harmonic
                    c'
                >16
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    d'
                    \tweak style #'harmonic
                    a'
                >8
                r16
                r8
                <g gs' a'>8
                r4
                <
                    ef'
                    \tweak style #'harmonic
                    af'
                >4
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    g
                    \tweak style #'harmonic
                    c'
                >16
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    d'
                    \tweak style #'harmonic
                    a'
                >8
                r16
                r8
                <g gs'>8
                r4
                <
                    ef'
                    \tweak style #'harmonic
                    af'
                >4
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    g
                    \tweak style #'harmonic
                    c'
                >16
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    d'
                    \tweak style #'harmonic
                    a'
                >8
                r16
                r8
                gs'8
                r4
                <
                    ef'
                    \tweak style #'harmonic
                    af'
                >4
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    g
                    \tweak style #'harmonic
                    c'
                >16
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    d'
                    \tweak style #'harmonic
                    a'
                >8
                r16
                r2
                r4
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    g
                    \tweak style #'harmonic
                    c'
                >16
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    d'
                    \tweak style #'harmonic
                    a'
                >8
                r16
                r2
                r4
                <
                    \parenthesize
                    \tweak ParenthesesItem.font-size -4
                    g
                    \tweak style #'harmonic
                    c'
                >16
                r8.
                r2
                \bar "|."
            }
        >>
        """
    )
