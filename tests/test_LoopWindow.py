import pytest
import abjad
import auxjad


def test_LoopWindow_01():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopWindow(input_music)
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 4/4
            c'4
            d'2
            e'4
        }
        ''')
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
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
        ''')
    notes = looper.get_current_window()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
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
        ''')


def test_LoopWindow_02():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopWindow(input_music,
                               window_size=(3, 4),
                               step_size=(1, 4),
                               )
    notes = looper()
    staff = abjad.Staff(notes)
    abjad.f(staff)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 3/4
            c'4
            d'2
        }
        ''')
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            d'2
            e'4
        }
        ''')


def test_LoopWindow_03():
    input_music = abjad.Container(r"c'4 d'2 e'4")
    looper = auxjad.LoopWindow(input_music,
                               window_size=(3, 4),
                               step_size=(1, 8),
                               )
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 3/4
            c'4
            d'2
        }
        ''')
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            c'8
            d'8
            ~
            d'4.
            e'8
        }
        ''')
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            d'2
            e'4
        }
        ''')
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            d'4.
            e'8
            ~
            e'8
            r8
        }
        ''')
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            d'4
            e'4
            r4
        }
        ''')
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            d'8
            e'8
            ~
            e'8
            r4.
        }
        ''')
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            e'4
            r2
        }
        ''')
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            e'8
            r8
            r2
        }
        ''')
    with pytest.raises(StopIteration):
        looper.__next__()


def test_LoopWindow_04():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopWindow(input_music,
                               window_size=(3, 4),
                               step_size=(5, 8),
                               max_steps=2,
                               repetition_chance=0.25,
                               head_position=(2, 8),
                               )
    assert looper.window_size == abjad.Meter((3, 4))
    assert looper.step_size == abjad.Duration((5, 8))
    assert looper.max_steps == 2
    assert looper.repetition_chance == 0.25
    assert looper.head_position == abjad.Duration((1, 4))
    looper.set_window_size((5, 4))
    looper.set_step_size((1, 4))
    looper.set_max_steps(3)
    looper.set_repetition_chance(0.1)
    looper.set_head_position((0, 1))
    assert looper.window_size == abjad.Meter((5, 4))
    assert looper.step_size == abjad.Duration((1, 4))
    assert looper.max_steps == 3
    assert looper.repetition_chance == 0.1
    assert looper.head_position == abjad.Duration((0, 1))


def test_LoopWindow_05():
    input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LoopWindow(input_music,
                               window_size=(3, 4),
                               step_size=(1, 4),
                               )
    music = looper.output_all()
    staff = abjad.Staff(music)
    assert format(staff) == abjad.String.normalize(
        r'''
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
        ''')


def test_LoopWindow_06():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopWindow(input_music)
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 4/4
            c'4
            d'2
            e'4
        }
        ''')
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
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
        ''')
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
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
        ''')
    looper.set_window_size((3, 8))
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 3/8
            c'16
            d'16
            ~
            d'4
        }
        ''')
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            d'4.
        }
        ''')
    notes = looper.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            d'4.
        }
        ''')


def test_LoopWindow_07():
    input_music = abjad.Container(r"\times 2/3 {c'8 d'8 e'} d'2.")
    looper = auxjad.LoopWindow(input_music,
                               window_size=(3, 4),
                               step_size=(1, 16))
    staff = abjad.Staff()
    for _ in range(3):
        window = looper()
        staff.append(window)
    assert format(staff) == abjad.String.normalize(
        r'''
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
        ''')
