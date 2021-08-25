import random

import abjad
import pytest

import auxjad


def test_Hocketer_01():
    random.seed(82132)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    hocketer = auxjad.Hocketer(container)
    assert hocketer.n_voices == 2
    assert hocketer.weights == [1.0, 1.0]
    assert hocketer.k == 1
    assert abjad.lilypond(hocketer) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
        }
        """
    )
    music = hocketer()
    score = abjad.Score()
    for selection in music:
        score.append(abjad.Staff(selection))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                r2
                e'4
                r4
            }
            \new Staff
            {
                c'4
                d'4
                r4
                f'4
            }
        >>
        """
    )
    music = hocketer.current_window
    with pytest.raises(AttributeError):
        hocketer.current_window = abjad.Container(r"c''2 e''2")
    score = abjad.Score()
    for selection in music:
        score.append(abjad.Staff(selection))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                r2
                e'4
                r4
            }
            \new Staff
            {
                c'4
                d'4
                r4
                f'4
            }
        >>
        """
    )


def test_Hocketer_02():
    random.seed(48765)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    hocketer = auxjad.Hocketer(container, n_voices=3)
    music = hocketer()
    score = abjad.Score()
    for selection in music:
        score.append(abjad.Staff(selection))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                c'8
                r8
                e'8
                r8
                g'8
                r4.
            }
            \new Staff
            {
                r8
                d'8
                r4
                r8
                a'8
                r4
            }
            \new Staff
            {
                r4.
                f'8
                r4
                b'8
                c''8
            }
        >>
        """
    )


def test_Hocketer_03():
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 \time 2/4 f'4 g'4")
    hocketer = auxjad.Hocketer(container,
                               n_voices=3,
                               weights=[1, 2, 5],
                               k=2,
                               force_k_voices=True,
                               explode_chords=True,
                               pitch_ranges=[abjad.PitchRange("[C4, D6]"),
                                             abjad.PitchRange("[C2, A4]"),
                                             abjad.PitchRange("[C1, E3]"),
                                             ],
                               disable_rewrite_meter=True,
                               use_multimeasure_rests=False,
                               omit_time_signatures=True,
                               boundary_depth=0,
                               maximum_dot_count=1,
                               rewrite_tuplets=False,
                               )
    assert hocketer.n_voices == 3
    assert hocketer.weights == [1, 2, 5]
    assert hocketer.k == 2
    assert hocketer.force_k_voices
    assert hocketer.explode_chords
    assert hocketer.pitch_ranges == [abjad.PitchRange("[C4, D6]"),
                                     abjad.PitchRange("[C2, A4]"),
                                     abjad.PitchRange("[C1, E3]"),
                                     ]
    assert hocketer.disable_rewrite_meter
    assert not hocketer.use_multimeasure_rests
    assert hocketer.omit_time_signatures
    assert hocketer.boundary_depth == 0
    assert hocketer.maximum_dot_count == 1
    assert not hocketer.rewrite_tuplets
    hocketer.n_voices = 5
    hocketer.weights = [1, 1, 1, 2, 7]
    hocketer.k = 3
    hocketer.force_k_voices = False
    hocketer.explode_chords = False
    hocketer.pitch_ranges = None
    hocketer.disable_rewrite_meter = False
    hocketer.use_multimeasure_rests = True
    hocketer.omit_time_signatures = False
    hocketer.boundary_depth = 1
    hocketer.maximum_dot_count = 2
    hocketer.rewrite_tuplets = True
    assert hocketer.n_voices == 5
    assert hocketer.weights == [1, 1, 1, 2, 7]
    assert hocketer.k == 3
    assert not hocketer.force_k_voices
    assert not hocketer.explode_chords
    assert hocketer.pitch_ranges is None
    assert not hocketer.disable_rewrite_meter
    assert hocketer.use_multimeasure_rests
    assert not hocketer.omit_time_signatures
    assert hocketer.boundary_depth == 1
    assert hocketer.maximum_dot_count == 2
    assert hocketer.rewrite_tuplets


def test_Hocketer_04():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    hocketer = auxjad.Hocketer(container)
    assert abjad.lilypond(hocketer.contents) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
        }
        """
    )
    hocketer()
    assert abjad.lilypond(hocketer.contents) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
        }
        """
    )
    hocketer.contents = abjad.Container(r"cs2 ds2")
    assert abjad.lilypond(hocketer.contents) == abjad.String.normalize(
        r"""
        {
            cs2
            ds2
        }
        """
    )


