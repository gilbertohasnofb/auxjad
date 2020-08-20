import random

import abjad
import pytest

import auxjad


def test_WindowLooper_01():
    container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.WindowLooper(container)
    assert format(looper) == abjad.String.normalize(
        r"""
        {
            c'4
            d'2
            e'4
            f'2
            ~
            f'8
            g'1
        }
        """)
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'2
            e'4
        }
        """)
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'8.
            d'16
            ~
            d'4
            ~
            d'8.
            e'16
            ~
            e'8.
            f'16
        }
        """)
    notes = looper.current_window
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'8.
            d'16
            ~
            d'4
            ~
            d'8.
            e'16
            ~
            e'8.
            f'16
        }
        """)


def test_WindowLooper_02():
    container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.WindowLooper(container,
                                 window_size=(3, 4),
                                 step_size=(1, 8),
                                 )
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'2
        }
        """)
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'8
            d'8
            ~
            d'4.
            e'8
        }
        """)


def test_WindowLooper_03():
    container = abjad.Container(r"c'4 d'2 e'4")
    looper = auxjad.WindowLooper(container,
                                 window_size=(3, 4),
                                 step_size=(1, 8),
                                 )
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'2
        }
        """)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'8
            d'8
            ~
            d'4.
            e'8
        }
        """)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            d'2
            e'4
        }
        """)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            d'4.
            e'4
            r8
        }
        """)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            d'4
            e'4
            r4
        }
        """)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            d'8
            e'4
            r4.
        }
        """)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            e'4
            r2
        }
        """)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            e'8
            r8
            r2
        }
        """)
    with pytest.raises(StopIteration):
        assert looper.__next__()


def test_WindowLooper_04():
    container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.WindowLooper(container,
                                 window_size=(3, 4),
                                 step_size=(5, 8),
                                 max_steps=2,
                                 repetition_chance=0.25,
                                 forward_bias=0.2,
                                 head_position=(2, 8),
                                 omit_time_signatures=False,
                                 fill_with_rests=False,
                                 boundary_depth=0,
                                 maximum_dot_count=1,
                                 rewrite_tuplets=False,
                                 process_on_first_call=True,
                                 )
    assert looper.window_size == abjad.Meter((3, 4))
    assert looper.step_size == abjad.Duration((5, 8))
    assert looper.max_steps == 2
    assert looper.repetition_chance == 0.25
    assert looper.forward_bias == 0.2
    assert looper.head_position == abjad.Duration((1, 4))
    assert not looper.omit_time_signatures
    assert not looper.fill_with_rests
    assert looper.boundary_depth == 0
    assert looper.maximum_dot_count == 1
    assert not looper.rewrite_tuplets
    assert looper.process_on_first_call
    looper.window_size = (5, 4)
    looper.step_size = (1, 4)
    looper.max_steps = 3
    looper.repetition_chance = 0.1
    looper.forward_bias = 0.8
    looper.head_position = 0
    looper.omit_time_signatures = True
    looper.fill_with_rests = True
    looper.boundary_depth = 1
    looper.maximum_dot_count = 2
    looper.rewrite_tuplets = True
    looper.process_on_first_call = False
    assert looper.window_size == abjad.Meter((5, 4))
    assert looper.step_size == abjad.Duration((1, 4))
    assert looper.max_steps == 3
    assert looper.repetition_chance == 0.1
    assert looper.forward_bias == 0.8
    assert looper.head_position == abjad.Duration(0)
    assert looper.omit_time_signatures
    assert looper.fill_with_rests
    assert looper.boundary_depth == 1
    assert looper.maximum_dot_count == 2
    assert looper.rewrite_tuplets
    assert not looper.process_on_first_call


def test_WindowLooper_05():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.WindowLooper(container,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 )
    notes = looper.output_all()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
            d'4
            e'4
            f'4
            e'4
            f'4
            r4
            f'4
            r2
        }
        """)


