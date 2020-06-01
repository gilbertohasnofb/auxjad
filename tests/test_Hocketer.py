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
                               disable_rewrite_meter=True,
                               use_multimeasure_rests=False,
                               )
    assert hocketer.n_voices == 3
    assert hocketer.weights == [1, 2, 5]
    assert hocketer.k == 2
    assert hocketer.disable_rewrite_meter
    assert not hocketer.use_multimeasure_rests
    hocketer.n_voices = 5
    hocketer.weights = [1, 1, 1, 2, 7]
    hocketer.k = 3
    hocketer.disable_rewrite_meter = False
    hocketer.use_multimeasure_rests = True
    assert hocketer.n_voices == 5
    assert hocketer.weights == [1, 1, 1, 2, 7]
    assert hocketer.k == 3
    assert not hocketer.disable_rewrite_meter
    assert hocketer.use_multimeasure_rests


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


def test_Hocketer_08():
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
