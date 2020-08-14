import random

import abjad
import pytest

import auxjad


def test_Fader_01():
    random.seed(13987)
    container = abjad.Container(r"c'4 ~ c'16 d'8. e'8 f'8 ~ f'4")
    fader = auxjad.Fader(container)
    assert format(fader) == abjad.String.normalize(
        r"""
        {
            c'4
            ~
            c'16
            d'8.
            e'8
            f'8
            ~
            f'4
        }
        """)
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            ~
            c'16
            d'8.
            e'8
            f'4.
        }
        """)
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            ~
            c'16
            r8.
            e'8
            f'4.
        }
        """)
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r2
            e'8
            f'4.
        }
        """)
    notes = fader.current_window
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r2
            e'8
            f'4.
        }
        """)


def test_Fader_02():
    random.seed(98752)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    fader = auxjad.Fader(container)
    notes = fader()
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
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            r4
            e'4
            f'4
        }
        """)
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r2
            e'4
            f'4
        }
        """)
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r2.
            f'4
        }
        """)
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            R1
        }
        """)
    with pytest.raises(RuntimeError):
        fader()


def test_Fader_03():
    container = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
    fader = auxjad.Fader(container,
                         fader_type='in',
                         max_steps=2,
                         repetition_chance=0.7,
                         disable_rewrite_meter=True,
                         omit_time_signatures=True,
                         use_multimeasure_rests=False,
                         mask=[1, 0, 1, 1, 0],
                         boundary_depth=0,
                         maximum_dot_count=1,
                         rewrite_tuplets=False,
                         process_on_first_call=True,
                         include_empty_measures=False,
                         )
    assert fader.fader_type == 'in'
    assert fader.max_steps == 2
    assert fader.repetition_chance == 0.7
    assert fader.disable_rewrite_meter
    assert fader.omit_time_signatures
    assert not fader.use_multimeasure_rests
    assert fader.mask == [1, 0, 1, 1, 0]
    assert fader.boundary_depth == 0
    assert fader.maximum_dot_count == 1
    assert not fader.rewrite_tuplets
    assert fader.process_on_first_call
    assert not fader.include_empty_measures
    fader.fader_type = 'out'
    fader.max_steps = 1
    fader.repetition_chance = 0.23
    fader.disable_rewrite_meter = False
    fader.omit_time_signatures = False
    fader.use_multimeasure_rests = True
    fader.mask = [0, 1, 1, 0, 1]
    fader.boundary_depth = 1
    fader.maximum_dot_count = 2
    fader.rewrite_tuplets = True
    fader.process_on_first_call = False
    fader.include_empty_measures = True
    assert fader.fader_type == 'out'
    assert fader.max_steps == 1
    assert fader.repetition_chance == 0.23
    assert not fader.disable_rewrite_meter
    assert not fader.omit_time_signatures
    assert fader.use_multimeasure_rests
    assert fader.mask == [0, 1, 1, 0, 1]
    assert fader.boundary_depth == 1
    assert fader.maximum_dot_count == 2
    assert fader.rewrite_tuplets
    assert not fader.process_on_first_call
    assert fader.include_empty_measures


def test_Fader_04():
    random.seed(19962)
    container = abjad.Container(r"c'4. d'8 e'2")
    fader = auxjad.Fader(container)
    notes = fader.output_all()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4.
            d'8
            e'2
            r4.
            d'8
            e'2
            r2
            e'2
            R1
        }
        """)


def test_Fader_05():
    random.seed(98738)
    container = abjad.Container(r"c'4. d'8 e'2")
    fader = auxjad.Fader(container,
                         fader_type='in',
                         )
    notes = fader.output_all()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            R1
            r4.
            d'8
            r2
            c'4.
            d'8
            r2
            c'4.
            d'8
            e'2
        }
        """)


def test_Fader_06():
    random.seed(13241)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    fader = auxjad.Fader(container)
    notes = fader.__next__()
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
    notes = fader.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            r4
            f'4
        }
        """)
    notes = fader.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            r2
        }
        """)
    fader.fader_type = 'in'
    notes = fader.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            r4
            f'4
        }
        """)
    notes = fader.__next__()
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
    fader.mask = [0, 0, 1, 1]
    notes = fader.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r2
            e'4
            f'4
        }
        """)
    notes = fader.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r4
            d'4
            e'4
            f'4
        }
        """)


def test_Fader_07():
    random.seed(44126)
    container = abjad.Container(r"\times 2/3 {c'8 d'8 e'8} d'2.")
    fader = auxjad.Fader(container)
    notes = fader.output_all()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                \time 4/4
                c'8
                d'8
                e'8
            }
            d'2.
            \times 2/3 {
                r8
                d'8
                e'8
            }
            d'2.
            \times 2/3 {
                r8
                d'8
                r8
            }
            d'2.
            r4
            d'2.
            R1
        }
        """)