def test_WindowLooper_06():
    container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.WindowLooper(container)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'2
            e'4
        }
        """)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'8.
            d'16
            ~
            d'4
            ~
            d'8.
            e'16
            ~
            e'8.
            f'16
        }
        """)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'8
            d'8
            ~
            d'4
            ~
            d'8
            e'4
            f'8
        }
        """)
    looper.window_size = (3, 8)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/8
            c'16
            d'16
            ~
            d'4
        }
        """)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/8
            d'4.
        }
        """)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/8
            d'4.
        }
        """)


def test_WindowLooper_07():
    container = abjad.Container(r"\times 2/3 {c'8 d'8 e'8} d'2.")
    looper = auxjad.WindowLooper(container,
                                 window_size=(3, 4),
                                 step_size=(1, 16),
                                 )
    notes = looper.output_n(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                \time 3/4
                c'8
                d'8
                e'8
            }
            d'2
            \times 2/3 {
                c'32
                d'16
                ~
                d'16
                e'8
            }
            d'16
            ~
            d'2
            \times 2/3 {
                d'16
                e'8
            }
            d'8
            ~
            d'2
        }
        """)


def test_WindowLooper_08():
    container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.WindowLooper(container, omit_time_signatures=True)
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'2
            e'4
        }
        """)


def test_WindowLooper_09():
    wrong_type_input = 'foobar'
    container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    with pytest.raises(TypeError):
        assert auxjad.WindowLooper(wrong_type_input)
        assert auxjad.WindowLooper(container, window_size=17j)
        assert auxjad.WindowLooper(container, step_size=True)
        assert auxjad.WindowLooper(container, max_steps='foo')
        assert auxjad.WindowLooper(container, repetition_chance='bar')
        assert auxjad.WindowLooper(container, forward_bias=False)
        assert auxjad.WindowLooper(container, head_position=62.3j)
        assert auxjad.WindowLooper(container, omit_time_signatures='xyz')
        assert auxjad.WindowLooper(container, fill_with_rests=1.2)
    with pytest.raises(ValueError):
        assert auxjad.WindowLooper(container, window_size=(100, 1))
        assert auxjad.WindowLooper(container, max_steps=-1)
        assert auxjad.WindowLooper(container, repetition_chance=-0.3)
        assert auxjad.WindowLooper(container, repetition_chance=1.4)
        assert auxjad.WindowLooper(container, forward_bias=-0.3)
        assert auxjad.WindowLooper(container, forward_bias=1.4)
        assert auxjad.WindowLooper(container, head_position=(100, 1))


def test_WindowLooper_10():
    container = abjad.Container(r"c'4 e'2 d'2 f'4")
    looper = auxjad.WindowLooper(container,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 )
    notes = looper.output_all(tie_identical_pitches=True)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            e'2
            ~
            e'2
            d'4
            e'4
            d'2
            ~
            d'2
            f'4
            d'4
            f'4
            r4
            f'4
            r2
        }
        """)


def test_WindowLooper_11():
    container = abjad.Container(r"c'4 <e' f' g'>2 r4 f'2.")
    looper = auxjad.WindowLooper(container,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 )
    notes = looper.output_all(tie_identical_pitches=True)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            <e' f' g'>2
            ~
            <e' f' g'>2
            r4
            <e' f' g'>4
            r4
            f'4
            r4
            f'2
            ~
            f'2.
            ~
            f'2
            r4
            f'4
            r2
        }
        """)


def test_WindowLooper_12():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.WindowLooper(container,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 )
    notes = looper.output_n(2)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
            d'4
            e'4
            f'4
        }
        """)


def test_WindowLooper_13():
    container = abjad.Container(r"c'4 d'2 e'4 f'4")
    looper = auxjad.WindowLooper(container,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 )
    notes = looper.output_n(2, tie_identical_pitches=True)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'2
            ~
            d'2
            e'4
        }
        """)


def test_WindowLooper_14():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.WindowLooper(container,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 )
    with pytest.raises(RuntimeError):
        looper.output_n(100)


