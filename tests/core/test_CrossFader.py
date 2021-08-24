import random

import abjad

import auxjad


def test_CrossFader_01():
    random.seed(17737)
    fade_out_container = abjad.Staff(r"fs'4 g'2 bf'4")
    fade_in_container = abjad.Staff(r"\times 4/5 {cs''4 d''1}")
    fader = auxjad.CrossFader(fade_out_container, fade_in_container)
    assert abjad.lilypond(fader) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            fs'4
            g'2
            bf'4
        }
        \new Staff
        {
            \times 4/5
            {
                \time 4/4
                cs''4
                d''1
            }
        }
        """
    )
    selection_a, selection_b = fader()
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                fs'4
                g'2
                bf'4
            }
            \new Staff
            {
                \time 4/4
                R1
            }
        >>
        """
    )
    selection_a, selection_b = fader()
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                fs'4
                g'2
                bf'4
            }
            \new Staff
            {
                \times 4/5
                {
                    \time 4/4
                    r4
                    d''1
                }
            }
        >>
        """
    )
    selection_a, selection_b = fader.current_window
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                fs'4
                g'2
                bf'4
            }
            \new Staff
            {
                \times 4/5
                {
                    \time 4/4
                    r4
                    d''1
                }
            }
        >>
        """
    )


def test_CrossFader_02():
    fade_out_container = abjad.Container(r"c'4 d'4 ~ d'4 r4")
    fade_in_container = abjad.Container(r"r2 c''2")
    fader = auxjad.CrossFader(fade_out_container, fade_in_container)
    assert len(fader) == 3
    fade_out_container = abjad.Container(r"fs'4 g'2 bf'4")
    fade_in_container = abjad.Container(r"\times 4/5 {cs''4 d''1}")
    fader = auxjad.CrossFader(fade_out_container, fade_in_container)
    assert len(fader) == 5
    fade_out_container = abjad.Container(r"c'4 d'4 ~ d'4 r4")
    fade_in_container = abjad.Container(r"r2 <c'' e'' g''>2")
    fader = auxjad.CrossFader(fade_out_container, fade_in_container)
    assert len(fader) == 5


def test_CrossFader_03():
    random.seed(44811)
    fade_out_container = abjad.Container(r"fs'4 g'2 bf'4")
    fade_in_container = abjad.Container(r"\times 4/5 {cs''4 d'1}")
    fader = auxjad.CrossFader(fade_out_container, fade_in_container)
    staff_a = abjad.Staff()
    staff_b = abjad.Staff()
    score = abjad.Score([staff_a, staff_b])
    for _ in range(3):
        selection_a, selection_b = fader()
        staff_a.extend(selection_a)
        staff_b.extend(selection_b)
    fader.reset()
    selection_a, selection_b = fader()
    staff_a.extend(selection_a)
    staff_b.extend(selection_b)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                fs'4
                g'2
                bf'4
                \time 4/4
                fs'4
                g'2
                bf'4
                \time 4/4
                fs'4
                r2
                bf'4
                \time 4/4
                fs'4
                g'2
                bf'4
            }
            \new Staff
            {
                \time 4/4
                R1
                \times 4/5
                {
                    \time 4/4
                    cs''4
                    r1
                }
                \times 4/5
                {
                    \time 4/4
                    cs''4
                    r1
                }
                \time 4/4
                R1
            }
        >>
        """
    )


def test_CrossFader_04():
    random.seed(44811)
    fade_out_container = abjad.Container(r"fs'4 g'2 bf'4")
    fade_in_container = abjad.Container(r"\times 4/5 {cs''4 d'1}")
    fader = auxjad.CrossFader(fade_out_container, fade_in_container)
    selection_a, selection_b = fader.output_all()
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                fs'4
                g'2
                bf'4
                fs'4
                g'2
                bf'4
                fs'4
                r2
                bf'4
                fs'4
                r2
                bf'4
                r2.
                bf'4
                R1
            }
            \new Staff
            {
                \time 4/4
                R1
                \times 4/5
                {
                    cs''4
                    r1
                }
                \times 4/5
                {
                    cs''4
                    r1
                }
                \times 4/5
                {
                    cs''4
                    d'1
                }
                \times 4/5
                {
                    cs''4
                    d'1
                }
                \times 4/5
                {
                    cs''4
                    d'1
                }
            }
        >>
        """
    )