def test_Hocketer_05():
    container = abjad.Container(r"c'2 d'2 e'2 f' 2")
    hocketer = auxjad.Hocketer(container)
    assert len(hocketer) == 2
    hocketer = auxjad.Hocketer(container, n_voices=7)
    assert len(hocketer) == 7


def test_Hocketer_06():
    random.seed(12174)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    hocketer = auxjad.Hocketer(container)
    music = hocketer()
    score = abjad.Score()
    for selection in music:
        score.append(abjad.Staff(selection))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                c'8
                d'8
                r4
                r8
                a'8
                r4
            }
            \new Staff
            {
                r4
                e'8
                f'8
                g'8
                r8
                b'8
                c''8
            }
        >>
        """
    )
    random.seed(12174)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    hocketer = auxjad.Hocketer(container,
                               disable_rewrite_meter=True,
                               )
    music = hocketer()
    score = abjad.Score()
    for selection in music:
        score.append(abjad.Staff(selection))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                c'8
                d'8
                r8
                r8
                r8
                a'8
                r8
                r8
            }
            \new Staff
            {
                r8
                r8
                e'8
                f'8
                g'8
                r8
                b'8
                c''8
            }
        >>
        """
    )


def test_Hocketer_07():
    random.seed(87201)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    hocketer = auxjad.Hocketer(container, weights=[2.1, 5.7])
    music = hocketer()
    score = abjad.Score()
    for selection in music:
        score.append(abjad.Staff(selection))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                r8
                d'8
                r4
                g'8
                r4.
            }
            \new Staff
            {
                c'8
                r8
                e'8
                f'8
                r8
                a'8
                b'8
                c''8
            }
        >>
        """
    )
    assert hocketer.weights == [2.1, 5.7]
    hocketer.reset_weights()
    assert hocketer.weights == [1.0, 1.0]


def test_Hocketer_08():
    random.seed(98212)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    hocketer = auxjad.Hocketer(container, n_voices=4, k=2)
    music = hocketer()
    score = abjad.Score()
    for selection in music:
        score.append(abjad.Staff(selection))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                c'4
                d'4
                e'4
                r4
            }
            \new Staff
            {
                r2
                e'4
                f'4
            }
            \new Staff
            {
                r2.
                f'4
            }
            \new Staff
            {
                r4
                d'4
                r2
            }
        >>
        """
    )


def test_Hocketer_09():
    random.seed(15663)
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 f'4 g'4 a'4")
    hocketer = auxjad.Hocketer(container)
    music = hocketer()
    score = abjad.Score()
    for selection in music:
        score.append(abjad.Staff(selection))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 3/4
                R1 * 3/4
                r4
                g'4
                a'4
            }
            \new Staff
            {
                \time 3/4
                c'4
                d'4
                e'4
                f'4
                r2
            }
        >>
        """
    )
    random.seed(15663)
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 f'4 g'4 a'4")
    hocketer = auxjad.Hocketer(container,
                               use_multimeasure_rests=False,
                               )
    music = hocketer()
    score = abjad.Score()
    for selection in music:
        score.append(abjad.Staff(selection))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 3/4
                r2.
                r4
                g'4
                a'4
            }
            \new Staff
            {
                \time 3/4
                c'4
                d'4
                e'4
                f'4
                r2
            }
        >>
        """
    )


