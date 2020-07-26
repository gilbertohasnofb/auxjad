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
    assert format(hocketer) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    music = hocketer()
    score = abjad.Score(music)
    assert format(score) == abjad.String.normalize(
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
        """)
    music = hocketer.current_window
    with pytest.raises(AttributeError):
        hocketer.current_window = abjad.Container(r"c''2 e''2")
    score = abjad.Score(music)
    assert format(score) == abjad.String.normalize(
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
        """)


def test_Hocketer_02():
    random.seed(48765)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    hocketer = auxjad.Hocketer(container, n_voices=3)
    music = hocketer()
    score = abjad.Score(music)
    assert format(score) == abjad.String.normalize(
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
                r4.
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
        """)


def test_Hocketer_03():
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 \time 2/4 f'4 g'4")
    hocketer = auxjad.Hocketer(container,
                               n_voices=3,
                               weights=[1, 2, 5],
                               k=2,
                               force_k_voices=True,
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
    assert not hocketer.disable_rewrite_meter
    assert hocketer.use_multimeasure_rests
    assert not hocketer.omit_time_signatures
    assert hocketer.boundary_depth == 1
    assert hocketer.maximum_dot_count == 2
    assert hocketer.rewrite_tuplets


def test_Hocketer_04():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    hocketer = auxjad.Hocketer(container)
    assert format(hocketer.contents) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    hocketer()
    assert format(hocketer.contents) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    hocketer.contents = abjad.Container(r"cs2 ds2")
    assert format(hocketer.contents) == abjad.String.normalize(
        r"""
        {
            cs2
            ds2
        }
        """)


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
    score = abjad.Score(music)
    assert format(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                c'8
                d'8
                r4.
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
        """)
    random.seed(12174)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    hocketer = auxjad.Hocketer(container,
                               disable_rewrite_meter=True,
                               )
    music = hocketer()
    score = abjad.Score(music)
    assert format(score) == abjad.String.normalize(
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
        """)


def test_Hocketer_07():
    random.seed(87201)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    hocketer = auxjad.Hocketer(container, weights=[2.1, 5.7])
    music = hocketer()
    score = abjad.Score(music)
    assert format(score) == abjad.String.normalize(
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
        """)
    assert hocketer.weights == [2.1, 5.7]
    hocketer.reset_weights()
    assert hocketer.weights == [1.0, 1.0]


def test_Hocketer_08():
    random.seed(98212)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    hocketer = auxjad.Hocketer(container, n_voices=4, k=2)
    music = hocketer()
    score = abjad.Score(music)
    assert format(score) == abjad.String.normalize(
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
        """)


def test_Hocketer_09():
    random.seed(15663)
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 f'4 g'4 a'4")
    hocketer = auxjad.Hocketer(container)
    music = hocketer()
    score = abjad.Score(music)
    assert format(score) == abjad.String.normalize(
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
        """)
    random.seed(15663)
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 f'4 g'4 a'4")
    hocketer = auxjad.Hocketer(container,
                               use_multimeasure_rests=False,
                               )
    music = hocketer()
    score = abjad.Score(music)
    assert format(score) == abjad.String.normalize(
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
        """)


def test_Hocketer_10():
    random.seed(14432)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    hocketer = auxjad.Hocketer(container,
                               n_voices=3,
                               k=2,
                               force_k_voices=True,
                               )
    music = hocketer()
    score = abjad.Score(music)
    assert format(score) == abjad.String.normalize(
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
                r8
                b'8
                c''8
            }
            \new Staff
            {
                r4
                e'8
                r8
                g'8
                a'8
                b'8
                c''8
            }
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
                r8
                a'8
                r4
            }
        >>
        """)


