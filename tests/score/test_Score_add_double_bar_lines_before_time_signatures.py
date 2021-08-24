import abjad

import auxjad


def test_Score_add_double_bar_lines_before_time_signatures_01():
    staff = abjad.Staff(
        r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
    )
    score = auxjad.Score([staff])
    score.add_double_bar_lines_before_time_signatures()
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 3/4
                c'2.
                \bar "||"
                \time 4/4
                d'1
                e'1
                \bar "||"
                \time 6/4
                f'2.
                g'2.
            }
        >>
        """
    )


def test_Score_add_double_bar_lines_before_time_signatures_02():
    staff_1 = abjad.Staff(
        r"\time 3/4 c''2. \time 4/4 d''1 e''1 \time 6/4 f''2. g''2."
    )
    staff_2 = abjad.Staff(
        r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
    )
    score = auxjad.Score([staff_1, staff_2])
    score.add_double_bar_lines_before_time_signatures()
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 3/4
                c''2.
                \bar "||"
                \time 4/4
                d''1
                e''1
                \bar "||"
                \time 6/4
                f''2.
                g''2.
            }
            \new Staff
            {
                \time 3/4
                c'2.
                \bar "||"
                \time 4/4
                d'1
                e'1
                \bar "||"
                \time 6/4
                f'2.
                g'2.
            }
        >>
        """
    )
    assert abjad.lilypond(staff_1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c''2.
            \bar "||"
            \time 4/4
            d''1
            e''1
            \bar "||"
            \time 6/4
            f''2.
            g''2.
        }
        """
    )
    assert abjad.lilypond(staff_2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2.
            \bar "||"
            \time 4/4
            d'1
            e'1
            \bar "||"
            \time 6/4
            f'2.
            g'2.
        }
        """
    )


def test_Score_add_double_bar_lines_before_time_signatures_03():
    voice_1 = abjad.Voice(
        r"\time 3/4 c''2. \time 4/4 d''1 e''1 \time 6/4 f''2. g''2."
    )
    voice_2 = abjad.Voice(
        r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
    )
    staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
    abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
    abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
    score = auxjad.Score([staff])
    score.add_double_bar_lines_before_time_signatures()
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            <<
                \new Voice
                {
                    \voiceOne
                    \time 3/4
                    c''2.
                    \time 4/4
                    d''1
                    e''1
                    \time 6/4
                    f''2.
                    g''2.
                }
                \new Voice
                {
                    \voiceTwo
                    \time 3/4
                    c'2.
                    \bar "||"
                    \time 4/4
                    d'1
                    e'1
                    \bar "||"
                    \time 6/4
                    f'2.
                    g'2.
                }
            >>
        >>
        """
    )


def test_Score_add_double_bar_lines_before_time_signatures_04():
    voice_1 = abjad.Voice(
        r"\time 3/4 c''2. \time 4/4 d''1 e''1 \time 6/4 f''2. g''2."
    )
    voice_2 = abjad.Voice(
        r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
    )
    staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
    abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
    abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
    score = auxjad.Score([staff])
    score.add_double_bar_lines_before_time_signatures(to_each_voice=True)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            <<
                \new Voice
                {
                    \voiceOne
                    \time 3/4
                    c''2.
                    \bar "||"
                    \time 4/4
                    d''1
                    e''1
                    \bar "||"
                    \time 6/4
                    f''2.
                    g''2.
                }
                \new Voice
                {
                    \voiceTwo
                    \time 3/4
                    c'2.
                    \bar "||"
                    \time 4/4
                    d'1
                    e'1
                    \bar "||"
                    \time 6/4
                    f'2.
                    g'2.
                }
            >>
        >>
        """
    )


