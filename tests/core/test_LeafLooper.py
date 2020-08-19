import random

import abjad
import pytest

import auxjad


def test_LeafLooper_01():
    container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LeafLooper(container, window_size=3)
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
            \time 11/8
            d'2
            e'8
            ~
            e'8
            f'8
            ~
            f'2
        }
        """)
    notes = looper.current_window
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 11/8
            d'2
            e'8
            ~
            e'8
            f'8
            ~
            f'2
        }
        """)


def test_LeafLooper_02():
    container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LeafLooper(container,
                               window_size=3,
                               step_size=1,
                               max_steps=2,
                               repetition_chance=0.25,
                               forward_bias=0.2,
                               head_position=0,
                               omit_time_signatures=False,
                               process_on_first_call=True,
                               )
    assert looper.window_size == 3
    assert looper.step_size == 1
    assert looper.max_steps == 2
    assert looper.repetition_chance == 0.25
    assert looper.forward_bias == 0.2
    assert looper.head_position == 0
    assert not looper.omit_time_signatures
    assert looper.process_on_first_call
    looper.window_size = 2
    looper.step_size = 2
    looper.max_steps = 3
    looper.repetition_chance = 0.1
    looper.forward_bias = 0.8
    looper.head_position = 2
    looper.omit_time_signatures = True
    looper.process_on_first_call = False
    assert looper.window_size == 2
    assert looper.step_size == 2
    assert looper.max_steps == 3
    assert looper.repetition_chance == 0.1
    assert looper.forward_bias == 0.8
    assert looper.head_position == 2
    assert looper.omit_time_signatures
    assert not looper.process_on_first_call


def test_LeafLooper_03():
    container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LeafLooper(container, window_size=3)
    assert looper.head_position == 0
    looper()
    assert looper.head_position == 0
    looper()
    assert looper.head_position == 1
    looper()
    assert looper.head_position == 2


def test_LeafLooper_04():
    container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LeafLooper(container, window_size=3)
    assert len(looper) == 5


def test_LeafLooper_05():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LeafLooper(container, window_size=2)
    notes = looper.output_all()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            c'4
            d'4
            d'4
            e'4
            e'4
            f'4
            \time 1/4
            f'4
        }
        """)


def test_LeafLooper_06():
    container = abjad.Container(r"c'4 d'4 e'8 f'4 g'2")
    looper = auxjad.LeafLooper(container, window_size=3)
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 5/8
            c'4
            d'8
            ~
            d'8
            e'8
        }
        """)
    looper.window_size = 4
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 9/8
            d'4
            e'8
            f'4
            g'2
        }
        """)


def test_LeafLooper_07():
    container = abjad.Container(r"c'4 d'16 e'8 f'2 g'8")
    looper = auxjad.LeafLooper(container,
                               window_size=3,
                               head_position=2,
                               )
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            e'8
            f'8
            ~
            f'4.
            g'8
        }
        """)