def test_Fader_08():
    random.seed(88111)
    container = abjad.Container(r"c'4. d'8 e'16 f'16 g'4.")
    fader = auxjad.Fader(container)
    notes = fader.output_n(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4.
            d'8
            e'16
            f'16
            g'4.
            c'4.
            r8
            e'16
            f'16
            g'4.
            c'4.
            r8
            e'16
            f'16
            r4.
        }
        """)


def test_Fader_09():
    random.seed(14812)
    container = abjad.Container(
        r"\time 3/8 c'4. \time 2/4 d'2 \time 3/8 e'4."
    )
    fader = auxjad.Fader(container)
    notes = fader.output_n(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/8
            c'4.
            \time 2/4
            d'2
            \time 3/8
            e'4.
            c'4.
            \time 2/4
            R1 * 1/2
            \time 3/8
            e'4.
            c'4.
            \time 2/4
            R1 * 1/2
            \time 3/8
            R1 * 3/8
        }
        """)


def test_Fader_10():
    random.seed(29862)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    fader = auxjad.Fader(container,
                         max_steps=3,
                         process_on_first_call=True,
                         )
    notes = fader.output_n(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'8
            d'8
            r8
            f'8
            g'8
            a'8
            b'8
            c''8
            r4.
            f'8
            g'8
            a'8
            b'8
            c''8
            r4.
            f'8
            r8
            a'8
            b'8
            r8
        }
        """)


def test_Fader_11():
    random.seed(18711)
    container = abjad.Container(r"c'8 d'8 e'2.")
    fader = auxjad.Fader(container,
                         disable_rewrite_meter=True,
                         use_multimeasure_rests=False,
                         )
    notes = fader.output_all()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'8
            d'8
            e'2.
            c'8
            r8
            e'2.
            r8
            r8
            e'2.
            r8
            r8
            r2.
        }
        """)


def test_Fader_12():
    random.seed(87123)
    container = abjad.Container(r"\time 2/4 c'4 d'4 \time 3/4 e'4 f'4 g'4")
    fader = auxjad.Fader(container,
                         omit_time_signatures=True,
                         )
    notes = fader.output_n(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
            g'4
            c'4
            d'4
            e'4
            f'4
            r4
            c'4
            d'4
            e'4
            r2
        }
        """)


def test_Fader_13():
    random.seed(47103)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    fader = auxjad.Fader(container,
                         process_on_first_call=True,
                         )
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            e'4
            r4
        }
        """)


def test_Fader_14():
    random.seed(19941)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    fader = auxjad.Fader(container,
                         fader_type='in',
                         mask=[0, 1, 1, 0]
                         )
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r4
            d'4
            e'4
            r4
        }
        """)
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            e'4
            r4
        }
        """)
    fader.reset_mask()
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            R1
        }
        """)
    fader.fader_type = 'out'
    fader.reset_mask()
    notes = fader()
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


def test_Fader_15():
    random.seed(71324)
    container = abjad.Container(
        r"\time 3/4 c'8->\f d'8\p ~ d'4 e'8..-- f'32-."
    )
    fader = auxjad.Fader(container)
    notes = fader.output_all()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'8
            \f
            - \accent
            d'4.
            \p
            e'8..
            - \tenuto
            f'32
            - \staccato
            c'8
            \f
            - \accent
            d'4.
            \p
            r8..
            f'32
            - \staccato
            c'8
            \f
            - \accent
            d'4.
            \p
            r4
            c'8
            \f
            - \accent
            r8
            r2
            R1 * 3/4
        }
        """)


def test_Fader_16():
    random.seed(91634)
    container = abjad.Container(r"c'4 ~ c'16 d'8. e'8 f'8 ~ f'4")
    fader = auxjad.Fader(container,
                         fader_type='in',
                         )
    assert format(fader) == abjad.String.normalize(
        r"""
        {
            c'4
            ~
            c'16
            d'8.
            e'8
            f'8
            ~
            f'4
        }
        """)
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            R1
        }
        """)
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r2
            r8
            f'4.
        }
        """)
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            ~
            c'16
            r8.
            r8
            f'4.
        }
        """)
    notes = fader.current_window
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            ~
            c'16
            r8.
            r8
            f'4.
        }
        """)