def test_WindowLooper_15():
    container = abjad.Container(r"c'4 d'4 e'4 f'4 g'4 a'4")
    looper = auxjad.WindowLooper(container,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 head_position=(3, 4),
                                 forward_bias=0.0,
                                 )
    notes = looper.output_n(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            f'4
            g'4
            a'4
            e'4
            f'4
            g'4
            d'4
            e'4
            f'4
        }
        """)


def test_WindowLooper_16():
    container = abjad.Container(r"c'4 d'4 e'4 f'4 g'4 a'4")
    looper = auxjad.WindowLooper(container,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 head_position=(3, 4),
                                 forward_bias=0.0,
                                 )
    notes = looper.output_all()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            f'4
            g'4
            a'4
            e'4
            f'4
            g'4
            d'4
            e'4
            f'4
            c'4
            d'4
            e'4
        }
        """)


def test_WindowLooper_17():
    container = abjad.Container(r"c'4 d'4 e'4 f'4 g'4 a'4")
    looper = auxjad.WindowLooper(container,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 forward_bias=0.0,
                                 )
    notes = looper.output_all()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
        }
        """)


def test_WindowLooper_18():
    container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.WindowLooper(container,
                                 process_on_first_call=True,
                                 )
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'8.
            d'16
            ~
            d'4
            ~
            d'8.
            e'16
            ~
            e'8.
            f'16
        }
        """)


def test_WindowLooper_19():
    container = abjad.Container(r"c'4-.\p\< d'2--\f e'4->\ppp f'2 ~ f'8")
    looper = auxjad.WindowLooper(container)
    staff = abjad.Staff()
    notes = looper.output_n(2)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \p
            - \staccato
            \<
            d'2
            \f
            - \tenuto
            e'4
            \ppp
            - \accent
            c'8.
            \p
            - \staccato
            \<
            d'16
            \f
            - \tenuto
            ~
            d'4
            ~
            d'8.
            e'16
            \ppp
            - \accent
            ~
            e'8.
            f'16
        }
        """)


def test_WindowLooper_20():
    container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.WindowLooper(container)
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'2
            e'4
        }
        """)
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'8.
            d'16
            ~
            d'4
            ~
            d'8.
            e'16
            ~
            e'8.
            f'16
        }
        """)
    looper.contents = abjad.Container(r"c'16 d'16 e'16 f'16 g'2. | a'1")
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            d'16
            e'16
            f'16
            g'16
            ~
            g'2
            ~
            g'8.
            a'16
        }
        """)
    looper.head_position = 0
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'16
            d'16
            e'16
            f'16
            g'2.
        }
        """)


def test_WindowLooper_21():
    container = abjad.Container(r"c'1")
    looper = auxjad.WindowLooper(container)
    assert len(looper) == 16
    container = abjad.Container(r"c'1")
    looper = auxjad.WindowLooper(container,
                                 step_size=(1, 4),
                                 )
    assert len(looper) == 4
    container = abjad.Container(r"c'2..")
    looper = auxjad.WindowLooper(container,
                                 step_size=(1, 4),
                                 window_size=(2, 4),
                                 )
    assert len(looper) == 4


def test_WindowLooper_22():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.WindowLooper(container,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 fill_with_rests=False,
                                 )
    notes = looper.output_n(2)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
            d'4
            e'4
            f'4
        }
        """)


def test_WindowLooper_23():
    random.seed(43271)
    container = abjad.Container(r"c'4 d'4 e'4 f'4 g'4 a'4 b'4 c''4")
    looper = auxjad.WindowLooper(container,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 head_position=(3, 4),
                                 forward_bias=0.5,
                                 )
    notes = looper.output_n(5)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            f'4
            g'4
            a'4
            e'4
            f'4
            g'4
            d'4
            e'4
            f'4
            e'4
            f'4
            g'4
            d'4
            e'4
            f'4
        }
        """)


def test_WindowLooper_24():
    random.seed(19814)
    container = abjad.Container(r"c'4 d'4 e'4 f'4 g'4 a'4 b'4 c''4")
    looper = auxjad.WindowLooper(container,
                                 window_size=(1, 4),
                                 step_size=(1, 4),
                                 max_steps=4,
                                 )
    notes = looper.output_n(4)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 1/4
            c'4
            f'4
            b'4
            c''4
        }
        """)