def test_CrossFader_05():
    random.seed(10711)
    fade_out_container = abjad.Container(r"e'8 fs'4. r2")
    fade_in_container = abjad.Container(r"c''2 ~ c''8 d''4.")
    fader = auxjad.CrossFader(fade_out_container, fade_in_container)
    selection_a, selection_b = fader.output_n(3)
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                e'8
                fs'4.
                r2
                e'8
                fs'4.
                r2
                e'8
                r2..
            }
            \new Staff
            {
                \time 4/4
                R1
                c''2
                ~
                c''8
                r4.
                c''2
                ~
                c''8
                r4.
            }
        >>
        """
    )


def test_CrossFader_06():
    random.seed(10711)
    fade_out_container = abjad.Container(r"e'8 fs'4. r2")
    fade_in_container = abjad.Container(r"c''2 ~ c''8 d''4.")
    fader = auxjad.CrossFader(fade_out_container, fade_in_container)
    staff_a = abjad.Staff()
    staff_b = abjad.Staff()
    score = abjad.Score([staff_a, staff_b])
    for selection_a, selection_b in fader:
        staff_a.extend(selection_a)
        staff_b.extend(selection_b)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                e'8
                fs'4.
                r2
                \time 4/4
                e'8
                fs'4.
                r2
                \time 4/4
                e'8
                r2..
                \time 4/4
                e'8
                r2..
                \time 4/4
                R1
            }
            \new Staff
            {
                \time 4/4
                R1
                \time 4/4
                c''2
                ~
                c''8
                r4.
                \time 4/4
                c''2
                ~
                c''8
                r4.
                \time 4/4
                c''2
                ~
                c''8
                d''4.
                \time 4/4
                c''2
                ~
                c''8
                d''4.
            }
        >>
        """
    )


def test_CrossFader_07():
    random.seed(87114)
    fade_out_container = abjad.Container(r"e'8 fs'4. r2")
    fade_in_container = abjad.Container(r"c''2 ~ c''8 d''4.")
    fader = auxjad.CrossFader(fade_out_container, fade_in_container)
    staff_a = abjad.Staff()
    staff_b = abjad.Staff()
    score = abjad.Score([staff_a, staff_b])
    for _ in range(3):
        selection_a, selection_b = next(fader)
        staff_a.extend(selection_a)
        staff_b.extend(selection_b)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                e'8
                fs'4.
                r2
                \time 4/4
                e'8
                r2..
                \time 4/4
                e'8
                r2..
            }
            \new Staff
            {
                \time 4/4
                R1
                \time 4/4
                R1
                \time 4/4
                c''2
                ~
                c''8
                r4.
            }
        >>
        """
    )


def test_CrossFader_08():
    random.seed(62190)
    fade_out_container = abjad.Container(r"\time 3/4 r4 c'4 d'4")
    fade_in_container = abjad.Container(r"\time 3/4 a''4 g''2")
    fader = auxjad.CrossFader(fade_out_container, fade_in_container)
    selection_a, selection_b = fader.output_all()
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 3/4
                r4
                c'4
                d'4
                r2
                d'4
                r2
                d'4
                R1 * 3/4
                R1 * 3/4
            }
            \new Staff
            {
                \time 3/4
                R1 * 3/4
                R1 * 3/4
                a''4
                r2
                a''4
                r2
                a''4
                g''2
            }
        >>
        """
    )
    random.seed(62190)
    fader = auxjad.CrossFader(fade_out_container,
                              fade_in_container,
                              fade_out_last=True,
                              )
    selection_a, selection_b = fader.output_all()
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 3/4
                r4
                c'4
                d'4
                r2
                d'4
                r2
                d'4
                r2
                d'4
                R1 * 3/4
            }
            \new Staff
            {
                \time 3/4
                R1 * 3/4
                R1 * 3/4
                a''4
                r2
                a''4
                g''2
                a''4
                g''2
            }
        >>
        """
    )
    random.seed(62190)
    fader = auxjad.CrossFader(fade_out_container,
                              fade_in_container,
                              fade_in_first=True,
                              fade_out_last=True,
                              )
    selection_a, selection_b = fader.output_all()
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 3/4
                r4
                c'4
                d'4
                r4
                c'4
                d'4
                r4
                c'4
                d'4
                r2
                d'4
                R1 * 3/4
            }
            \new Staff
            {
                \time 3/4
                R1 * 3/4
                a''4
                r2
                a''4
                g''2
                a''4
                g''2
                a''4
                g''2
            }
        >>
        """
    )


