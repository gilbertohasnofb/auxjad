import random

import abjad
import pytest

import auxjad


def test_Shuffler_01():
    random.seed(87234)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    shuffler = auxjad.Shuffler(container)
    assert format(shuffler) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            d'4
            c'4
            f'4
            e'4
        }
        """)
    notes = shuffler.shuffle()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            e'4
            d'4
            f'4
        }
        """)
    notes = shuffler.current_window
    with pytest.raises(AttributeError):
        shuffler.current_window = abjad.Container(r"c''2 e''2")
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            e'4
            d'4
            f'4
        }
        """)


def test_Shuffler_02():
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 \time 2/4 f'4 g'4")
    shuffler = auxjad.Shuffler(container,
                               pitch_only=False,
                               preserve_rest_position=True,
                               disable_rewrite_meter=False,
                               omit_time_signatures=True,
                               boundary_depth=0,
                               maximum_dot_count=1,
                               rewrite_tuplets=False,
                               process_on_first_call=True,
                               )
    assert not shuffler.pitch_only
    assert shuffler.preserve_rest_position
    assert not shuffler.disable_rewrite_meter
    assert shuffler.omit_time_signatures
    assert shuffler.boundary_depth == 0
    assert shuffler.maximum_dot_count == 1
    assert not shuffler.rewrite_tuplets
    assert shuffler.process_on_first_call
    shuffler.pitch_only = True
    shuffler.preserve_rest_position = False
    shuffler.disable_rewrite_meter = True
    shuffler.omit_time_signatures = False
    shuffler.boundary_depth = 1
    shuffler.maximum_dot_count = 2
    shuffler.rewrite_tuplets = True
    shuffler.process_on_first_call = False
    assert shuffler.pitch_only
    assert not shuffler.preserve_rest_position
    assert shuffler.disable_rewrite_meter
    assert not shuffler.omit_time_signatures
    assert shuffler.boundary_depth == 1
    assert shuffler.maximum_dot_count == 2
    assert shuffler.rewrite_tuplets
    assert not shuffler.process_on_first_call


def test_Shuffler_03():
    random.seed(18331)
    container = abjad.Container(r"c'8. d'4 r8 r8. e'16 f'8.")
    shuffler = auxjad.Shuffler(container)
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r4
            r16
            e'16
            f'8
            ~
            f'16
            d'8.
            ~
            d'16
            c'8.
        }
        """)
    container = abjad.Container(r"c'8. d'4 r8 r8. e'16 f'8.")
    shuffler = auxjad.Shuffler(container, pitch_only=True)
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            f'8.
            r4
            d'8
            ~
            d'8.
            c'16
            e'8.
        }
        """)


def test_Shuffler_04():
    container = abjad.Container(
        r"\time 3/4 c'16 d'8. ~ d'4 e'4 r4 f'4 ~ f'8.. g'32"
    )
    shuffler = auxjad.Shuffler(container)
    notes = shuffler.rotate()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            d'4..
            e'16
            ~
            e'8.
            r16
            r8.
            f'16
            ~
            f'4
            ~
            f'8
            ~
            f'32
            g'32
            c'16
        }
        """)
    notes = shuffler.rotate(n_rotations=2, anticlockwise=True)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            g'32
            c'16
            d'32
            ~
            d'8
            ~
            d'4
            ~
            d'32
            e'8..
            ~
            e'32
            r8..
            r32
            f'4...
        }
        """)
    container = abjad.Container(
        r"\time 3/4 c'16 d'8. ~ d'4 e'4 r4 f'4 ~ f'8.. g'32"
    )
    shuffler = auxjad.Shuffler(container, pitch_only=True)
    notes = shuffler.rotate()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            d'16
            e'8.
            ~
            e'4
            r4
            f'4
            g'4
            ~
            g'8..
            c'32
        }
        """)
    notes = shuffler.rotate(n_rotations=2, anticlockwise=True)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            g'16
            c'8.
            ~
            c'4
            d'4
            e'4
            r4
            r8..
            f'32
        }
        """)


def test_Shuffler_05():
    random.seed(18332)
    container = abjad.Container(r"c'8. d'4 r8 r8. e'16 f'8.")
    shuffler = auxjad.Shuffler(container, preserve_rest_position=True)
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            d'4
            e'16
            r8.
            r8
            f'8
            ~
            f'16
            c'8.
        }
        """)
    container = abjad.Container(r"c'8. d'4 r8 r8. e'16 f'8.")
    shuffler = auxjad.Shuffler(container,
                               pitch_only=True,
                               preserve_rest_position=True,
                               )
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            d'8.
            f'4
            r8
            r8.
            c'16
            e'8.
        }
        """)


def test_Shuffler_06():
    container = abjad.Container(r"c'8. d'4 r8 r8. e'16 f'8.")
    shuffler = auxjad.Shuffler(container, preserve_rest_position=True)
    notes = shuffler.rotate()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            d'4
            e'16
            r8.
            r8
            f'8
            ~
            f'16
            c'8.
        }
        """)
    container = abjad.Container(r"c'8. d'4 r8 r8. e'16 f'8.")
    shuffler = auxjad.Shuffler(container,
                               pitch_only=True,
                               preserve_rest_position=True,
                               )
    notes = shuffler.rotate()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            d'8.
            e'4
            r8
            r8.
            f'16
            c'8.
        }
        """)


def test_Shuffler_07():
    random.seed(98231)
    container = abjad.Container(r"c'4 d'8 e'4. f'8. g'16")
    shuffler = auxjad.Shuffler(container)
    notes = shuffler.shuffle_n(2)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            d'8
            g'16
            c'16
            ~
            c'8.
            f'16
            ~
            f'8
            e'4.
            g'16
            f'8.
            e'4
            ~
            e'8
            c'4
            d'8
        }
        """)
    container = abjad.Container(r"c'4 d'8 e'4. f'8. g'16")
    shuffler = auxjad.Shuffler(container, pitch_only=True)
    notes = shuffler.shuffle_n(2)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            e'4
            d'8
            g'4.
            c'8.
            f'16
            f'4
            c'8
            d'4.
            e'8.
            g'16
        }
        """)


def test_Shuffler_08():
    container = abjad.Container(r"c'4 d'8 e'4. f'8. g'16")
    shuffler = auxjad.Shuffler(container)
    notes = shuffler.rotate_n(2)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            d'8
            e'4.
            f'8.
            g'16
            c'4
            e'4.
            f'8
            ~
            f'16
            g'16
            c'4
            d'8
        }
        """)
    container = abjad.Container(r"c'4 d'8 e'4. f'8. g'16")
    shuffler = auxjad.Shuffler(container, pitch_only=True)
    notes = shuffler.rotate_n(2)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            d'4
            e'8
            f'4.
            g'8.
            c'16
            e'4
            f'8
            g'4.
            c'8.
            d'16
        }
        """)


def test_Shuffler_09():
    random.seed(17231)
    container = abjad.Container(r"\time 5/4 r4 \times 2/3 {c'4 d'2} e'4. f'8")
    shuffler = auxjad.Shuffler(container, pitch_only=True)
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 5/4
            d'4
            \times 2/3 {
                f'4
                c'2
            }
            e'4.
            r8
        }
        """)
    shuffler.pitch_only = False
    with pytest.raises(ValueError):
        notes = shuffler()
    with pytest.raises(ValueError):
        notes = shuffler.rotate()


