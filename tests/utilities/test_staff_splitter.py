import abjad

import auxjad


def test_staff_splitter_01():
    staff = abjad.Staff(r"a4 b4 c'4 d'4")
    staves = auxjad.staff_splitter(staff)
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "treble"
                r2
                c'4
                d'4
            }
            \new Staff
            {
                \clef "bass"
                a4
                b4
                r2
            }
        >>
        """
    )


def test_staff_splitter_02():
    staff = abjad.Staff(r"<g b>4 <a c'>4 <b d' f'>4 <a f c' e' g'>4")
    staves = auxjad.staff_splitter(staff)
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "treble"
                r4
                c'4
                <d' f'>4
                <c' e' g'>4
            }
            \new Staff
            {
                \clef "bass"
                <g b>4
                a4
                b4
                <f a>4
            }
        >>
        """
    )


def test_staff_splitter_03():
    staff = abjad.Staff(
        r"\time 2/4 c'2 \times 2/3 {<g b d'>2 <e' f'>4}"
        r"\times 2/3 {a2 <g b>4}"
    )
    staves = auxjad.staff_splitter(staff)
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 2/4
                \clef "treble"
                c'2
                \times 2/3
                {
                    d'2
                    <e' f'>4
                }
                R1 * 1/2
            }
            \new Staff
            {
                \time 2/4
                \clef "bass"
                R1 * 1/2
                \times 2/3
                {
                    <g b>2
                    r4
                }
                \times 2/3
                {
                    a2
                    <g b>4
                }
            }
        >>
        """
    )


def test_staff_splitter_04():
    staff = abjad.Staff(r"c'4 d'4 e'4 <d' f' a'>4")
    staves = auxjad.staff_splitter(staff, threshold="e'")
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "treble"
                r2
                e'4
                <f' a'>4
            }
            \new Staff
            {
                \clef "bass"
                c'4
                d'4
                r4
                d'4
            }
        >>
        """
    )
    staves = auxjad.staff_splitter(staff, threshold='E4')
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "treble"
                r2
                e'4
                <f' a'>4
            }
            \new Staff
            {
                \clef "bass"
                c'4
                d'4
                r4
                d'4
            }
        >>
        """
    )
    staves = auxjad.staff_splitter(staff, threshold=abjad.NamedPitch("e'"))
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "treble"
                r2
                e'4
                <f' a'>4
            }
            \new Staff
            {
                \clef "bass"
                c'4
                d'4
                r4
                d'4
            }
        >>
        """
    )
    staves = auxjad.staff_splitter(staff, threshold=abjad.NumberedPitch(4))
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "treble"
                r2
                e'4
                <f' a'>4
            }
            \new Staff
            {
                \clef "bass"
                c'4
                d'4
                r4
                d'4
            }
        >>
        """
    )
    staves = auxjad.staff_splitter(staff, threshold=4)
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "treble"
                r2
                e'4
                <f' a'>4
            }
            \new Staff
            {
                \clef "bass"
                c'4
                d'4
                r4
                d'4
            }
        >>
        """
    )


def test_staff_splitter_05():
    staff = abjad.Staff(r"c'4 d'4 e'4 <d' f' a'>4")
    staves = auxjad.staff_splitter(staff,
                                   threshold="e'",
                                   lower_clef='treble',
                                   )
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "treble"
                r2
                e'4
                <f' a'>4
            }
            \new Staff
            {
                \clef "treble"
                c'4
                d'4
                r4
                d'4
            }
        >>
        """
    )


def test_staff_splitter_06():
    staff = abjad.Staff(r"e4 f4 g4 <f a c'>4")
    staves = auxjad.staff_splitter(staff,
                                   threshold='g',
                                   upper_clef='bass',
                                   )
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "bass"
                r2
                g4
                <a c'>4
            }
            \new Staff
            {
                \clef "bass"
                e4
                f4
                r4
                f4
            }
        >>
        """
    )


def test_staff_splitter_07():
    staff = abjad.Staff(r"c'4 d'4 e'4 <d' f' a'>4")
    staves = auxjad.staff_splitter(staff,
                                   threshold="e'",
                                   add_clefs=False,
                                   )
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                r2
                e'4
                <f' a'>4
            }
            \new Staff
            {
                c'4
                d'4
                r4
                d'4
            }
        >>
        """
    )


def test_staff_splitter_08():
    staff = abjad.Staff(
        r"\time 2/4 c'2 \times 2/3 {<g b d'>2 <e' f'>4}"
        r"\times 2/3 {a2 <g b>4}"
    )
    staves = auxjad.staff_splitter(staff,
                                   use_multimeasure_rests=False,
                                   )
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 2/4
                \clef "treble"
                c'2
                \times 2/3
                {
                    d'2
                    <e' f'>4
                }
                r2
            }
            \new Staff
            {
                \time 2/4
                \clef "bass"
                r2
                \times 2/3
                {
                    <g b>2
                    r4
                }
                \times 2/3
                {
                    a2
                    <g b>4
                }
            }
        >>
        """
    )


