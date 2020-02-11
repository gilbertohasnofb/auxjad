import abjad
import auxjad


def test_LoopWindowByElements_01():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopWindowByElements(input_music, 3)
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
            \time 11/8
            d'2
            e'4
            f'2
            ~
            f'8
        }
        ''')
    notes = looper.get_current_window()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 11/8
            d'2
            e'4
            f'2
            ~
            f'8
        }
        ''')


def test_LoopWindowByElements_02():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopWindowByElements(input_music,
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


def test_LoopWindowByElements_03():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopWindowByElements(input_music, 3)
    assert looper.current_head_position == 0
    looper()
    assert looper.current_head_position == 0
    looper()
    assert looper.current_head_position == 1
    looper()
    assert looper.current_head_position == 2


def test_LoopWindowByElements_04():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopWindowByElements(input_music, 3)
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


def test_LoopWindowByElements_05():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopWindowByElements(input_music, 3)
    assert len(looper) == 5


def test_LoopWindowByElements_06():
    input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LoopWindowByElements(input_music, 2)
    assert looper.done == False
    notes = looper.output_all()
    assert looper.done == True
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 2/4
            c'4
            d'4
            \time 2/4
            d'4
            e'4
            \time 2/4
            e'4
            f'4
            \time 1/4
            f'4
        }
        ''')


def test_LoopWindowByElements_07():
    input_music = abjad.Container(r"c'4 d'8 \times 2/3 {a4 g2}")
    looper = auxjad.LoopWindowByElements(input_music, 2)
    notes = looper.output_all()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r'''
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
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                \time 2/4
                a4
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                g2
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                #(ly:expect-warning "strange time signature found")
                \time 2/6
                g2
            }
        }
        ''')
