import abjad
import pytest
import auxjad


def test_LoopWindowByList_01():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.LoopWindowByList(input_list, window_size=3)
    assert looper() == ['A', 'B', 'C']
    assert looper() == ['B', 'C', 'D']
    assert looper.get_current_window() == ['B', 'C', 'D']


def test_LoopWindowByList_02():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.LoopWindowByList(input_list,
                                     window_size=3,
                                     step_size=1,
                                     max_steps=2,
                                     repetition_chance=0.25,
                                     forward_bias=0.2,
                                     head_position=0,
                                     )
    assert looper.window_size == 3
    assert looper.step_size == 1
    assert looper.max_steps == 2
    assert looper.repetition_chance == 0.25
    assert looper.forward_bias == 0.2
    assert looper.head_position == 0
    looper.set_window_size(2)
    looper.set_step_size(2)
    looper.set_max_steps(3)
    looper.set_repetition_chance(0.1)
    looper.set_forward_bias(0.8)
    looper.set_head_position(2)
    assert looper.window_size == 2
    assert looper.step_size == 2
    assert looper.max_steps == 3
    assert looper.repetition_chance == 0.1
    assert looper.forward_bias == 0.8
    assert looper.head_position == 2


def test_LoopWindowByList_03():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.LoopWindowByList(input_list, window_size=3)
    assert looper.head_position == 0
    looper()
    assert looper.head_position == 0
    looper()
    assert looper.head_position == 1
    looper()
    assert looper.head_position == 2


def test_LoopWindowByList_04():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.LoopWindowByList(input_list, window_size=3)
    assert len(looper) == 6


def test_LoopWindowByList_05():
    input_list = ['A', 'B', 'C', 'D']
    looper = auxjad.LoopWindowByList(input_list, window_size=3)
    assert looper.output_all() == ['A', 'B', 'C', 'B', 'C', 'D', 'C', 'D', 'D']


def test_LoopWindowByList_06():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.LoopWindowByList(input_list, window_size=3)
    assert looper() == ['A', 'B', 'C']
    looper.set_window_size(4)
    assert looper() == ['B', 'C', 'D', 'E']


def test_LoopWindowByList_07():
    input_list = [123, 'foo', (3, 4), 3.14]
    looper = auxjad.LoopWindowByList(input_list, window_size=3)
    assert looper() == [123, 'foo', (3, 4)]


def test_LoopWindowByList_08():
    input_list = [
        abjad.Container(r"c'4 d'4 e'4 f'4"),
        abjad.Container(r"fs'1"),
        abjad.Container(r"r2 bf2"),
        abjad.Container(r"c''2. r4"),
    ]
    looper = auxjad.LoopWindowByList(input_list, window_size=3)
    staff = abjad.Staff()
    for element in looper.output_all():
        staff.append(element)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            {
                c'4
                d'4
                e'4
                f'4
            }
            {
                fs'1
            }
            {
                r2
                bf2
            }
            {
                fs'1
            }
            {
                r2
                bf2
            }
            {
                c''2.
                r4
            }
            {
                r2
                bf2
            }
            {
                c''2.
                r4
            }
            {
                c''2.
                r4
            }
        }
        ''')


def test_LoopWindowByList_09():
    input_list = ['A', 'B', 'C', 'D']
    looper = auxjad.LoopWindowByList(input_list, window_size=3)
    assert looper.__next__() == ['A', 'B', 'C']
    assert looper.__next__() == ['B', 'C', 'D']
    assert looper.__next__() == ['C', 'D']
    assert looper.__next__() == ['D']
    with pytest.raises(StopIteration):
        assert looper.__next__()



def test_LoopWindowByList_10():
    wrong_type_input = 'foo'
    input_list = ['A', 'B', 'C', 'D']
    with pytest.raises(TypeError):
        assert auxjad.LoopWindowByList(wrong_type_input, window_size=3)
        assert auxjad.LoopWindowByList(input_list, window_size='foobar')
        assert auxjad.LoopWindowByList(input_list,
                                       window_size=3,
                                       step_size='foobar',
                                       )
        assert auxjad.LoopWindowByList(input_list,
                                       window_size=3,
                                       max_steps='foobar',
                                       )
        assert auxjad.LoopWindowByList(input_list,
                                       window_size=3,
                                       repetition_chance='foobar',
                                       )
        assert auxjad.LoopWindowByList(input_list,
                                       window_size=3,
                                       head_position='foobar',
                                       )
    with pytest.raises(ValueError):
        assert auxjad.LoopWindowByList(input_list, window_size=-1)
        assert auxjad.LoopWindowByList(input_list,
                                       window_size=3,
                                       step_size=-1)
        assert auxjad.LoopWindowByList(input_list,
                                       window_size=3,
                                       step_size=100)
        assert auxjad.LoopWindowByList(input_list,
                                       window_size=3,
                                       max_steps=-1)
        assert auxjad.LoopWindowByList(input_list,
                                       window_size=3,
                                       repetition_chance=-0.3)
        assert auxjad.LoopWindowByList(input_list,
                                       window_size=3,
                                       repetition_chance=1.4)
        assert auxjad.LoopWindowByList(input_list,
                                       window_size=3,
                                       head_position=-1)
        assert auxjad.LoopWindowByList(input_list,
                                       window_size=3,
                                       head_position=100)


def test_LoopWindowByList_11():
    input_list = ['A', 'B', 'C', 'D']
    looper = auxjad.LoopWindowByList(input_list, window_size=3)
    assert looper.output_n(2) == ['A', 'B', 'C', 'B', 'C', 'D']


def test_LoopWindowByList_12():
    input_list = ['A', 'B', 'C', 'D']
    looper = auxjad.LoopWindowByList(input_list, window_size=3)
    with pytest.raises(RuntimeError):
        looper.output_n(100)


def test_LoopWindowByList_13():
    input_list = ['A', 'B', 'C', 'D']
    looper = auxjad.LoopWindowByList(input_list,
                                     window_size=2,
                                     head_position=2,
                                     forward_bias=0.0,
                                     )
    assert looper.output_all() == ['C', 'D', 'B', 'C', 'A', 'B']


def test_LoopWindowByList_14():
    input_list = ['A', 'B', 'C', 'D']
    looper = auxjad.LoopWindowByList(input_list,
                                     window_size=2,
                                     head_position=0,
                                     forward_bias=0.0,
                                     )
    assert looper.output_all() == ['A', 'B']