def test_CrossFader_09():
    random.seed(50137)
    fade_out_container = abjad.Container(r"e'2 c'2")
    fade_in_container = abjad.Container(
        r"c''8 d''8 e''8 f''8 g''8 a''8 b''8 c'''8"
    )
    fader = auxjad.CrossFader(fade_out_container, fade_in_container)
    selection_a, selection_b = fader.output_all()
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                e'2
                c'2
                e'2
                c'2
                r2
                c'2
                r2
                c'2
                r2
                c'2
                R1
                R1
                R1
                R1
                R1
                R1
            }
            \new Staff
            {
                \time 4/4
                R1
                r4.
                f''8
                r2
                r4.
                f''8
                r2
                r4.
                f''8
                r8
                a''8
                r4
                r4.
                f''8
                r8
                a''8
                b''8
                r8
                r4.
                f''8
                r8
                a''8
                b''8
                r8
                r4.
                f''8
                r8
                a''8
                b''8
                c'''8
                r4
                e''8
                f''8
                r8
                a''8
                b''8
                c'''8
                r8
                d''8
                e''8
                f''8
                r8
                a''8
                b''8
                c'''8
                c''8
                d''8
                e''8
                f''8
                r8
                a''8
                b''8
                c'''8
                c''8
                d''8
                e''8
                f''8
                g''8
                a''8
                b''8
                c'''8
            }
        >>
        """
    )
    random.seed(50137)
    fader = auxjad.CrossFader(fade_out_container,
                              fade_in_container,
                              weighted_duration=True,
                              )
    selection_a, selection_b = fader.output_all()
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                e'2
                c'2
                e'2
                c'2
                r2
                c'2
                r2
                c'2
                r2
                c'2
                r2
                c'2
                r2
                c'2
                r2
                c'2
                r2
                c'2
                r2
                c'2
                R1
            }
            \new Staff
            {
                \time 4/4
                R1
                r4.
                f''8
                r2
                r4.
                f''8
                r2
                r4.
                f''8
                r8
                a''8
                r4
                r4.
                f''8
                r8
                a''8
                b''8
                r8
                r4
                e''8
                f''8
                r8
                a''8
                b''8
                r8
                r4
                e''8
                f''8
                g''8
                a''8
                b''8
                r8
                c''8
                r8
                e''8
                f''8
                g''8
                a''8
                b''8
                r8
                c''8
                r8
                e''8
                f''8
                g''8
                a''8
                b''8
                c'''8
                c''8
                d''8
                e''8
                f''8
                g''8
                a''8
                b''8
                c'''8
                c''8
                d''8
                e''8
                f''8
                g''8
                a''8
                b''8
                c'''8
            }
        >>
        """
    )


def test_CrossFader_10():
    fade_out_container = abjad.Container(r"\time 3/4 e2 \times 2/3 {fs8 gs4}")
    fade_in_container = abjad.Container(r"\time 3/4 c'8 d' e' f' g' a'")
    fader = auxjad.CrossFader(fade_out_container, fade_in_container)
    fader.fade_out_contents = abjad.Container(r"\time 3/4 a4. bf4.")
    assert abjad.lilypond(fader) == abjad.String.normalize(
        r"""
        {
            %%% \time 3/4 %%%
            a4.
            bf4.
        }
        {
            %%% \time 3/4 %%%
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }
        """
    )


def test_CrossFader_11():
    random.seed(41379)
    fade_out_container = abjad.Container(r"a'4 bf'2 r4")
    fade_in_container = abjad.Container(r"c''2 d''2")
    fader = auxjad.CrossFader(fade_out_container,
                              fade_in_container,
                              initial_repetitions=2,
                              final_repetitions=3,
                              )
    selection_a, selection_b = fader.output_all()
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                a'4
                bf'2
                r4
                a'4
                bf'2
                r4
                r4
                bf'2
                r4
                r4
                bf'2
                r4
                r4
                bf'2
                r4
                R1
                R1
                R1
            }
            \new Staff
            {
                \time 4/4
                R1
                R1
                R1
                r2
                d''2
                c''2
                d''2
                c''2
                d''2
                c''2
                d''2
                c''2
                d''2
            }
        >>
        """
    )