def test_Shuffler_10():
    random.seed(98103)
    container = abjad.Container(
        r"\time 3/4 c'8. d'4 r8 r8. \time 2/4 e'16 f'4.."
    )
    shuffler = auxjad.Shuffler(container)
    notes = shuffler.shuffle_n(2)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            e'16
            d'8.
            ~
            d'16
            f'4..
            \time 2/4
            c'8.
            r16
            r4
            \time 3/4
            c'8.
            f'16
            ~
            f'4.
            r8
            \time 2/4
            r8.
            d'16
            ~
            d'8.
            e'16
        }
        """)


def test_Shuffler_11():
    random.seed(87233)
    container = abjad.Container(r"<c' e' g'>4--\p d'8-. e'8-. f'4-^\f r4")
    shuffler = auxjad.Shuffler(container)
    notes = shuffler.shuffle_n(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            e'8
            \p
            - \staccato
            d'8
            - \staccato
            f'4
            \f
            - \marcato
            <c' e' g'>4
            \p
            - \tenuto
            r4
            r4
            d'8
            - \staccato
            f'8
            \f
            - \marcato
            ~
            f'8
            <c' e' g'>4
            \p
            - \tenuto
            e'8
            - \staccato
            f'4
            \f
            - \marcato
            e'8
            \p
            - \staccato
            <c' e' g'>8
            - \tenuto
            ~
            <c' e' g'>8
            d'8
            - \staccato
            r4
        }
        """)


