import random

import abjad
import pytest

import auxjad


def test_ListLooper_01():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.ListLooper(input_list, window_size=3)
    assert format(looper) == "['A', 'B', 'C', 'D', 'E', 'F']"
    assert looper() == ['A', 'B', 'C']
    assert looper() == ['B', 'C', 'D']
    assert looper.current_window == ['B', 'C', 'D']


def test_ListLooper_02():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.ListLooper(input_list,
                               window_size=3,
                               step_size=1,
                               max_steps=2,
                               repetition_chance=0.25,
                               forward_bias=0.2,
                               head_position=0,
                               process_on_first_call=True,
                               )
    assert looper.window_size == 3
    assert looper.step_size == 1
    assert looper.max_steps == 2
    assert looper.repetition_chance == 0.25
    assert looper.forward_bias == 0.2
    assert looper.head_position == 0
    assert looper.process_on_first_call
    looper.window_size = 2
    looper.step_size = 2
    looper.max_steps = 3
    looper.repetition_chance = 0.1
    looper.forward_bias = 0.8
    looper.head_position = 2
    looper.process_on_first_call = False
    assert looper.window_size == 2
    assert looper.step_size == 2
    assert looper.max_steps == 3
    assert looper.repetition_chance == 0.1
    assert looper.forward_bias == 0.8
    assert looper.head_position == 2
    assert not looper.process_on_first_call


def test_ListLooper_03():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.ListLooper(input_list, window_size=3)
    assert looper.head_position == 0
    looper()
    assert looper.head_position == 0
    looper()
    assert looper.head_position == 1
    looper()
    assert looper.head_position == 2


def test_ListLooper_04():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.ListLooper(input_list, window_size=3)
    assert len(looper) == 6


def test_ListLooper_05():
    input_list = ['A', 'B', 'C', 'D']
    looper = auxjad.ListLooper(input_list, window_size=3)
    assert looper.output_all() == ['A', 'B', 'C', 'B', 'C', 'D', 'C', 'D', 'D']


def test_ListLooper_06():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.ListLooper(input_list, window_size=3)
    assert looper() == ['A', 'B', 'C']
    looper.window_size = 4
    assert looper() == ['B', 'C', 'D', 'E']


def test_ListLooper_07():
    input_list = [123, 'foo', (3, 4), 3.14]
    looper = auxjad.ListLooper(input_list, window_size=3)
    assert looper() == [123, 'foo', (3, 4)]


def test_ListLooper_08():
    input_list = [
        abjad.Container(r"c'4 d'4 e'4 f'4"),
        abjad.Container(r"fs'1"),
        abjad.Container(r"r2 bf2"),
        abjad.Container(r"c''2. r4"),
    ]
    looper = auxjad.ListLooper(input_list, window_size=3)
    staff = abjad.Staff()
    for element in looper.output_all():
        staff.append(element)
    assert format(staff) == abjad.String.normalize(
        r"""
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
        """)


def test_ListLooper_09():
    input_list = ['A', 'B', 'C', 'D']
    looper = auxjad.ListLooper(input_list, window_size=3)
    assert looper.__next__() == ['A', 'B', 'C']
    assert looper.__next__() == ['B', 'C', 'D']
    assert looper.__next__() == ['C', 'D']
    assert looper.__next__() == ['D']
    with pytest.raises(StopIteration):
        assert looper.__next__()


def test_ListLooper_10():
    wrong_type_input = 'foo'
    input_list = ['A', 'B', 'C', 'D']
    with pytest.raises(TypeError):
        assert auxjad.ListLooper(wrong_type_input, window_size=3)
        assert auxjad.ListLooper(input_list, window_size='foobar')
        assert auxjad.ListLooper(input_list,
                                 window_size=3,
                                 step_size='foobar',
                                 )
        assert auxjad.ListLooper(input_list,
                                 window_size=3,
                                 max_steps='foobar',
                                 )
        assert auxjad.ListLooper(input_list,
                                 window_size=3,
                                 repetition_chance='foobar',
                                 )
        assert auxjad.ListLooper(input_list,
                                 window_size=3,
                                 head_position='foobar',
                                 )
    with pytest.raises(ValueError):
        assert auxjad.ListLooper(input_list, window_size=-1)
        assert auxjad.ListLooper(input_list,
                                 window_size=3,
                                 step_size=-1)
        assert auxjad.ListLooper(input_list,
                                 window_size=3,
                                 step_size=100)
        assert auxjad.ListLooper(input_list,
                                 window_size=3,
                                 max_steps=-1)
        assert auxjad.ListLooper(input_list,
                                 window_size=3,
                                 repetition_chance=-0.3)
        assert auxjad.ListLooper(input_list,
                                 window_size=3,
                                 repetition_chance=1.4)
        assert auxjad.ListLooper(input_list,
                                 window_size=3,
                                 head_position=-1)
        assert auxjad.ListLooper(input_list,
                                 window_size=3,
                                 head_position=100)


def test_ListLooper_11():
    input_list = ['A', 'B', 'C', 'D']
    looper = auxjad.ListLooper(input_list, window_size=3)
    assert looper.output_n(2) == ['A', 'B', 'C', 'B', 'C', 'D']


def test_ListLooper_12():
    input_list = ['A', 'B', 'C', 'D']
    looper = auxjad.ListLooper(input_list, window_size=3)
    with pytest.raises(RuntimeError):
        looper.output_n(100)


def test_ListLooper_13():
    input_list = ['A', 'B', 'C', 'D']
    looper = auxjad.ListLooper(input_list,
                               window_size=2,
                               head_position=2,
                               forward_bias=0.0,
                               )
    assert looper.output_all() == ['C', 'D', 'B', 'C', 'A', 'B']


def test_ListLooper_14():
    input_list = ['A', 'B', 'C', 'D']
    looper = auxjad.ListLooper(input_list,
                               window_size=2,
                               head_position=0,
                               forward_bias=0.0,
                               )
    assert looper.output_all() == ['A', 'B']


def test_ListLooper_15():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.ListLooper(input_list,
                               window_size=3,
                               process_on_first_call=True,
                               )
    assert looper() == ['B', 'C', 'D']


def test_ListLooper_16():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.ListLooper(input_list,
                               window_size=3,
                               )
    assert looper.contents == ['A', 'B', 'C', 'D', 'E', 'F']
    assert looper() == ['A', 'B', 'C']
    assert looper() == ['B', 'C', 'D']
    looper.contents = [0, 1, 2, 3, 4]
    assert looper.contents == [0, 1, 2, 3, 4]
    assert looper() == [1, 2, 3]
    looper.head_position = 0
    assert looper() == [0, 1, 2]


def test_ListLooper_17():
    random.seed(85162)
    input_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    looper = auxjad.ListLooper(input_list,
                               window_size=2,
                               head_position=4,
                               forward_bias=0.5,
                               )
    assert looper.output_n(4) == ['E', 'F', 'D', 'E', 'C', 'D', 'B', 'C']


def test_ListLooper_18():
    random.seed(70013)
    input_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    looper = auxjad.ListLooper(input_list,
                               window_size=2,
                               head_position=2,
                               max_steps=4,
                               )
    assert looper.output_n(4) == ['C', 'D', 'D', 'E', 'E', 'F', 'H']