def test_Fader_17():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    fader = auxjad.Fader(container)
    assert len(fader) == 4
    container = abjad.Container(r"c'4 ~ c'8 d'8 e'4 ~ e'8 f'8")
    fader = auxjad.Fader(container)
    assert len(fader) == 4
    container = abjad.Container(r"c'4 ~ c'16 r16 d'8 e'4 ~ e'8 f'16 r16")
    fader = auxjad.Fader(container)
    assert len(fader) == 4
    container = abjad.Container(r"<c' e' g'>2 <d' f'>2")
    fader = auxjad.Fader(container)
    assert len(fader) == 5
    container = abjad.Container(r"<c' e' g'>4 ~ <c' e' g'>16 r8. <d' f'>2")
    fader = auxjad.Fader(container)
    assert len(fader) == 5
    container = abjad.Container(r"<c' e' g'>4 d'4 <e' g' b'>4 r4")
    fader = auxjad.Fader(container)
    assert len(fader) == 7


def test_Fader_18():
    random.seed(66501)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    fader = auxjad.Fader(container)
    notes = fader()
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
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r4
            d'4
            e'4
            f'4
        }
        """)
    fader.contents = abjad.Container(r"c'16 d'16 e'16 f'16 g'2.")
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'16
            d'16
            e'16
            f'16
            g'2.
        }
        """)
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'16
            d'16
            r16
            f'16
            g'2.
        }
        """)


def test_Fader_19():
    random.seed(48915)
    container = abjad.Container(r"c'4 d'8 e'8 f'4 ~ f'8. g'16")
    fader = auxjad.Fader(container)
    assert fader.mask == [1, 1, 1, 1, 1]
    fader = auxjad.Fader(container,
                         fader_type='in',
                         )
    assert fader.mask == [0, 0, 0, 0, 0]
    fader()
    assert fader.mask == [0, 0, 0, 0, 0]
    fader()
    assert fader.mask == [0, 1, 0, 0, 0]
    fader()
    assert fader.mask == [0, 1, 1, 0, 0]
    staff = abjad.Staff(fader.current_window)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r4
            d'8
            e'8
            r2
        }
        """)
    fader.mask = [1, 0, 1, 1, 0]
    assert fader.mask == [1, 0, 1, 1, 0]
    notes = fader()
    staff = abjad.Staff(notes)
    abjad.f(staff)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            r8
            e'8
            f'4..
            r16
        }
        """)
    fader.reset_mask()
    assert fader.mask == [0, 0, 0, 0, 0]
    notes = fader()
    staff = abjad.Staff(notes)
    abjad.f(staff)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            R1
        }
        """)


def test_Fader_20():
    container = abjad.Container(r"c'4. d'8 e'2")
    fader = auxjad.Fader(container)
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4.
            d'8
            e'2
        }
        """)
    fader = auxjad.Fader(container,
                         boundary_depth=1,
                         )
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            ~
            c'8
            d'8
            e'2
        }
        """)


def test_Fader_22():
    random.seed(92114)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    fader = auxjad.Fader(container)
    fader.random_mask()
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r8
            d'8
            r4
            g'8
            a'8
            r4
        }
        """)
    fader.random_mask()
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r8
            d'8
            r4
            g'8
            a'8
            b'8
            r8
        }
        """)


def test_Fader_23():
    random.seed(36017)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    fader = auxjad.Fader(container,
                         mask=[0, 0, 1, 1, 1, 1, 1, 1],
                         )
    fader.shuffle_mask()
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r8
            d'8
            e'8
            f'8
            g'8
            a'8
            b'8
            r8
        }
        """)
    fader.shuffle_mask()
    notes = fader()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'8
            d'8
            e'8
            r8
            g'8
            r8
            b'8
            c''8
        }
        """)


def test_Fader_24():
    random.seed(83012)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    fader = auxjad.Fader(container)
    staff = abjad.Staff()
    for window in fader:
        staff.append(window)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
            \time 4/4
            c'4
            r4
            e'4
            f'4
            \time 4/4
            c'4
            r4
            e'4
            r4
            \time 4/4
            c'4
            r2.
            \time 4/4
            R1
        }
        """)
    auxjad.mutate(staff[:]).remove_repeated_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
            c'4
            r4
            e'4
            f'4
            c'4
            r4
            e'4
            r4
            c'4
            r2.
            R1
        }
        """)