def test_Hocketer_10():
    random.seed(14432)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    hocketer = auxjad.Hocketer(container,
                               n_voices=3,
                               k=2,
                               force_k_voices=True,
                               )
    music = hocketer()
    score = abjad.Score()
    for selection in music:
        score.append(abjad.Staff(selection))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                c'8
                d'8
                r8
                f'8
                g'8
                a'8
                b'8
                c''8
            }
            \new Staff
            {
                c'8
                r8
                e'8
                f'8
                r4
                b'8
                r8
            }
            \new Staff
            {
                r8
                d'8
                e'8
                r8
                g'8
                a'8
                r8
                c''8
            }
        >>
        """
    )


def test_Hocketer_11():
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    with pytest.raises(ValueError):
        hocketer = auxjad.Hocketer(container,  # noqa: F841
                                   n_voices=2,
                                   k=4,
                                   force_k_voices=True,
                                   )

    hocketer = auxjad.Hocketer(container,
                               n_voices=4,
                               k=3,
                               force_k_voices=True,
                               )
    with pytest.raises(ValueError):
        hocketer.k = 5
        hocketer.n_voices = 2

    hocketer = auxjad.Hocketer(container, n_voices=4, k=5)
    with pytest.raises(ValueError):
        hocketer.force_k_voices = True


def test_Hocketer_12():
    random.seed(48765)
    container = abjad.Container(
        r"\time 5/4 r4 \times 2/3 {c'4 d'2} e'4. f'8"
        r"\times 4/5 {\time 4/4 g'2. \times 2/3 {a'8 r8 b'2}}"
    )
    hocketer = auxjad.Hocketer(container,
                               n_voices=4,
                               k=2,
                               )
    music = hocketer()
    score = abjad.Score()
    for selection in music:
        score.append(abjad.Staff(selection))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 5/4
                r4
                \times 2/3
                {
                    c'4
                    d'2
                }
                r4.
                f'8
                \times 4/5
                {
                    \time 4/4
                    r2.
                    \times 2/3
                    {
                        a'8
                        r8
                        r2
                    }
                }
            }
            \new Staff
            {
                \time 5/4
                R1 * 5/4
                \time 4/4
                R1
            }
            \new Staff
            {
                \time 5/4
                r4
                \times 2/3
                {
                    r4
                    d'2
                }
                e'4.
                f'8
                \times 4/5
                {
                    \time 4/4
                    r2.
                    \times 2/3
                    {
                        a'8
                        r8
                        b'2
                    }
                }
            }
            \new Staff
            {
                \time 5/4
                r4
                \times 2/3
                {
                    c'4
                    r2
                }
                r2
                \times 4/5
                {
                    \time 4/4
                    g'2.
                    \times 2/3
                    {
                        r4
                        b'2
                    }
                }
            }
        >>
        """
    )


def test_Hocketer_13():
    container = abjad.Container(r"c'4. d'8 e'2")
    hocketer = auxjad.Hocketer(container,
                               n_voices=1,
                               )
    music = hocketer()
    score = abjad.Score()
    for selection in music:
        score.append(abjad.Staff(selection))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                c'4.
                d'8
                e'2
            }
        >>
        """
    )
    hocketer = auxjad.Hocketer(container,
                               n_voices=1,
                               boundary_depth=1,
                               )
    music = hocketer()
    score = abjad.Score()
    for selection in music:
        score.append(abjad.Staff(selection))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                c'4
                ~
                c'8
                d'8
                e'2
            }
        >>
        """
    )


def test_Hocketer_14():
    random.seed(15663)
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 f'4 g'4 a'4")
    hocketer = auxjad.Hocketer(container,
                               omit_time_signatures=True,
                               use_multimeasure_rests=False,
                               )
    music = hocketer()
    score = abjad.Score()
    for selection in music:
        score.append(abjad.Staff(selection))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                r2.
                r4
                g'4
                a'4
            }
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
                r2
            }
        >>
        """
    )


def test_Hocketer_15():
    random.seed(12432)
    container = abjad.Container(
        r"c'2-.\p\< d'2-.\f\> e'1 f'2.\pp\< g'4--\p "
        r"a'2\ff\> b'2\p\> ~ b'2 c''2\ppp"
    )
    hocketer = auxjad.Hocketer(container,
                               n_voices=3,
                               k=2,
                               force_k_voices=True,
                               )
    music = hocketer()
    score = abjad.Score()
    for selection in music:
        score.append(abjad.Staff(selection))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                c'2
                \p
                - \staccato
                \<
                d'2
                \f
                - \staccato
                \>
                e'1
                f'2.
                \pp
                \<
                g'4
                \p
                - \tenuto
                a'2
                \ff
                \>
                r2
                \p
                r2
                c''2
                \ppp
            }
            \new Staff
            {
                r2
                d'2
                \f
                - \staccato
                \>
                e'1
                r2.
                \pp
                g'4
                \p
                - \tenuto
                r2
                b'2
                \>
                ~
                b'2
                r2
                \ppp
            }
            \new Staff
            {
                c'2
                \p
                - \staccato
                \<
                r2
                \f
                R1
                f'2.
                \pp
                \<
                r4
                \p
                a'2
                \ff
                \>
                b'2
                \p
                \>
                ~
                b'2
                c''2
                \ppp
            }
        >>
        """
    )


