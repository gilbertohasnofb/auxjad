import auxjad


def test_LoopWindowByList_01():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.LoopWindowByList(input_list, 3)
    assert looper() == ['A', 'B', 'C']
    assert looper() == ['B', 'C', 'D']
    assert looper.get_current_window() == ['B', 'C', 'D']


def test_LoopWindowByList_02():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.LoopWindowByList(input_list,
                                     3,
                                     step_size=1,
                                     max_steps=2,
                                     repetition_chance=0.25,
                                     initial_head_position=0,
                                     )
    assert looper.elements_per_window == 3
    assert looper.step_size == 1
    assert looper.max_steps == 2
    assert looper.repetition_chance == 0.25
    assert looper.current_head_position == 0


def test_LoopWindowByList_03():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.LoopWindowByList(input_list, 3)
    assert looper.current_head_position == 0
    looper()
    assert looper.current_head_position == 0
    looper()
    assert looper.current_head_position == 1
    looper()
    assert looper.current_head_position == 2


def test_LoopWindowByList_04():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.LoopWindowByList(input_list, 3)
    assert looper.counter == 0
    assert looper.current_head_position == 0
    for _ in range(4):
        looper()
    assert looper.counter == 4
    assert looper.current_head_position == 3
    looper.reset_counter()
    assert looper.current_head_position == 3
    assert looper.counter == 0
    looper.set_head_position(0)
    assert looper.current_head_position == 0
    assert looper.counter == 0


def test_LoopWindowByList_05():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.LoopWindowByList(input_list, 3)
    assert len(looper) == 6


def test_LoopWindowByList_06():
    input_list = ['A', 'B', 'C', 'D']
    looper = auxjad.LoopWindowByList(input_list, 3)
    assert not looper.done
    assert looper.output_all() == ['A', 'B', 'C', 'B', 'C', 'D', 'C', 'D', 'D']
    assert looper.done


def test_LoopWindowByList_07():
    input_list = ['A', 'B', 'C', 'D', 'E', 'F']
    looper = auxjad.LoopWindowByList(input_list, 3)
    assert looper() == ['A', 'B', 'C']
    looper.set_elements_per_window(4)
    assert looper() == ['B', 'C', 'D', 'E']


def test_LoopWindowByList_08():
    input_list = [123, 'foo', (3, 4), 3.14]
    looper = auxjad.LoopWindowByList(input_list, 3)
    assert looper() == [123, 'foo', (3, 4)]


def test_LoopWindowByList_09():
    import abjad
    import copy
    input_list = [
        abjad.Container(r"c'4 d'4 e'4 f'4"),
        abjad.Container(r"fs'1"),
        abjad.Container(r"r2 bf2"),
        abjad.Container(r"c''2. r4"),
    ]
    looper = auxjad.LoopWindowByList(input_list, 3)
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
