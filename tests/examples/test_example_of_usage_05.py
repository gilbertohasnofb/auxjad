import random

import abjad

import auxjad


def test_example_of_usage_05():
    random.seed(77124)
    container = abjad.Container([
        auxjad.ArtificialHarmonic(r"<ds' gs'>4"),
        auxjad.ArtificialHarmonic(r"<b e'>8."),
        auxjad.ArtificialHarmonic(r"<g c'>16", is_parenthesized=True),
        abjad.Rest(r"r4"),
        abjad.Chord([2, 8, 9], (1, 8)),
        auxjad.ArtificialHarmonic(r"<d' a'>8", is_parenthesized=True),
    ])
    abjad.mutate(container[:]).respell_accidentals()
    shuffler = auxjad.Shuffler(container)
    staff = abjad.Staff()
    notes = shuffler.shuffle_n(4)
    staff.append(notes)
    container = abjad.Container(shuffler.current_window)
    fader = auxjad.Fader(container, fader_type='out')
    notes = fader.output_all()
    staff.append(notes)
    abjad.mutate(staff[:]).prettify_rewrite_meter(abjad.Meter((4, 4)))
    abjad.mutate(staff[:]).remove_repeated_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >16
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                d'
                \tweak style #'harmonic
                a'
            >8
            <d' gs' a'>16
            ~
            <d' gs' a'>16
            r8.
            r16
            <
                b
                \tweak style #'harmonic
                e'
            >8.
            <
                ds'
                \tweak style #'harmonic
                gs'
            >4
            r4
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >16
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                d'
                \tweak style #'harmonic
                a'
            >8
            <d' gs' a'>16
            ~
            <d' gs' a'>16
            <
                b
                \tweak style #'harmonic
                e'
            >8.
            <
                ds'
                \tweak style #'harmonic
                gs'
            >4
            <
                ds'
                \tweak style #'harmonic
                gs'
            >4
            r4
            <
                b
                \tweak style #'harmonic
                e'
            >8.
            <d' gs' a'>16
            ~
            <d' gs' a'>16
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                d'
                \tweak style #'harmonic
                a'
            >8
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >16
            <
                ds'
                \tweak style #'harmonic
                gs'
            >4
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >16
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
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
            <d' gs' a'>8
            r4
            <
                ds'
                \tweak style #'harmonic
                gs'
            >4
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >16
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
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
            <d' gs' a'>8
            r4
            <
                ds'
                \tweak style #'harmonic
                gs'
            >4
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >16
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                d'
                \tweak style #'harmonic
                a'
            >8
            r16
            r8
            <d' gs' a'>8
            r4
            <
                ds'
                \tweak style #'harmonic
                gs'
            >4
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >16
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                d'
                \tweak style #'harmonic
                a'
            >8
            r16
            r8
            <d' gs'>8
            r4
            <
                ds'
                \tweak style #'harmonic
                gs'
            >4
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >16
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                d'
                \tweak style #'harmonic
                a'
            >8
            r16
            r8
            gs'8
            r4
            <
                ds'
                \tweak style #'harmonic
                gs'
            >4
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >16
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                d'
                \tweak style #'harmonic
                a'
            >8
            r16
            r2
            r4
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >16
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                d'
                \tweak style #'harmonic
                a'
            >8
            r16
            r2
            r4
            <
                \parenthesize
                \tweak ParenthesesItem.font-size #-4
                g
                \tweak style #'harmonic
                c'
            >16
            r8.
            r2
            R1
        }
        """)
