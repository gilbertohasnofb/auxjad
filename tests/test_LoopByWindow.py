import abjad
import pytest
import auxjad


def test_LoopByWindow_01():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopByWindow(input_music)
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
            c'8.
            d'16
            ~
            d'4..
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
            c'8.
            d'16
            ~
            d'4..
            e'16
            ~
            e'8.
            f'16
        }
        """)


def test_LoopByWindow_02():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopByWindow(input_music,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
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
            d'2
            e'4
        }
        """)


def test_LoopByWindow_03():
    input_music = abjad.Container(r"c'4 d'2 e'4")
    looper = auxjad.LoopByWindow(input_music,
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
            d'4.
            e'8
            ~
            e'8
            r8
        }
        """)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
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
            d'8
            e'8
            ~
            e'8
            r4.
        }
        """)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
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
            e'8
            r8
            r2
        }
        """)
    with pytest.raises(StopIteration):
        assert looper.__next__()


def test_LoopByWindow_04():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopByWindow(input_music,
                                 window_size=(3, 4),
                                 step_size=(5, 8),
                                 max_steps=2,
                                 repetition_chance=0.25,
                                 forward_bias=0.2,
                                 head_position=(2, 8),
                                 omit_time_signature=False,
                                 )
    assert looper.window_size == abjad.Meter((3, 4))
    assert looper.step_size == abjad.Duration((5, 8))
    assert looper.max_steps == 2
    assert looper.repetition_chance == 0.25
    assert looper.forward_bias == 0.2
    assert looper.head_position == abjad.Duration((1, 4))
    assert not looper.omit_time_signature
    looper.window_size = (5, 4)
    looper.step_size = (1, 4)
    looper.max_steps = 3
    looper.repetition_chance = 0.1
    looper.forward_bias = 0.8
    looper.head_position = 0
    looper.omit_time_signature = True
    assert looper.window_size == abjad.Meter((5, 4))
    assert looper.step_size == abjad.Duration((1, 4))
    assert looper.max_steps == 3
    assert looper.repetition_chance == 0.1
    assert looper.forward_bias == 0.8
    assert looper.head_position == abjad.Duration(0)
    assert looper.omit_time_signature


def test_LoopByWindow_05():
    input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LoopByWindow(input_music,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 )
    music = looper.output_all()
    staff = abjad.Staff(music)
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


def test_LoopByWindow_06():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopByWindow(input_music)
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
            c'8.
            d'16
            ~
            d'4..
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
            c'8
            d'8
            ~
            d'4.
            e'8
            ~
            e'8
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
            d'4.
        }
        """)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            d'4.
        }
        """)


def test_LoopByWindow_07():
    input_music = abjad.Container(r"\times 2/3 {c'8 d'8 e'} d'2.")
    looper = auxjad.LoopByWindow(input_music,
                                 window_size=(3, 4),
                                 step_size=(1, 16))
    staff = abjad.Staff()
    for _ in range(3):
        window = looper()
        staff.append(window)
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


def test_LoopByWindow_08():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopByWindow(input_music, omit_time_signature=True)
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


def test_LoopByWindow_09():
    wrong_type_input = 'foobar'
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    with pytest.raises(TypeError):
        assert auxjad.LoopByWindow(wrong_type_input)
        assert auxjad.LoopByWindow(input_music, window_size=17j)
        assert auxjad.LoopByWindow(input_music, max_steps='foobar')
        assert auxjad.LoopByWindow(input_music, repetition_chance='foobar')
        assert auxjad.LoopByWindow(input_music, head_position=62.3j)
        assert auxjad.LoopByWindow(input_music, omit_time_signature='foobar')
    with pytest.raises(ValueError):
        assert auxjad.LoopByWindow(input_music, window_size=(100, 1))
        assert auxjad.LoopByWindow(input_music, max_steps=-1)
        assert auxjad.LoopByWindow(input_music, repetition_chance=-0.3)
        assert auxjad.LoopByWindow(input_music, repetition_chance=1.4)
        assert auxjad.LoopByWindow(input_music, head_position=(100, 1))


def test_LoopByWindow_10():
    input_music = abjad.Container(r"c'4 e'2 d'2 f'4")
    looper = auxjad.LoopByWindow(input_music,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 )
    music = looper.output_all(tie_identical_pitches=True)
    staff = abjad.Staff(music)
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


def test_LoopByWindow_11():
    input_music = abjad.Container(r"c'4 <e' f' g'>2 r4 f'2.")
    looper = auxjad.LoopByWindow(input_music,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 )
    music = looper.output_all(tie_identical_pitches=True)
    staff = abjad.Staff(music)
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


def test_LoopByWindow_12():
    input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LoopByWindow(input_music,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 )
    music = looper.output_n(2)
    staff = abjad.Staff(music)
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


def test_LoopByWindow_13():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'4")
    looper = auxjad.LoopByWindow(input_music,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 )
    music = looper.output_n(2, tie_identical_pitches=True)
    staff = abjad.Staff(music)
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


def test_LoopByWindow_14():
    input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LoopByWindow(input_music,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 )
    with pytest.raises(RuntimeError):
        looper.output_n(100)


def test_LoopByWindow_15():
    input_music = abjad.Container(r"c'4 d'4 e'4 f'4 g'4 a'4")
    looper = auxjad.LoopByWindow(input_music,
                                 window_size=(3, 4),
                                 step_size=(1, 4),
                                 head_position=(3, 4),
                                 forward_bias=0.0,
                                 )
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            f'4
            g'4
            a'4
        }
        """)
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            e'4
            f'4
            g'4
        }
        """)
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            d'4
            e'4
            f'4
        }
        """)