def test_WindowLooper_25():
    container = abjad.Container(r"c'4. d'8 e'2")
    looper = auxjad.WindowLooper(container)
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4.
            d'8
            e'2
        }
        """)
    looper = auxjad.WindowLooper(container,
                                 boundary_depth=1,
                                 )
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            ~
            c'8
            d'8
            e'2
        }
        """)


def test_WindowLooper_26():
    container = abjad.Container(r"c'4 d'2 e'4")
    looper = auxjad.WindowLooper(container,
                                 window_size=(3, 4),
                                 step_size=(1, 8),
                                 )
    staff = abjad.Staff()
    for window in looper:
        staff.append(window)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'2
            \time 3/4
            c'8
            d'8
            ~
            d'4.
            e'8
            \time 3/4
            d'2
            e'4
            \time 3/4
            d'4.
            e'4
            r8
            \time 3/4
            d'4
            e'4
            r4
            \time 3/4
            d'8
            e'4
            r4.
            \time 3/4
            e'4
            r2
            \time 3/4
            e'8
            r8
            r2
        }
        """)
    auxjad.mutate(staff[:]).remove_repeated_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'2
            c'8
            d'8
            ~
            d'4.
            e'8
            d'2
            e'4
            d'4.
            e'4
            r8
            d'4
            e'4
            r4
            d'8
            e'4
            r4.
            e'4
            r2
            e'8
            r8
            r2
        }
        """)


def test_WindowLooper_27():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.WindowLooper(container)
    assert isinstance(looper(), abjad.Selection)
    tuplet = abjad.Tuplet('3:2', r"c'2 d'2 e'2")
    looper = auxjad.WindowLooper(tuplet)
    assert isinstance(looper(), abjad.Selection)
    voice = abjad.Voice(r"c'4 d'4 e'4 f'4")
    looper = auxjad.WindowLooper(voice)
    assert isinstance(looper(), abjad.Selection)
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    looper = auxjad.WindowLooper(staff)
    assert isinstance(looper(), abjad.Selection)
    score = abjad.Score([abjad.Staff(r"c'4 d'4 e'4 f'4")])
    looper = auxjad.WindowLooper(score)
    assert isinstance(looper(), abjad.Selection)
    voice = abjad.Voice(r"c'4 d'4 e'4 f'4")
    staff = abjad.Staff([voice])
    looper = auxjad.WindowLooper(staff)
    assert isinstance(looper(), abjad.Selection)
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    score = abjad.Score([staff])
    looper = auxjad.WindowLooper(score)
    assert isinstance(looper(), abjad.Selection)

    voice1 = abjad.Voice(r"c'4 d'4 e'4 f'4")
    voice2 = abjad.Voice(r"g2 f2")
    staff = abjad.Staff([voice1, voice2], simultaneous=True)
    with pytest.raises(ValueError):
        auxjad.WindowLooper(staff)

    staff1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
    staff2 = abjad.Staff(r"g2 f2")
    score = abjad.Score([staff1, staff2])
    with pytest.raises(ValueError):
        auxjad.WindowLooper(score)


def test_WindowLooper_28():
    container = abjad.Container(r"c'4.\p( d'8 e'8\f) f'4.\p( ~ f'4 g'1\pp)")
    looper = auxjad.WindowLooper(container, step_size=(1, 4))
    notes = looper.output_n(6)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4.
            \p
            (
            d'8
            e'8
            \f
            )
            f'4.
            \p
            c'8
            (
            d'8
            e'8
            \f
            )
            f'8
            \p
            ~
            f'2
            e'8
            \f
            f'8
            \p
            (
            ~
            f'2
            g'4
            \pp
            )
            f'2
            \p
            (
            g'2
            \pp
            )
            f'4
            \p
            (
            g'2.
            \pp
            )
            g'1
        }
        """)