def test_Fader_25():
    random.seed(19873)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    fader = auxjad.Fader(container, max_steps=3)
    staff = abjad.Staff()
    for window in fader:
        staff.append(window)
    auxjad.mutate(staff[:]).remove_repeated_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
            c'4
            r2.
            R1
        }
        """)


def test_Fader_26():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    fader = auxjad.Fader(container)
    assert isinstance(fader(), abjad.Selection)
    tuplet = abjad.Tuplet('3:2', r"c'2 d'2 e'2")
    fader = auxjad.Fader(tuplet)
    assert isinstance(fader(), abjad.Selection)
    voice = abjad.Voice(r"c'4 d'4 e'4 f'4")
    fader = auxjad.Fader(voice)
    assert isinstance(fader(), abjad.Selection)
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    fader = auxjad.Fader(staff)
    assert isinstance(fader(), abjad.Selection)
    score = abjad.Score([abjad.Staff(r"c'4 d'4 e'4 f'4")])
    fader = auxjad.Fader(score)
    assert isinstance(fader(), abjad.Selection)
    voice = abjad.Voice(r"c'4 d'4 e'4 f'4")
    staff = abjad.Staff([voice])
    fader = auxjad.Fader(staff)
    assert isinstance(fader(), abjad.Selection)
    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    score = abjad.Score([staff])
    fader = auxjad.Fader(score)
    assert isinstance(fader(), abjad.Selection)

    voice1 = abjad.Voice(r"c'4 d'4 e'4 f'4")
    voice2 = abjad.Voice(r"g2 f2")
    staff = abjad.Staff([voice1, voice2], simultaneous=True)
    with pytest.raises(ValueError):
        fader = auxjad.Fader(staff)

    staff1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
    staff2 = abjad.Staff(r"g2 f2")
    score = abjad.Score([staff1, staff2])
    with pytest.raises(ValueError):
        fader = auxjad.Fader(score)


def test_Fader_27():
    random.seed(41888)
    container = abjad.Container(r"\times 2/3 {c'2(\p\< d'2 e'2\f} "
                                r"f'4\p\> g'2 a'4\pp)")
    fader = auxjad.Fader(container)
    notes = fader.output_n(5)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                \time 4/4
                c'2
                \p
                \<
                (
                d'2
                e'2
                \f
            }
            f'4
            \p
            \>
            g'2
            a'4
            \pp
            )
            \times 2/3 {
                c'2
                \p
                \<
                (
                d'2
                e'2
                \f
                )
            }
            r4
            g'2
            \p
            \>
            (
            a'4
            \pp
            )
            \times 2/3 {
                r2
                d'2
                \p
                \<
                (
                e'2
                \f
                )
            }
            r4
            g'2
            \p
            \>
            (
            a'4
            \pp
            )
            \times 2/3 {
                r2
                d'2
                \p
                \<
                r2
                \f
                )
            }
            r4
            g'2
            \p
            \>
            (
            a'4
            \pp
            )
            R1
            r4
            g'2
            \p
            \>
            (
            a'4
            \pp
            )
        }
        """)


def test_Fader_28():
    random.seed(17613)
    container = abjad.Container(r"<c' e'>4 ~ <c' e'>16 d'8. <gs e'>8 "
                                r"<bf f' a'>8 ~ <bf f' a'>4")
    fader = auxjad.Fader(container)
    staff = abjad.Staff(fader.output_all())
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            <c' e'>4
            ~
            <c' e'>16
            d'8.
            <gs e'>8
            <bf f' a'>4.
            <c' e'>4
            ~
            <c' e'>16
            d'8.
            gs8
            <bf f' a'>4.
            <c' e'>4
            ~
            <c' e'>16
            d'8.
            gs8
            <bf a'>4.
            c'4
            ~
            c'16
            d'8.
            gs8
            <bf a'>4.
            r4
            r16
            d'8.
            gs8
            <bf a'>4.
            r4
            r16
            d'8.
            gs8
            bf4.
            r2
            gs8
            bf4.
            r2
            r8
            bf4.
            R1
        }
        """)


def test_Fader_29():
    container = abjad.Container(r"c'2 <d' e' f' g'>2")
    fader = auxjad.Fader(container, mask=[1, 0, 1, 1, 0])
    staff = abjad.Staff(fader())
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'2
            <e' f'>2
        }
        """)