def test_Hocketer_16():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    hocketer = auxjad.Hocketer(container)
    for voice in hocketer():
        assert isinstance(voice, abjad.Selection)
    tuplet = abjad.Tuplet('3:2', r"c'2 d'2 e'2")
    hocketer = auxjad.Hocketer(tuplet)
    for voice in hocketer():
        assert isinstance(voice, abjad.Selection)
    voice = abjad.Voice(r"c'4 d'4 e'4 f'4")
    hocketer = auxjad.Hocketer(voice)
    for voice in hocketer():
        assert isinstance(voice, abjad.Selection)
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    hocketer = auxjad.Hocketer(staff)
    for voice in hocketer():
        assert isinstance(voice, abjad.Selection)
    score = abjad.Score([abjad.Staff(r"c'4 d'4 e'4 f'4")])
    hocketer = auxjad.Hocketer(score)
    for voice in hocketer():
        assert isinstance(voice, abjad.Selection)
    voice = abjad.Voice(r"c'4 d'4 e'4 f'4")
    staff = abjad.Staff([voice])
    hocketer = auxjad.Hocketer(staff)
    for voice in hocketer():
        assert isinstance(voice, abjad.Selection)
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    score = abjad.Score([staff])
    hocketer = auxjad.Hocketer(score)
    for voice in hocketer():
        assert isinstance(voice, abjad.Selection)

    voice1 = abjad.Voice(r"c'4 d'4 e'4 f'4")
    voice2 = abjad.Voice(r"g2 f2")
    staff = abjad.Staff([voice1, voice2], simultaneous=True)
    with pytest.raises(ValueError):
        hocketer = auxjad.Hocketer(staff)  # noqa: F841

    staff1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
    staff2 = abjad.Staff(r"g2 f2")
    score = abjad.Score([staff1, staff2])
    with pytest.raises(ValueError):
        hocketer = auxjad.Hocketer(score)  # noqa: F841


def test_Hocketer_17():
    random.seed(19876)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    hocketer = auxjad.Hocketer(container, n_voices=5, k=3)
    hocketer()
    score = abjad.Score()
    for selection in hocketer[:]:
        staff = abjad.Staff(selection)
        score.append(staff)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                r2.
                f'4
            }
            \new Staff
            {
                c'4
                r4
                e'4
                r4
            }
            \new Staff
            {
                r4
                d'4
                e'4
                r4
            }
            \new Staff
            {
                c'4
                d'4
                r4
                f'4
            }
            \new Staff
            {
                c'4
                r4
                e'4
                r4
            }
        >>
        """
    )
    staff = abjad.Staff(hocketer[0])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r2.
            f'4
        }
        """
    )
    partial_score = abjad.Score()
    for selection in hocketer[1:4]:
        staff = abjad.Staff(selection)
        partial_score.append(staff)
    assert abjad.lilypond(partial_score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                c'4
                r4
                e'4
                r4
            }
            \new Staff
            {
                r4
                d'4
                e'4
                r4
            }
            \new Staff
            {
                c'4
                d'4
                r4
                f'4
            }
        >>
        """
    )


def test_Hocketer_18():
    random.seed(97813)
    container = abjad.Container(r"c4 d8 e'8 f'4 g'8 a8")
    hocketer = auxjad.Hocketer(container,
                               n_voices=2,
                               pitch_ranges=[abjad.PitchRange("[C4, B5]"),
                                             abjad.PitchRange("[C3, B3]"),
                                             ])
    hocketer()
    score = abjad.Score()
    for selection in hocketer[:]:
        staff = abjad.Staff(selection)
        score.append(staff)
    abjad.attach(abjad.Clef('bass'), abjad.select(score[1]).leaf(0))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                r4.
                e'8
                f'4
                g'8
                r8
            }
            \new Staff
            {
                \clef "bass"
                c4
                d8
                r8
                r4.
                a8
            }
        >>
        """
    )