def test_CrossFader_12():
    random.seed(91766)
    fade_out_container = abjad.Container(r"a'4 bf'2 r4")
    fade_in_container = abjad.Container(r"c''2 d''2")
    fader = auxjad.CrossFader(fade_out_container,
                              fade_in_container,
                              repetition_chance=0.8,
                              )
    selection_a, selection_b = fader.output_n(4)
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                a'4
                bf'2
                r4
                a'4
                bf'2
                r4
                a'4
                bf'2
                r4
                a'4
                bf'2
                r4
            }
            \new Staff
            {
                \time 4/4
                R1
                r2
                d''2
                r2
                d''2
                r2
                d''2
            }
        >>
        """
    )


def test_CrossFader_13():
    random.seed(81943)
    fade_out_container = abjad.Container(
        r"\time 3/4 a'4 bf'2 ~ \time 2/4 bf'4 f'4"
    )
    fade_in_container = abjad.Container(
        r"\time 3/4 r16 cs''4.. e''4 \time 2/4 d''2"
    )
    fader = auxjad.CrossFader(fade_out_container, fade_in_container)
    selection_a, selection_b = fader.output_n(3)
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 3/4
                a'4
                bf'2
                ~
                \time 2/4
                bf'4
                f'4
                \time 3/4
                a'4
                bf'2
                ~
                \time 2/4
                bf'4
                f'4
                \time 3/4
                a'4
                bf'2
                ~
                \time 2/4
                bf'4
                r4
            }
            \new Staff
            {
                \time 3/4
                R1 * 3/4
                \time 2/4
                R1 * 1/2
                \time 3/4
                r16
                cs''4..
                r4
                \time 2/4
                R1 * 1/2
                \time 3/4
                r16
                cs''4..
                r4
                \time 2/4
                R1 * 1/2
            }
        >>
        """
    )


def test_CrossFader_14():
    random.seed(75991)
    fade_out_container = abjad.Container(r"fs'4 g'2 bf'4")
    fade_in_container = abjad.Container(r"\times 4/5 {cs''4 d''1}")
    fader = auxjad.CrossFader(fade_out_container,
                              fade_in_container,
                              omit_time_signatures=True,
                              )
    selection_a, selection_b = fader.output_n(3)
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                fs'4
                g'2
                bf'4
                fs'4
                g'2
                r4
                fs'4
                g'2
                r4
            }
            \new Staff
            {
                R1
                R1
                \times 4/5
                {
                    cs''4
                    r1
                }
            }
        >>
        """
    )


def test_CrossFader_15():
    random.seed(33163)
    fade_out_container = abjad.Container(r"c'8 d'4 e'8 ~ e'2")
    fade_in_container = abjad.Container(r"c'2 d'2")
    fader = auxjad.CrossFader(fade_out_container,
                              fade_in_container,
                              disable_rewrite_meter=True,
                              )
    selection_a, selection_b = fader.output_n(3)
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                c'8
                d'4
                e'8
                ~
                e'2
                r8
                d'4
                e'8
                ~
                e'2
                r8
                d'4
                e'8
                ~
                e'2
            }
            \new Staff
            {
                \time 4/4
                R1
                R1
                r2
                d'2
            }
        >>
        """
    )


