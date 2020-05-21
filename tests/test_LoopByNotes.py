import abjad
import pytest
import auxjad


def test_LoopByNotes_01():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopByNotes(input_music, window_size=3)
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
            e'4
            f'2
            ~
            f'8
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
            e'4
            f'2
            ~
            f'8
        }
        """)


def test_LoopByNotes_02():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopByNotes(input_music,
                                window_size=3,
                                step_size=1,
                                max_steps=2,
                                repetition_chance=0.25,
                                forward_bias=0.2,
                                head_position=0,
                                omit_all_time_signatures=False,
                                force_identical_time_signatures=False,
                                )
    assert looper.window_size == 3
    assert looper.step_size == 1
    assert looper.max_steps == 2
    assert looper.repetition_chance == 0.25
    assert looper.forward_bias == 0.2
    assert looper.head_position == 0
    assert not looper.omit_all_time_signatures
    assert not looper.force_identical_time_signatures
    looper.window_size = 2
    looper.step_size = 2
    looper.max_steps = 3
    looper.repetition_chance = 0.1
    looper.forward_bias = 0.8
    looper.head_position = 2
    looper.omit_all_time_signatures = True
    looper.force_identical_time_signatures = True
    assert looper.window_size == 2
    assert looper.step_size == 2
    assert looper.max_steps == 3
    assert looper.repetition_chance == 0.1
    assert looper.forward_bias == 0.8
    assert looper.head_position == 2
    assert looper.omit_all_time_signatures
    assert looper.force_identical_time_signatures


def test_LoopByNotes_03():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopByNotes(input_music, window_size=3)
    assert looper.head_position == 0
    looper()
    assert looper.head_position == 0
    looper()
    assert looper.head_position == 1
    looper()
    assert looper.head_position == 2


def test_LoopByNotes_04():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopByNotes(input_music, window_size=3)
    assert len(looper) == 5


def test_LoopByNotes_05():
    input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LoopByNotes(input_music, window_size=2)
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


def test_LoopByNotes_06():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopByNotes(input_music, window_size=3)
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
    looper.window_size = 4
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 19/8
            d'2
            e'4
            f'2
            ~
            f'8
            g'1
        }
        """)


def test_LoopByNotes_07():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopByNotes(input_music,
                                window_size=3,
                                head_position=2,
                                )
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 15/8
            e'4
            f'2
            ~
            f'8
            g'1
        }
        """)


def test_LoopByNotes_08():
    input_music = abjad.Container(r"c'4 d'8 \times 2/3 {a4 g2}")
    looper = auxjad.LoopByNotes(input_music, window_size=2)
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
        """)


def test_LoopByNotes_09():
    input_music = abjad.Container(r"c'4 d'2 e'4")
    looper = auxjad.LoopByNotes(input_music, window_size=2)
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
            \time 1/4
            e'4
        }
        """)
    with pytest.raises(StopIteration):
        assert looper.__next__()


def test_LoopByNotes_10():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopByNotes(input_music,
                                window_size=3,
                                omit_all_time_signatures=True,
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


def test_LoopByNotes_11():
    wrong_type_input = 'foo'
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    with pytest.raises(TypeError):
        assert auxjad.LoopByNotes(wrong_type_input, window_size=3)
        assert auxjad.LoopByNotes(input_music, window_size='foobar')
        assert auxjad.LoopByNotes(input_music,
                                  window_size=3,
                                  step_size='foobar',
                                  )
        assert auxjad.LoopByNotes(input_music,
                                  window_size=3,
                                  max_steps='foobar',
                                  )
        assert auxjad.LoopByNotes(input_music,
                                  window_size=3,
                                  repetition_chance='foobar',
                                  )
        assert auxjad.LoopByNotes(input_music,
                                  window_size=3,
                                  head_position='foobar',
                                  )
        assert auxjad.LoopByNotes(input_music,
                                  window_size=3,
                                  omit_all_time_signatures='foobar',
                                  )
    with pytest.raises(ValueError):
        assert auxjad.LoopByNotes(input_music, window_size=100)
        assert auxjad.LoopByNotes(input_music,
                                  window_size=3,
                                  step_size=-1,
                                  )
        assert auxjad.LoopByNotes(input_music,
                                  window_size=3,
                                  step_size=100,
                                  )
        assert auxjad.LoopByNotes(input_music,
                                  window_size=3,
                                  max_steps=-1,
                                  )
        assert auxjad.LoopByNotes(input_music,
                                  window_size=3,
                                  repetition_chance=-0.3,
                                  )
        assert auxjad.LoopByNotes(input_music,
                                  window_size=3,
                                  repetition_chance=1.4,
                                  )
        assert auxjad.LoopByNotes(input_music,
                                  window_size=3,
                                  head_position=-1,
                                  )
        assert auxjad.LoopByNotes(input_music,
                                  window_size=3,
                                  head_position=100,
                                  )


def test_LoopByNotes_12():
    input_music = abjad.Container(r"c'4 d'2 r8 d'4 <e' g'>8 r4 f'2. <e' g'>16")
    looper = auxjad.LoopByNotes(input_music,
                                window_size=4,
                                )
    music = looper.output_all(tie_identical_pitches=True)
    staff = abjad.Staff(music)
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


def test_LoopByNotes_13():
    input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LoopByNotes(input_music, window_size=2)
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


def test_LoopByNotes_14():
    input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LoopByNotes(input_music, window_size=2)
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


def test_LoopByNotes_15():
    input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LoopByNotes(input_music, window_size=2)
    with pytest.raises(RuntimeError):
        looper.output_n(100)


def test_LoopByNotes_16():
    input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LoopByNotes(input_music,
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


def test_LoopByNotes_16():
    input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LoopByNotes(input_music,
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


def test_LoopByNotes_17():
    input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
    looper = auxjad.LoopByNotes(input_music,
                                window_size=2,
                                force_identical_time_signatures=True,
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
            \time 2/4
            d'4
            e'4
            \time 2/4
            e'4
            f'4
            \time 1/4
            f'4
        }
        """)


def test_LoopByNotes_18():
    input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    looper = auxjad.LoopByNotes(input_music,
                                window_size=3,
                                move_window_on_first_call=True,
                                )
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 11/8
            d'2
            e'4
            f'2
            ~
            f'8
        }
        """)


def test_LoopByNotes_19():
    input_music = abjad.Container(r"c'4 d'4 e'4 f'4 g'4 a'4")
    looper = auxjad.LoopByNotes(input_music,
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
            d'4
            e'4
            f'4
        }
        """)
    looper.contents = abjad.Container(r"c'''4 r4 d'''4 r4 e'''4 r4 f'''4 r4")
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            d'''4
            r4
            e'''4
        }
        """)
    looper.head_position = 0
    notes = looper()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'''4
            r4
            d'''4
        }
        """)
