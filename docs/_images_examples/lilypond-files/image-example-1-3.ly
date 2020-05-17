\include "lilypond-book-preamble.ly"
\language "english"

\new Staff
{
    \time 23/16
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
}