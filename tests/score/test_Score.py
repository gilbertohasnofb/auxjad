import abjad

import auxjad


def test_Score_01():
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    score = auxjad.Score([staff])
    score.add_final_barline()
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
                \bar "|."
            }
        >>
        """)


def test_Score_02():
    staff_1 = abjad.Staff(r"c''1 d''1 e''1 f''1")
    staff_2 = abjad.Staff(r"c'1 d'1 e'1 f'1")
    score = auxjad.Score([staff_1, staff_2])
    score.add_final_barline()
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                c''1
                d''1
                e''1
                f''1
                \bar "|."
            }
            \new Staff
            {
                c'1
                d'1
                e'1
                f'1
                \bar "|."
            }
        >>
        """)
    assert abjad.lilypond(staff_1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c''1
            d''1
            e''1
            f''1
            \bar "|."
        }
        """)
    assert abjad.lilypond(staff_2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            d'1
            e'1
            f'1
            \bar "|."
        }
        """)


def test_Score_03():
    voice_1 = abjad.Voice(r"c''1 d''1 e''1 f''1")
    voice_2 = abjad.Voice(r"c'2 d'2 e'2 f'2 g'2 a'2 b'2 c''2")
    staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
    abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
    abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
    score = auxjad.Score([staff])
    score.add_final_barline()
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            <<
                \new Voice
                {
                    \voiceOne
                    c''1
                    d''1
                    e''1
                    f''1
                }
                \new Voice
                {
                    \voiceTwo
                    c'2
                    d'2
                    e'2
                    f'2
                    g'2
                    a'2
                    b'2
                    c''2
                    \bar "|."
                }
            >>
        >>
        """)


def test_Score_04():
    voice_1 = abjad.Voice(r"c''1 d''1 e''1 f''1")
    voice_2 = abjad.Voice(r"c'2 d'2 e'2 f'2 g'2 a'2 b'2 c''2")
    staff_1 = abjad.Staff([voice_1, voice_2], simultaneous=True)
    abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
    abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
    staff_2 = abjad.Staff(r"c'1 d'1 e'1 f'1")
    score = auxjad.Score([staff_1, staff_2])
    score.add_final_barline()
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            <<
                \new Voice
                {
                    \voiceOne
                    c''1
                    d''1
                    e''1
                    f''1
                }
                \new Voice
                {
                    \voiceTwo
                    c'2
                    d'2
                    e'2
                    f'2
                    g'2
                    a'2
                    b'2
                    c''2
                    \bar "|."
                }
            >>
            \new Staff
            {
                c'1
                d'1
                e'1
                f'1
                \bar "|."
            }
        >>
        """)


def test_Score_05():
    voice_1 = abjad.Voice(r"c''1 d''1 e''1 f''1")
    voice_2 = abjad.Voice(r"c'1 d'1 e'1 f'1")
    staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
    abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
    abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
    score = auxjad.Score([staff])
    score.add_final_barline()
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            <<
                \new Voice
                {
                    \voiceOne
                    c''1
                    d''1
                    e''1
                    f''1
                }
                \new Voice
                {
                    \voiceTwo
                    c'1
                    d'1
                    e'1
                    f'1
                    \bar "|."
                }
            >>
        >>
        """)


def test_Score_06():
    assert auxjad.Score.add_final_barline is abjad.Score.add_final_barline