def test_Hocketer_11():
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    with pytest.raises(ValueError):
        hocketer = auxjad.Hocketer(container,
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
    with pytest.raises(ValueError):
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
    staves = hocketer()
    score = abjad.Score(staves)
    assert format(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 5/4
                r4
                \times 2/3 {
                    c'4
                    d'2
                }
                r4.
                f'8
                \times 4/5 {
                    \time 4/4
                    r2.
                    \times 2/3 {
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
                \times 2/3 {
                    r4
                    d'2
                }
                e'4.
                f'8
                \times 4/5 {
                    \time 4/4
                    r2.
                    \times 2/3 {
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
                \times 2/3 {
                    c'4
                    r2
                }
                r2
                \times 4/5 {
                    \time 4/4
                    g'2.
                    \times 2/3 {
                        r4
                        b'2
                    }
                }
            }
        >>
        """)


def test_Hocketer_13():
    container = abjad.Container(r"c'4. d'8 e'2")
    hocketer = auxjad.Hocketer(container,
                               n_voices=1,
                               )
    music = hocketer()
    score = abjad.Score(music)
    assert format(score) == abjad.String.normalize(
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
        """)
    hocketer = auxjad.Hocketer(container,
                               n_voices=1,
                               boundary_depth=1,
                               )
    music = hocketer()
    score = abjad.Score(music)
    assert format(score) == abjad.String.normalize(
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
        """)


def test_Hocketer_14():
    random.seed(15663)
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 f'4 g'4 a'4")
    hocketer = auxjad.Hocketer(container,
                               omit_time_signatures=True,
                               use_multimeasure_rests=False,
                               )
    music = hocketer()
    score = abjad.Score(music)
    assert format(score) == abjad.String.normalize(
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
        """)


def test_Hocketer_15():
    random.seed(14432)
    container = abjad.Container(r"c'2-.\p\< d'2-.\f\> e'1 f'2.\pp\< "
                                r"g'4--\p a'2\ff\> b'2\p\> ~ b'2 c''2\!")
    hocketer = auxjad.Hocketer(container,
                               n_voices=3,
                               k=2,
                               force_k_voices=True,
                               )
    music = hocketer()
    score = abjad.Score(music)
    assert format(score) == abjad.String.normalize(
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
                R1
                f'2.
                \pp
                \<
                g'4
                \p
                - \tenuto
                r2
                b'2
                \>
                ~
                b'2
                c''2
                \!
            }
            \new Staff
            {
                R1
                e'1
                \f
                \>
                r2.
                \pp
                g'4
                \p
                - \tenuto
                a'2
                \ff
                \>
                b'2
                \p
                \>
                ~
                b'2
                c''2
                \!
            }
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
                r4
                \p
                a'2
                \ff
                \>
                r2
                \p
                R1
            }
        >>
        """)


def test_Hocketer_16():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    hocketer = auxjad.Hocketer(container)
    for voice in hocketer():
        assert isinstance(voice, abjad.Staff)
    tuplet = abjad.Tuplet('3:2', r"c'2 d'2 e'2")
    hocketer = auxjad.Hocketer(tuplet)
    for voice in hocketer():
        assert isinstance(voice, abjad.Staff)
    voice = abjad.Voice(r"c'4 d'4 e'4 f'4")
    hocketer = auxjad.Hocketer(voice)
    for voice in hocketer():
        assert isinstance(voice, abjad.Staff)
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    hocketer = auxjad.Hocketer(staff)
    for voice in hocketer():
        assert isinstance(voice, abjad.Staff)
    score = abjad.Score([abjad.Staff(r"c'4 d'4 e'4 f'4")])
    hocketer = auxjad.Hocketer(score)
    for voice in hocketer():
        assert isinstance(voice, abjad.Staff)
    voice = abjad.Voice(r"c'4 d'4 e'4 f'4")
    staff = abjad.Staff([voice])
    hocketer = auxjad.Hocketer(staff)
    for voice in hocketer():
        assert isinstance(voice, abjad.Staff)
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    score = abjad.Score([staff])
    hocketer = auxjad.Hocketer(score)
    for voice in hocketer():
        assert isinstance(voice, abjad.Staff)
    voice1 = abjad.Voice(r"c'4 d'4 e'4 f'4")
    voice2 = abjad.Voice(r"g2 f2")
    staff = abjad.Staff([voice1, voice2], simultaneous=True)
    with pytest.raises(ValueError):
        auxjad.Hocketer(staff)
    staff1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
    staff2 = abjad.Staff(r"g2 f2")
    score = abjad.Score([staff1, staff2])
    with pytest.raises(ValueError):
        auxjad.Hocketer(score)


def test_Hocketer_17():
    random.seed(19876)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    hocketer = auxjad.Hocketer(container, n_voices=5, k=3)
    hocketer()
    score = abjad.Score()
    for selection in hocketer[:]:
        staff = abjad.Staff(selection)
        score.append(staff)
    assert format(score) == abjad.String.normalize(
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
        """)
    staff = abjad.Staff(hocketer[0])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r2.
            f'4
        }
        """)
    partial_score = abjad.Score()
    for selection in hocketer[1:4]:
        staff = abjad.Staff(selection)
        partial_score.append(staff)
    assert format(partial_score) == abjad.String.normalize(
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
        """)