def test_Score_add_double_bar_lines_before_time_signatures_05():
    voice_1 = abjad.Voice(
        r"\time 3/4 c''2. \time 4/4 d''1 e''1 \time 6/4 f''2. g''2."
    )
    voice_2 = abjad.Voice(
        r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
    )
    staff_1 = abjad.Staff([voice_1, voice_2], simultaneous=True)
    abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
    abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
    staff_2 = abjad.Staff(
        r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
    )
    score = auxjad.Score([staff_1, staff_2])
    score.add_double_bar_lines_before_time_signatures()
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            <<
                \new Voice
                {
                    \voiceOne
                    \time 3/4
                    c''2.
                    \time 4/4
                    d''1
                    e''1
                    \time 6/4
                    f''2.
                    g''2.
                }
                \new Voice
                {
                    \voiceTwo
                    \time 3/4
                    c'2.
                    \bar "||"
                    \time 4/4
                    d'1
                    e'1
                    \bar "||"
                    \time 6/4
                    f'2.
                    g'2.
                }
            >>
            \new Staff
            {
                \time 3/4
                c'2.
                \bar "||"
                \time 4/4
                d'1
                e'1
                \bar "||"
                \time 6/4
                f'2.
                g'2.
            }
        >>
        """
    )


def test_Score_add_double_bar_lines_before_time_signatures_06():
    voice_1 = abjad.Voice(
        r"\time 3/4 c''2. \time 4/4 d''1 e''1 \time 6/4 f''2. g''2."
    )
    voice_2 = abjad.Voice(
        r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
    )
    staff_1 = abjad.Staff([voice_1, voice_2], simultaneous=True)
    abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
    abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
    staff_2 = abjad.Staff(
        r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
    )
    score = auxjad.Score([staff_1, staff_2])
    score.add_double_bar_lines_before_time_signatures(to_each_voice=True)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            <<
                \new Voice
                {
                    \voiceOne
                    \time 3/4
                    c''2.
                    \bar "||"
                    \time 4/4
                    d''1
                    e''1
                    \bar "||"
                    \time 6/4
                    f''2.
                    g''2.
                }
                \new Voice
                {
                    \voiceTwo
                    \time 3/4
                    c'2.
                    \bar "||"
                    \time 4/4
                    d'1
                    e'1
                    \bar "||"
                    \time 6/4
                    f'2.
                    g'2.
                }
            >>
            \new Staff
            {
                \time 3/4
                c'2.
                \bar "||"
                \time 4/4
                d'1
                e'1
                \bar "||"
                \time 6/4
                f'2.
                g'2.
            }
        >>
        """
    )


def test_Score_add_double_bar_lines_before_time_signatures_07():
    staff = abjad.Staff(
        r"\time 3/4 R1 * 3/4 \time 4/4 R1 * 2 \time 6/4 R1 * 6/4 \time 4/4 R1"
    )
    score = auxjad.Score([staff])
    score.add_double_bar_lines_before_time_signatures()
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 3/4
                R1 * 3/4
                \bar "||"
                \time 4/4
                R1 * 2
                \bar "||"
                \time 6/4
                R1 * 3/2
                \bar "||"
                \time 4/4
                R1
            }
        >>
        """
    )


def test_Score_add_double_bar_lines_before_time_signatures_08():
    staff = abjad.Staff(
        r"R1 "
        r"\time 3/4 c'2. "
        r"\time 4/4 d'1 "
        r"e'1 "
        r"\time 6/4 f'2. g'2. "
        r"\time 2/4 a'2"
    )
    abjad.attach(abjad.BarLine('.|:'), staff[0])
    abjad.attach(abjad.BarLine(':|.'), staff[1])
    abjad.attach(abjad.BarLine('|'), staff[3])
    abjad.attach(abjad.BarLine('!'), staff[5])
    score = auxjad.Score([staff])
    score.add_double_bar_lines_before_time_signatures()
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                R1
                \bar ".|:"
                \time 3/4
                c'2.
                \bar ":|."
                \time 4/4
                d'1
                e'1
                \bar "||"
                \time 6/4
                f'2.
                g'2.
                \bar "!"
                \time 2/4
                a'2
            }
        >>
        """
    )


def test_Score_add_double_bar_lines_before_time_signatures_09():
    assert (auxjad.Score.add_double_bar_lines_before_time_signatures
            is abjad.Score.add_double_bar_lines_before_time_signatures)
