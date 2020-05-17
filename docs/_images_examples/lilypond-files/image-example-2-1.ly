\include "lilypond-book-preamble.ly"
\language "english"

\new Staff
    {
        \time 13/4
        c'2
        \mp
        - \tenuto
        ~
        c'8
        af'4.
        \mp
        bf'4.
        \mf
        - \tenuto
        c'4.
        \mp
        d'4.
        \mf
        - \accent
        ef'4
        \p
        - \accent
        af'2
        \mp
        ~
        af'8
        c'4
        \mp
        - \accent
    }