def test_CrossFader_16():
    random.seed(81662)
    fade_out_container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
    fade_in_container = abjad.Container(r"\time 4/4 g'2 a'2")
    fader = auxjad.CrossFader(fade_out_container,
                              fade_in_container,
                              fade_in_first=True,
                              fade_out_last=True,
                              weighted_duration=True,
                              )
    selection_a, selection_b = fader.output_all()
    staff_a = abjad.Staff(selection_a)
    staff_b = abjad.Staff(selection_b)
    auxjad.mutate.sync_containers([staff_a, staff_b])
    score = abjad.Score([staff_a, staff_b])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 3/4
                c'4
                d'4
                e'4
                c'4
                d'4
                e'4
                c'4
                r4
                e'4
                c'4
                r2
                c'4
                r2
                R1 * 3/4
                R1 * 3/4
                R1 * 3/4
            }
            \new Staff
            {
                \time 4/4
                R1
                r2
                a'2
                r2
                a'2
                r2
                a'2
                g'2
                a'2
                g'2
                a'2
            }
        >>
        """
    )


def test_CrossFader_17():
    fade_out_container = abjad.Container(r"fs'4 g'2 bf'4")
    fade_in_container = abjad.Container(r"\times 4/5 {cs''4 d''1}")
    fader = auxjad.CrossFader(fade_out_container,
                              fade_in_container,
                              fade_in_first=True,
                              fade_out_last=True,
                              initial_repetitions=3,
                              final_repetitions=3,
                              repetition_chance=0.7,
                              weighted_duration=True,
                              disable_rewrite_meter=True,
                              omit_time_signatures=True,
                              use_multimeasure_rests=True,
                              boundary_depth=True,
                              maximum_dot_count=True,
                              rewrite_tuplets=True,
                              )
    assert fader.fade_in_first
    assert fader.fade_out_last
    assert fader.initial_repetitions == 3
    assert fader.final_repetitions == 3
    assert fader.repetition_chance == 0.7
    assert fader.weighted_duration
    assert fader.disable_rewrite_meter
    assert fader.omit_time_signatures
    assert fader.use_multimeasure_rests
    assert fader.boundary_depth
    assert fader.maximum_dot_count
    assert fader.rewrite_tuplets
    fader.fade_in_first = False
    fader.fade_out_last = False
    fader.initial_repetitions = 4
    fader.final_repetitions = 7
    fader.repetition_chance = 0.23
    fader.weighted_duration = False
    fader.disable_rewrite_meter = False
    fader.omit_time_signatures = False
    fader.use_multimeasure_rests = False
    fader.boundary_depth = False
    fader.maximum_dot_count = False
    fader.rewrite_tuplets = False
    assert not fader.fade_in_first
    assert not fader.fade_out_last
    assert fader.initial_repetitions == 4
    assert fader.final_repetitions == 7
    assert fader.repetition_chance == 0.23
    assert not fader.weighted_duration
    assert not fader.disable_rewrite_meter
    assert not fader.omit_time_signatures
    assert not fader.use_multimeasure_rests
    assert not fader.boundary_depth
    assert not fader.maximum_dot_count
    assert not fader.rewrite_tuplets


def test_CrossFader_18():
    random.seed(97142)
    fade_out_container = abjad.Container(r"c'4.\p e'8--\f ~ e'2")
    fade_in_container = abjad.Container(
        r"\times 2/3 {f'4-.\pp r4 d'4->\f ~ } d'2"
    )
    fader = auxjad.CrossFader(fade_out_container,
                              fade_in_container,
                              fade_in_first=True,
                              fade_out_last=True,
                              )
    selection_a, selection_b = fader.output_all()
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 4/4
                c'4.
                \p
                e'8
                \f
                - \tenuto
                ~
                e'2
                c'4.
                \p
                e'8
                \f
                - \tenuto
                ~
                e'2
                r4.
                e'8
                - \tenuto
                ~
                e'2
                r4.
                e'8
                - \tenuto
                ~
                e'2
                R1
            }
            \new Staff
            {
                \time 4/4
                R1
                \times 2/3
                {
                    f'4
                    \pp
                    - \staccato
                    r2
                }
                r2
                \times 2/3
                {
                    f'4
                    - \staccato
                    r2
                }
                r2
                \times 2/3
                {
                    f'4
                    - \staccato
                    r4
                    d'4
                    \f
                    - \accent
                    ~
                }
                d'2
                \times 2/3
                {
                    f'4
                    \pp
                    - \staccato
                    r4
                    d'4
                    \f
                    - \accent
                    ~
                }
                d'2
            }
        >>
        """
    )