def test_Hocketer_19():
    random.seed(66191)
    container = abjad.Container(r"c' d' e f' g a' b' c''")
    hocketer = auxjad.Hocketer(container,
                               n_voices=3,
                               pitch_ranges=[abjad.PitchRange("[C4, C5]"),
                                             abjad.PitchRange("[C4, C5]"),
                                             abjad.PitchRange("[C3, B3]"),
                                             ])
    hocketer()
    score = abjad.Score()
    for selection in hocketer[:]:
        staff = abjad.Staff(selection)
        score.append(staff)
    abjad.attach(abjad.Clef('bass'), abjad.select(score[2]).leaf(0))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                c'4
                d'4
                r4
                f'4
                r4
                a'4
                r2
            }
            \new Staff
            {
                R1
                r2
                b'4
                c''4
            }
            \new Staff
            {
                \clef "bass"
                r2
                e4
                r4
                g4
                r2.
            }
        >>
        """
    )


def test_Hocketer_20():
    random.seed(81742)
    container = abjad.Container(r"c'8 d'8 e8 f'8 g8 a'8 b'8 c''8")
    hocketer = auxjad.Hocketer(container,
                               n_voices=4,
                               k=2,
                               force_k_voices=True,
                               pitch_ranges=[abjad.PitchRange("[C4, C5]"),
                                             abjad.PitchRange("[C4, C5]"),
                                             abjad.PitchRange("[E3, G4]"),
                                             abjad.PitchRange("[E3, G4]"),
                                             ])
    hocketer()
    score = abjad.Score()
    for selection in hocketer[:]:
        staff = abjad.Staff(selection)
        score.append(staff)
    abjad.attach(abjad.Clef('bass'), abjad.select(score[2]).leaf(0))
    abjad.attach(abjad.Clef('bass'), abjad.select(score[3]).leaf(0))
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                r2
                r8
                a'8
                b'8
                c''8
            }
            \new Staff
            {
                c'8
                d'8
                r4
                r8
                a'8
                b'8
                c''8
            }
            \new Staff
            {
                \clef "bass"
                r8
                d'8
                e8
                f'8
                g8
                r4.
            }
            \new Staff
            {
                \clef "bass"
                c'8
                r8
                e8
                f'8
                g8
                r4.
            }
        >>
        """
    )


def test_Hocketer_21():
    random.seed(48124)
    container = abjad.Container(
        r"<c' e' g'>4 <d' f' a'>4 <e' g' b'>4 <f' a' c'>4"
    )
    hocketer = auxjad.Hocketer(container,
                               n_voices=3,
                               )
    hocketer()
    score = abjad.Score()
    for selection in hocketer[:]:
        staff = abjad.Staff(selection)
        score.append(staff)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                r2
                <e' g' b'>4
                r4
            }
            \new Staff
            {
                <c' e' g'>4
                <d' f' a'>4
                r2
            }
            \new Staff
            {
                r2.
                <c' f' a'>4
            }
        >>
        """
    )

    container = abjad.Container(
        r"<c' e' g'>4 <d' f' a'>4 <e' g' b'>4 <f' a' c'>4"
    )
    hocketer = auxjad.Hocketer(container,
                               n_voices=3,
                               explode_chords=True,
                               )
    hocketer()
    score = abjad.Score()
    for selection in hocketer[:]:
        staff = abjad.Staff(selection)
        score.append(staff)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                e'4
                f'4
                e'4
                a'4
            }
            \new Staff
            {
                g'4
                d'4
                b'4
                c'4
            }
            \new Staff
            {
                c'4
                a'4
                g'4
                f'4
            }
        >>
        """
    )


def test_Hocketer_22():
    random.seed(91776)
    container = abjad.Container(
        r"<c' e' g'>4 <d' f' a'>4 <e' g' b'>4 <f' a' c''>4"
    )
    hocketer = auxjad.Hocketer(container,
                               n_voices=3,
                               explode_chords=True,
                               pitch_ranges=[abjad.PitchRange("[E4, C5]"),
                                             abjad.PitchRange("[E4, C5]"),
                                             abjad.PitchRange("[C4, F4]"),
                                             ],
                               )
    hocketer()
    score = abjad.Score()
    for selection in hocketer[:]:
        staff = abjad.Staff(selection)
        score.append(staff)
    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                e'4
                f'4
                g'4
                c''4
            }
            \new Staff
            {
                g'4
                a'4
                b'4
                a'4
            }
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
            }
        >>
        """
    )


def test_Hocketer_23():
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 \time 2/4 f'4 g'4")
    hocketer = auxjad.Hocketer(container,
                               n_voices=3,
                               pitch_ranges=[abjad.PitchRange("[C4, D6]"),
                                             abjad.PitchRange("[C2, A4]"),
                                             abjad.PitchRange("[C1, E3]"),
                                             ],
                               )
    assert hocketer.pitch_ranges == [abjad.PitchRange("[C4, D6]"),
                                     abjad.PitchRange("[C2, A4]"),
                                     abjad.PitchRange("[C1, E3]"),
                                     ]
    hocketer.n_voices = 4
    assert hocketer.pitch_ranges is None