def test_Shuffler_12():
    random.seed(18892)
    container = abjad.Container(r"\time 3/4 c'16 d'4.. e'4 | r4 f'2")
    shuffler = auxjad.Shuffler(container,
                               omit_time_signatures=True,
                               )
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            d'4..
            e'16
            ~
            e'8.
            f'16
            ~
            f'4..
            r16
            r8.
            c'16
        }
        """)
    assert shuffler.omit_time_signatures
    shuffler.omit_time_signatures = False
    assert not shuffler.omit_time_signatures


def test_Shuffler_13():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    shuffler = auxjad.Shuffler(container)
    assert format(shuffler.contents) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    shuffler()
    assert format(shuffler.contents) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    shuffler.contents = abjad.Container(r"cs2 ds2")
    assert format(shuffler.contents) == abjad.String.normalize(
        r"""
        {
            cs2
            ds2
        }
        """)


def test_Shuffler_14():
    container = abjad.Container(r"c'2 d'2")
    shuffler = auxjad.Shuffler(container)
    assert len(shuffler) == 2
    container = abjad.Container(r"c'4 d'4 e'4 f'4 ~ | f'2 g'2")
    shuffler = auxjad.Shuffler(container)
    assert len(shuffler) == 5
    container = abjad.Container(r"c'8. d'4 r8 r8. e'16 f'8.")
    shuffler = auxjad.Shuffler(container)
    assert len(shuffler) == 5


def test_Shuffler_15():
    random.seed(98604)
    container = abjad.Container(r"c'4. d'8 e'2")
    shuffler = auxjad.Shuffler(container)
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            e'2
            c'4.
            d'8
        }
        """)
    random.seed(98604)
    shuffler = auxjad.Shuffler(container,
                               boundary_depth=1,
                               )
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            e'2
            c'4
            ~
            c'8
            d'8
        }
        """)


def test_Shuffler_16():
    random.seed(19867)
    container = abjad.Container(r"c'4 d'8. e'16 f'2")
    shuffler = auxjad.Shuffler(container)
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            e'16
            f'8.
            ~
            f'4
            ~
            f'16
            c'8.
            ~
            c'16
            d'8.
        }
        """)
    random.seed(19867)
    shuffler = auxjad.Shuffler(container,
                               disable_rewrite_meter=True,
                               )
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            e'16
            f'2
            c'4
            d'8.
        }
        """)


def test_Shuffler_17():
    random.seed(22047)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    shuffler = auxjad.Shuffler(container,
                               process_on_first_call=False,
                               )
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
        }
        """)


def test_Shuffler_18():
    random.seed(10932)
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
    shuffler = auxjad.Shuffler(container)
    staff = abjad.Staff()
    for window in shuffler:
        staff.append(window)
        if abjad.inspect(staff).duration() == abjad.Duration((9, 4)):
            break
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            e'4
            c'4
            d'4
            \time 3/4
            d'4
            c'4
            e'4
            \time 3/4
            c'4
            e'4
            d'4
        }
        """)
    auxjad.mutate(staff[:]).remove_repeated_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            e'4
            c'4
            d'4
            d'4
            c'4
            e'4
            c'4
            e'4
            d'4
        }
        """)


def test_Shuffler_19():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    shuffler = auxjad.Shuffler(container)
    assert isinstance(shuffler(), abjad.Selection)
    tuplet = abjad.Tuplet('3:2', r"c'2 d'2 e'2")
    shuffler = auxjad.Shuffler(tuplet, pitch_only=True)
    assert isinstance(shuffler(), abjad.Selection)
    voice = abjad.Voice(r"c'4 d'4 e'4 f'4")
    shuffler = auxjad.Shuffler(voice)
    assert isinstance(shuffler(), abjad.Selection)
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    shuffler = auxjad.Shuffler(staff)
    assert isinstance(shuffler(), abjad.Selection)
    score = abjad.Score([abjad.Staff(r"c'4 d'4 e'4 f'4")])
    shuffler = auxjad.Shuffler(score)
    assert isinstance(shuffler(), abjad.Selection)
    voice = abjad.Voice(r"c'4 d'4 e'4 f'4")
    staff = abjad.Staff([voice])
    shuffler = auxjad.Shuffler(staff)
    assert isinstance(shuffler(), abjad.Selection)
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    score = abjad.Score([staff])
    shuffler = auxjad.Shuffler(score)
    assert isinstance(shuffler(), abjad.Selection)

    voice1 = abjad.Voice(r"c'4 d'4 e'4 f'4")
    voice2 = abjad.Voice(r"g2 f2")
    staff = abjad.Staff([voice1, voice2], simultaneous=True)
    with pytest.raises(ValueError):
        auxjad.Shuffler(staff)

    staff1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
    staff2 = abjad.Staff(r"g2 f2")
    score = abjad.Score([staff1, staff2])
    with pytest.raises(ValueError):
        auxjad.Shuffler(score)


def test_Shuffler_20():
    random.seed(76123)
    container = abjad.Container(r"\times 2/3 {\time 3/4 r8 d'8 r8} c'4 r4")
    shuffler = auxjad.Shuffler(container, pitch_only=True)
    notes = shuffler.shuffle_n(5)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                \time 3/4
                r8
                d'8
                r8
            }
            r4
            c'4
            \times 2/3 {
                d'8
                c'8
                r8
            }
            r4
            r4
            r4
            d'4
            c'4
            \times 2/3 {
                r8
                d'8
                c'8
            }
            r4
            r4
            \times 2/3 {
                c'8
                r8
                r8
            }
            d'4
            r4
        }
        """)


def test_Shuffler_21():
    random.seed(98141)
    container = abjad.Container(r"c'4.. d'16 e'4. f'8")
    shuffler = auxjad.Shuffler(container, pitch_only=True)
    notes = shuffler.shuffle_n(2)
    staff = abjad.Staff(notes)
    shuffler.pitch_only = False
    notes = shuffler.shuffle_n(2)
    staff.append(notes)
    auxjad.mutate(staff[:]).remove_repeated_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            d'4..
            c'16
            f'4.
            e'8
            d'4..
            f'16
            c'4.
            e'8
            f'16
            d'4..
            e'8
            c'4.
            c'4.
            d'8
            ~
            d'4
            ~
            d'16
            e'8
            f'16
        }
        """)