def test_LoopByWindow_16():
    input_music = abjad.Container(r"c'4 d'4 e'4 f'4 g'4 a'4")
    looper = auxjad.LoopByWindow(input_music,
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


def test_LoopByWindow_17():
    input_music = abjad.Container(r"c'4 d'4 e'4 f'4 g'4 a'4")
    looper = auxjad.LoopByWindow(input_music,
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


def test_LoopByWindow_18():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopByWindow(input_music,
                                 move_window_on_first_call=True,
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
        d'4..
        e'16
        ~
        e'8.
        f'16
    }
    """)


def test_LoopByWindow_19():
    input_music = abjad.Container(r"c'4-.\pp\< d'2--\f e'4->\ppp f'2 ~ f'8")
    looper = auxjad.LoopByWindow(input_music)
    staff = abjad.Staff()
    for _ in range(2):
        music = looper()
        staff.append(music)
    assert format(staff) == abjad.String.normalize(
    r"""
    \new Staff
    {
        \time 4/4
        c'4
        \pp
        - \staccato
        \<
        d'2
        \f
        - \tenuto
        e'4
        \ppp
        - \accent
        c'8.
        \pp
        - \staccato
        \<
        d'16
        \f
        - \tenuto
        ~
        d'4..
        e'16
        \ppp
        - \accent
        ~
        e'8.
        f'16
    }
    """)


def test_LoopByWindow_20():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopByWindow(input_music)
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
            c'8.
            d'16
            ~
            d'4..
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
            e'16
            f'16
            g'8
            ~
            g'2
            ~
            g'8
            a'8
        }
        """)
    looper.head_position = 0
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'16
            d'16
            e'16
            f'16
            g'2.
        }
        """)


def test_LoopByWindow_21():
    input_music = abjad.Container(r"c'1")
    looper = auxjad.LoopByWindow(input_music)
    assert len(looper) == 16
    input_music = abjad.Container(r"c'1")
    looper = auxjad.LoopByWindow(input_music,
                                 step_size=(1, 4),
                                 )
    assert len(looper) == 4
    input_music = abjad.Container(r"c'2..")
    looper = auxjad.LoopByWindow(input_music,
                                 step_size=(1, 4),
                                 window_size=(2, 4),
                                 )
    assert len(looper) == 4
