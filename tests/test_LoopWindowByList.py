import pytest
import auxjad


def test_LoopWindowByList_01():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.LoopWindowByList(input_list, elements_per_window=3)
    assert looper() == ['A', 'B', 'C']
    assert looper() == ['B', 'C', 'D']
    assert looper.get_current_window() == ['B', 'C', 'D']


def test_LoopWindowByList_02():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.LoopWindowByList(input_list,
                                     elements_per_window=3,
                                     step_size=1,
                                     max_steps=2,
                                     repetition_chance=0.25,
                                     head_position=0,
                                     )
    assert looper.elements_per_window == 3
    assert looper.step_size == 1
    assert looper.max_steps == 2
    assert looper.repetition_chance == 0.25
    assert looper.head_position == 0
    looper.set_elements_per_window(2)
    looper.set_step_size(2)
    looper.set_max_steps(3)
    looper.set_repetition_chance(0.1)
    looper.set_head_position(2)
    assert looper.elements_per_window == 2
    assert looper.step_size == 2
    assert looper.max_steps == 3
    assert looper.repetition_chance == 0.1
    assert looper.head_position == 2


def test_LoopWindowByList_03():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.LoopWindowByList(input_list, elements_per_window=3)
    assert looper.head_position == 0
    looper()
    assert looper.head_position == 0
    looper()
    assert looper.head_position == 1
    looper()
    assert looper.head_position == 2


def test_LoopWindowByList_04():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.LoopWindowByList(input_list, elements_per_window=3)
    assert len(looper) == 6


def test_LoopWindowByList_05():
    input_list = ['A', 'B', 'C', 'D']
    looper = auxjad.LoopWindowByList(input_list, elements_per_window=3)
    assert looper.output_all() == ['A', 'B', 'C', 'B', 'C', 'D', 'C', 'D', 'D']


def test_LoopWindowByList_06():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.LoopWindowByList(input_list, elements_per_window=3)
    assert looper() == ['A', 'B', 'C']
    looper.set_elements_per_window(4)
    assert looper() == ['B', 'C', 'D', 'E']


def test_LoopWindowByList_07():
    input_list = [123, 'foo', (3, 4), 3.14]
    looper = auxjad.LoopWindowByList(input_list, elements_per_window=3)
    assert looper() == [123, 'foo', (3, 4)]


def test_LoopWindowByList_08():
    import abjad
    import copy
    input_list = [
        abjad.Container(r"c'4 d'4 e'4 f'4"),
        abjad.Container(r"fs'1"),
        abjad.Container(r"r2 bf2"),
        abjad.Container(r"c''2. r4"),
    ]
    looper = auxjad.LoopWindowByList(input_list, elements_per_window=3)
    staff = abjad.Staff()
    for element in looper.output_all():
        staff.append(copy.deepcopy(element))
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
    looper = auxjad.LoopWindowByList(input_list, elements_per_window=3)
    assert looper.__next__() == ['A', 'B', 'C']
    assert looper.__next__() == ['B', 'C', 'D']
    assert looper.__next__() == ['C', 'D']
    assert looper.__next__() == ['D']
    with pytest.raises(StopIteration):
        looper.__next__()