def test_Fader_30():
    random.seed(39761)
    container = abjad.Container([
        auxjad.ArtificialHarmonic(r"<c' f'>2"),
        abjad.Chord(r"<c' f'>2"),
    ])
    fader = auxjad.Fader(container, fader_type='out')
    staff = abjad.Staff(fader.output_all())
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            <
                c'
                \tweak style #'harmonic
                f'
            >2
            <c' f'>2
            <
                c'
                \tweak style #'harmonic
                f'
            >2
            f'2
            <
                c'
                \tweak style #'harmonic
                f'
            >2
            r2
            R1
        }
        """)


def test_Fader_31():
    random.seed(76132)
    container = abjad.Container(r"c'4 d'4 e'2")
    fader = auxjad.Fader(container,
                         fader_type='out',
                         process_on_first_call=False,
                         include_empty_measures=True,
                         )
    staff = abjad.Staff(fader.output_all())
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            e'2
            r4
            d'4
            e'2
            r2
            e'2
            R1
        }
        """)
    random.seed(76132)
    container = abjad.Container(r"c'4 d'4 e'2")
    fader = auxjad.Fader(container,
                         fader_type='out',
                         process_on_first_call=True,
                         include_empty_measures=True,
                         )
    staff = abjad.Staff(fader.output_all())
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r4
            d'4
            e'2
            r2
            e'2
            R1
        }
        """)
    random.seed(76132)
    container = abjad.Container(r"c'4 d'4 e'2")
    fader = auxjad.Fader(container,
                         fader_type='out',
                         process_on_first_call=False,
                         include_empty_measures=False,
                         )
    staff = abjad.Staff(fader.output_all())
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            e'2
            r4
            d'4
            e'2
            r2
            e'2
        }
        """)
    random.seed(76132)
    container = abjad.Container(r"c'4 d'4 e'2")
    fader = auxjad.Fader(container,
                         fader_type='out',
                         process_on_first_call=True,
                         include_empty_measures=False,
                         )
    staff = abjad.Staff(fader.output_all())
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r4
            d'4
            e'2
            r2
            e'2
        }
        """)


def test_Fader_32():
    random.seed(76132)
    container = abjad.Container(r"c'4 d'4 e'2")
    fader = auxjad.Fader(container,
                         fader_type='in',
                         process_on_first_call=False,
                         include_empty_measures=True,
                         )
    staff = abjad.Staff(fader.output_all())
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            R1
            c'4
            r2.
            c'4
            d'4
            r2
            c'4
            d'4
            e'2
        }
        """)
    random.seed(76132)
    container = abjad.Container(r"c'4 d'4 e'2")
    fader = auxjad.Fader(container,
                         fader_type='in',
                         process_on_first_call=True,
                         include_empty_measures=True,
                         )
    staff = abjad.Staff(fader.output_all())
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            r2.
            c'4
            d'4
            r2
            c'4
            d'4
            e'2
        }
        """)
    random.seed(76132)
    container = abjad.Container(r"c'4 d'4 e'2")
    fader = auxjad.Fader(container,
                         fader_type='in',
                         process_on_first_call=False,
                         include_empty_measures=False,
                         )
    staff = abjad.Staff(fader.output_all())
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            r2.
            c'4
            d'4
            r2
            c'4
            d'4
            e'2
        }
        """)
    random.seed(76132)
    container = abjad.Container(r"c'4 d'4 e'2")
    fader = auxjad.Fader(container,
                         fader_type='in',
                         process_on_first_call=True,
                         include_empty_measures=False,
                         )
    staff = abjad.Staff(fader.output_all())
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            r2.
            c'4
            d'4
            r2
            c'4
            d'4
            e'2
        }
        """)


def test_Fader_33():
    random.seed(85909)
    container = abjad.Container(r"c'4. d'8 e'4.. f'16")
    fader = auxjad.Fader(container,
                         repetition_chance=0.5,
                         )
    notes = fader.output_n(5)
    staff = abjad.Staff(notes)
    abjad.f(staff)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4.
            d'8
            e'4..
            f'16
            c'4.
            d'8
            e'4..
            r16
            c'4.
            d'8
            e'4..
            r16
            c'4.
            d'8
            r2
            c'4.
            d'8
            r2
        }
        """)