def test_LeafLooper_08():
    container = abjad.Container(r"c'4 d'8 \times 2/3 {a4 g2}")
    looper = auxjad.LeafLooper(container, window_size=2)
    notes = looper.output_all()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            #(ly:expect-warning "strange time signature found")
            \time 7/24
            d'8
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                a4
            }
            \times 2/3 {
                \time 2/4
                a4
                g2
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                #(ly:expect-warning "strange time signature found")
                \time 2/6
                g2
            }
        }
        """)


def test_LeafLooper_09():
    container = abjad.Container(r"c'4 d'2 e'8")
    looper = auxjad.LeafLooper(container, window_size=2)
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
            \time 5/8
            d'2
            e'8
        }
        """)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 1/8
            e'8
        }
        """)
    with pytest.raises(StopIteration):
        assert looper.__next__()


def test_LeafLooper_10():
    container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LeafLooper(container,
                               window_size=3,
                               omit_time_signatures=True,
                               )
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


def test_LeafLooper_11():
    wrong_type_input = 'foo'
    container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    with pytest.raises(TypeError):
        assert auxjad.LeafLooper(wrong_type_input, window_size=3)
        assert auxjad.LeafLooper(container, window_size='foobar')
        assert auxjad.LeafLooper(container,
                                 window_size=3,
                                 step_size='foobar',
                                 )
        assert auxjad.LeafLooper(container,
                                 window_size=3,
                                 max_steps='foobar',
                                 )
        assert auxjad.LeafLooper(container,
                                 window_size=3,
                                 repetition_chance='foobar',
                                 )
        assert auxjad.LeafLooper(container,
                                 window_size=3,
                                 head_position='foobar',
                                 )
        assert auxjad.LeafLooper(container,
                                 window_size=3,
                                 omit_time_signatures='foobar',
                                 )
    with pytest.raises(ValueError):
        assert auxjad.LeafLooper(container, window_size=100)
        assert auxjad.LeafLooper(container,
                                 window_size=3,
                                 step_size=-1,
                                 )
        assert auxjad.LeafLooper(container,
                                 window_size=3,
                                 step_size=100,
                                 )
        assert auxjad.LeafLooper(container,
                                 window_size=3,
                                 max_steps=-1,
                                 )
        assert auxjad.LeafLooper(container,
                                 window_size=3,
                                 repetition_chance=-0.3,
                                 )
        assert auxjad.LeafLooper(container,
                                 window_size=3,
                                 repetition_chance=1.4,
                                 )
        assert auxjad.LeafLooper(container,
                                 window_size=3,
                                 head_position=-1,
                                 )
        assert auxjad.LeafLooper(container,
                                 window_size=3,
                                 head_position=100,
                                 )


def test_LeafLooper_12():
    container = abjad.Container(r"c'4 d'2 r8 d'4 <e' g'>8 r4 f'2. <e' g'>16")
    looper = auxjad.LeafLooper(container,
                               window_size=4,
                               disable_rewrite_meter=True,
                               )
    notes = looper.output_all(tie_identical_pitches=True)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 9/8
            c'4
            d'2
            r8
            d'4
            ~
            \time 4/4
            d'2
            r8
            d'4
            <e' g'>8
            \time 3/4
            r8
            d'4
            <e' g'>8
            r4
            \time 11/8
            d'4
            <e' g'>8
            r4
            f'2.
            \time 19/16
            <e' g'>8
            r4
            f'2.
            <e' g'>16
            \time 17/16
            r4
            f'2.
            <e' g'>16
            \time 13/16
            f'2.
            <e' g'>16
            ~
            \time 1/16
            <e' g'>16
        }
        """)


def test_LeafLooper_13():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LeafLooper(container, window_size=2)
    notes = looper.output_n(2)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            c'4
            d'4
            d'4
            e'4
        }
        """)


def test_LeafLooper_14():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LeafLooper(container, window_size=2)
    notes = looper.output_n(2, tie_identical_pitches=True)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            c'4
            d'4
            ~
            d'4
            e'4
        }
        """)


def test_LeafLooper_15():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LeafLooper(container, window_size=2)
    with pytest.raises(RuntimeError):
        looper.output_n(100)


def test_LeafLooper_16():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LeafLooper(container,
                               window_size=2,
                               head_position=2,
                               forward_bias=0.0,
                               )
    notes = looper.output_all()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            e'4
            f'4
            d'4
            e'4
            c'4
            d'4
        }
        """)


def test_LeafLooper_17():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LeafLooper(container,
                               window_size=2,
                               head_position=0,
                               forward_bias=0.0,
                               )
    notes = looper.output_all()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            c'4
            d'4
        }
        """)


def test_LeafLooper_18():
    container = abjad.Container(r"c'4 d'8 e'2 f'8 g'4")
    looper = auxjad.LeafLooper(container,
                               window_size=3,
                               process_on_first_call=True,
                               )
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            d'8
            e'8
            ~
            e'4.
            f'8
        }
        """)


def test_LeafLooper_19():
    container = abjad.Container(r"c'4 d'4 e'4 f'4 g'4 a'4")
    looper = auxjad.LeafLooper(container,
                               window_size=3,
                               )
    notes = looper()
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
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            d'4
            e'4
            f'4
        }
        """)
    looper.contents = abjad.Container(r"cs'''4 ds'''4 es'''4 fs'''4")
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            ds'''4
            es'''4
            fs'''4
        }
        """)
    looper.head_position = 0
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            cs'''4
            ds'''4
            es'''4
        }
        """)


def test_LeafLooper_20():
    random.seed(15231)
    container = abjad.Container(r"c'4 d'4 e'4 f'4 g'4 a'4 b'4 c''4")
    looper = auxjad.LeafLooper(container,
                               window_size=3,
                               head_position=3,
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


def test_LeafLooper_21():
    random.seed(55126)
    container = abjad.Container(r"c'4 d'4 e'4 f'4 g'4 a'4 b'4 c''4 d''4")
    looper = auxjad.LeafLooper(container,
                               window_size=2,
                               max_steps=4,
                               )
    notes = looper.output_n(4)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            c'4
            d'4
            g'4
            a'4
            a'4
            b'4
            c''4
            d''4
        }
        """)