def test_staff_splitter_09():
    staff = abjad.Staff(
        r"c'2\p <b d'>2\ff \times 2/3 {<g b d'>2\f <e' f'>1\mf}"
        r"\times 2/3 {a2\pp <g b>1\mp}"
    )
    staves = auxjad.staff_splitter(staff)
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "treble"
                c'2
                \p
                d'2
                \ff
                \times 2/3
                {
                    d'2
                    \f
                    <e' f'>1
                    \mf
                }
                R1
            }
            \new Staff
            {
                \clef "bass"
                r2
                b2
                \ff
                \times 2/3
                {
                    <g b>2
                    \f
                    r1
                }
                \times 2/3
                {
                    a2
                    \pp
                    <g b>1
                    \mp
                }
            }
        >>
        """
    )
    staff = abjad.Staff(
        r"c'2\p <b d'>2\ff \times 2/3 {<g b d'>2\f <e' f'>1\mf}"
        r"\times 2/3 {a2\pp <g b>1\mp}"
    )
    staves = auxjad.staff_splitter(staff,
                                   reposition_dynamics=False,
                                   )
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "treble"
                c'2
                \p
                d'2
                \ff
                \times 2/3
                {
                    d'2
                    \f
                    <e' f'>1
                    \mf
                }
                R1
                \mp
            }
            \new Staff
            {
                \clef "bass"
                r2
                \p
                b2
                \ff
                \times 2/3
                {
                    <g b>2
                    \f
                    r1
                    \mf
                }
                \times 2/3
                {
                    a2
                    \pp
                    <g b>1
                    \mp
                }
            }
        >>
        """
    )


def test_staff_splitter_10():
    staff = abjad.Staff(
        r"c'2\p <b d'>2\ff \times 2/3 {<g b d'>2\f <e' f'>1\mf}"
        r"\times 2/3 {a2\pp <g b>1\mp}"
    )
    staves = auxjad.staff_splitter(staff)
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "treble"
                c'2
                \p
                d'2
                \ff
                \times 2/3
                {
                    d'2
                    \f
                    <e' f'>1
                    \mf
                }
                R1
            }
            \new Staff
            {
                \clef "bass"
                r2
                b2
                \ff
                \times 2/3
                {
                    <g b>2
                    \f
                    r1
                }
                \times 2/3
                {
                    a2
                    \pp
                    <g b>1
                    \mp
                }
            }
        >>
        """
    )
    staff = abjad.Staff(
        r"c'2\p <b d'>2\ff \times 2/3 {<g b d'>2\f <e' f'>1\mf}"
        r"\times 2/3 {a2\pp <g b>1\mp}"
    )
    staves = auxjad.staff_splitter(staff,
                                   dynamics_only_on_upper_staff=True,
                                   )
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "treble"
                c'2
                \p
                d'2
                \ff
                \times 2/3
                {
                    d'2
                    \f
                    <e' f'>1
                    \mf
                }
                R1
            }
            \new Staff
            {
                \clef "bass"
                r2
                b2
                \times 2/3
                {
                    <g b>2
                    r1
                }
                \times 2/3
                {
                    a2
                    <g b>1
                }
            }
        >>
        """
    )
    staff = abjad.Staff(
        r"c'2\p <b d'>2\ff \times 2/3 {<g b d'>2\f <e' f'>1\mf}"
        r"\times 2/3 {a2\pp <g b>1\mp}"
    )
    staves = auxjad.staff_splitter(staff,
                                   dynamics_only_on_upper_staff=True,
                                   reposition_dynamics=False,
                                   )
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "treble"
                c'2
                \p
                d'2
                \ff
                \times 2/3
                {
                    d'2
                    \f
                    <e' f'>1
                    \mf
                }
                R1
                \mp
            }
            \new Staff
            {
                \clef "bass"
                r2
                b2
                \times 2/3
                {
                    <g b>2
                    r1
                }
                \times 2/3
                {
                    a2
                    <g b>1
                }
            }
        >>
        """
    )
    staff = abjad.Staff(
        r"c'2\p <b d'>2\ff \times 2/3 {<g b d'>2\f <e' f'>1\mf}"
        r"\times 2/3 {a2\pp <g b>1\mp}"
    )
    staves = auxjad.staff_splitter(staff,
                                   dynamics_only_on_upper_staff=True,
                                   reposition_dynamics=False,
                                   rewrite_meter=False,
                                   )
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "treble"
                c'2
                \p
                d'2
                \ff
                \times 2/3
                {
                    d'2
                    \f
                    <e' f'>1
                    \mf
                }
                R1
                \mp
            }
            \new Staff
            {
                \clef "bass"
                r2
                b2
                \times 2/3
                {
                    <g b>2
                    r1
                }
                \times 2/3
                {
                    a2
                    <g b>1
                }
            }
        >>
        """
    )


def test_staff_splitter_11():
    staff = abjad.Staff(r"a4 b4 c'4 d'4")
    staves = auxjad.staff_splitter(staff,
                                   rewrite_meter=False,
                                   )
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "treble"
                r4
                r4
                c'4
                d'4
            }
            \new Staff
            {
                \clef "bass"
                a4
                b4
                r4
                r4
            }
        >>
        """
    )


def test_staff_splitter_12():
    staff = abjad.Staff(
        r"\time 2/4 a8( b c' d') \times 2/3 {<g b d'>2 <e' f'>4}"
        r"\time 3/4 <d a c' g'>4--  r8 <f a bf>4."
    )
    staves = abjad.staff_splitter(staff)
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 2/4
                \clef "treble"
                r4
                c'8
                (
                d'8
                )
                \times 2/3
                {
                    d'2
                    <e' f'>4
                }
                \time 3/4
                <c' g'>4
                - \tenuto
                r2
            }
            \new Staff
            {
                \time 2/4
                \clef "bass"
                a8
                (
                b8
                )
                r4
                \times 2/3
                {
                    <g b>2
                    r4
                }
                \time 3/4
                <d a>4
                - \tenuto
                r8
                <f a bf>4.
            }
        >>
        """
    )


def test_staff_splitter_13():
    staff = abjad.Staff(r"a4 b4 c'4 d'4")
    staves = abjad.staff_splitter(staff)
    score = abjad.Score(staves)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \clef "treble"
                r2
                c'4
                d'4
            }
            \new Staff
            {
                \clef "bass"
                a4
                b4
                r2
            }
        >>
        """
    )