def test_CrossFader_19():
    random.seed(25519)
    fade_out_container = abjad.Container(r"\times 2/3 {<c' e'>2 g'1}")
    fade_in_container = abjad.Container(r"<d' ef'>2. <bf a'>4")
    fader = auxjad.CrossFader(fade_out_container,
                              fade_in_container,
                              fade_in_first=True,
                              fade_out_last=True,
                              )
    selection_a, selection_b = fader.output_all()
    score = abjad.Score([
        abjad.Staff(selection_a),
        abjad.Staff(selection_b),
    ])
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \times 2/3
                {
                    \time 4/4
                    <c' e'>2
                    g'1
                }
                \times 2/3
                {
                    <c' e'>2
                    g'1
                }
                \times 2/3
                {
                    <c' e'>2
                    g'1
                }
                \times 2/3
                {
                    <c' e'>2
                    g'1
                }
                \times 2/3
                {
                    c'2
                    g'1
                }
                \times 2/3
                {
                    c'2
                    g'1
                }
                \times 2/3
                {
                    c'2
                    r1
                }
                R1
            }
            \new Staff
            {
                \time 4/4
                R1
                ef'2.
                r4
                <d' ef'>2.
                r4
                <d' ef'>2.
                bf4
                <d' ef'>2.
                bf4
                <d' ef'>2.
                <bf a'>4
                <d' ef'>2.
                <bf a'>4
                <d' ef'>2.
                <bf a'>4
            }
        >>
        """
    )


def test_CrossFader_20():
    random.seed(87144)
    fade_out_container = abjad.Container(r"b'8 c''8 e''2 g''4")
    fade_in_container = abjad.Container(r"\times 2/3 {e'2 d'2 c'2}")
    fader = auxjad.CrossFader(fade_out_container, fade_in_container)
    selection_a, selection_b = fader.output_all()
    literal_voice_one = abjad.LilyPondLiteral(r'\voiceOne')
    literal_voice_two = abjad.LilyPondLiteral(r'\voiceTwo')
    abjad.attach(literal_voice_one, selection_a[0])
    abjad.attach(literal_voice_two, selection_b[0])
    staff = abjad.Staff(
        [abjad.Voice(selection_a), abjad.Voice(selection_b)],
        simultaneous=True,
    )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        <<
            \new Voice
            {
                \time 4/4
                \voiceOne
                b'8
                c''8
                e''2
                g''4
                b'8
                c''8
                e''2
                r4
                b'8
                c''8
                e''2
                r4
                b'8
                c''8
                e''2
                r4
                b'8
                c''8
                e''2
                r4
                b'8
                c''8
                r2.
                b'8
                r2..
                R1
            }
            \new Voice
            {
                \time 4/4
                \voiceTwo
                R1
                R1
                \times 2/3
                {
                    r1
                    c'2
                }
                \times 2/3
                {
                    e'2
                    r2
                    c'2
                }
                \times 2/3
                {
                    e'2
                    d'2
                    c'2
                }
                \times 2/3
                {
                    e'2
                    d'2
                    c'2
                }
                \times 2/3
                {
                    e'2
                    d'2
                    c'2
                }
                \times 2/3
                {
                    e'2
                    d'2
                    c'2
                }
            }
        >>
        """
    )