def test_LeafLooper_22():
    container = abjad.Container(r"c'4 d'2 e'8 f'2")
    looper = auxjad.LeafLooper(container,
                               window_size=2,
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
            \time 5/8
            d'2
            e'8
            \time 5/8
            e'8
            f'2
            \time 2/4
            f'2
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
            \time 5/8
            d'2
            e'8
            e'8
            f'2
            \time 2/4
            f'2
        }
        """)


def test_LeafLooper_23():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LeafLooper(container, window_size=2)
    assert isinstance(looper(), abjad.Selection)
    tuplet = abjad.Tuplet('3:2', r"c'2 d'2 e'2")
    looper = auxjad.LeafLooper(tuplet, window_size=2)
    assert isinstance(looper(), abjad.Selection)
    voice = abjad.Voice(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LeafLooper(voice, window_size=2)
    assert isinstance(looper(), abjad.Selection)
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LeafLooper(staff, window_size=2)
    assert isinstance(looper(), abjad.Selection)
    score = abjad.Score([abjad.Staff(r"c'4 d'4 e'4 f'4")])
    looper = auxjad.LeafLooper(score, window_size=2)
    assert isinstance(looper(), abjad.Selection)
    voice = abjad.Voice(r"c'4 d'4 e'4 f'4")
    staff = abjad.Staff([voice])
    looper = auxjad.LeafLooper(staff, window_size=2)
    assert isinstance(looper(), abjad.Selection)
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    score = abjad.Score([staff])
    looper = auxjad.LeafLooper(score, window_size=2)
    assert isinstance(looper(), abjad.Selection)

    voice1 = abjad.Voice(r"c'4 d'4 e'4 f'4")
    voice2 = abjad.Voice(r"g2 f2")
    staff = abjad.Staff([voice1, voice2], simultaneous=True)
    with pytest.raises(ValueError):
        auxjad.LeafLooper(staff, window_size=2)

    staff1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
    staff2 = abjad.Staff(r"g2 f2")
    score = abjad.Score([staff1, staff2])
    with pytest.raises(ValueError):
        auxjad.LeafLooper(score, window_size=2)


def test_LeafLooper_24():
    container = abjad.Container(r"c'4\p( d'2 e'4\f) f'2( ~ f'8 g'4 a'1\pp)")
    looper = auxjad.LeafLooper(container,
                               window_size=3,
                               disable_rewrite_meter=True,
                               )
    notes = looper.output_n(5)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \p
            (
            d'2
            e'4
            \f
            )
            \time 11/8
            d'2
            \p
            (
            e'4
            \f
            )
            f'2
            ~
            f'8
            \time 9/8
            e'4
            f'2
            (
            ~
            f'8
            g'4
            )
            \time 15/8
            f'2
            (
            ~
            f'8
            g'4
            a'1
            \pp
            )
            \time 5/4
            g'4
            \f
            (
            a'1
            \pp
            )
        }
        """)


def test_LeafLooper_25():
    container = abjad.Container(r"c'16 d'4 e'8. f'4 g'16")
    looper = auxjad.LeafLooper(container,
                               window_size=3,
                               )
    notes = looper.output_n(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            c'16
            d'8.
            ~
            d'16
            e'8.
            \time 11/16
            d'4
            e'8.
            f'4
            \time 2/4
            e'8.
            f'16
            ~
            f'8.
            g'16
        }
        """)
    looper = auxjad.LeafLooper(container,
                               window_size=3,
                               disable_rewrite_meter=True,
                               )
    notes = looper.output_n(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            c'16
            d'4
            e'8.
            \time 11/16
            d'4
            e'8.
            f'4
            \time 2/4
            e'8.
            f'4
            g'16
        }
        """)
