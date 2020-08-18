import abjad
import pytest

import auxjad


def test_Repeater_01():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    repeater = auxjad.Repeater(container)
    assert format(repeater) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    notes = repeater()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    notes = repeater.current_window
    with pytest.raises(AttributeError):
        repeater.current_window = abjad.Container(r"c''2 e''2")
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)


def test_Repeater_02():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    repeater = auxjad.Repeater(container)
    notes = repeater(2)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
            c'4
            d'4
            e'4
            f'4
        }
        """)


def test_Repeater_03():
    container = abjad.Staff(r"\time 3/4 c'2. \time 2/4 r2 g'2")
    repeater = auxjad.Repeater(container)
    notes = repeater(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2.
            \time 2/4
            r2
            g'2
            \time 3/4
            c'2.
            \time 2/4
            r2
            g'2
            \time 3/4
            c'2.
            \time 2/4
            r2
            g'2
        }
        """)


def test_Repeater_04():
    container = abjad.Container(r"c'4 d'4 e'4")
    repeater = auxjad.Repeater(container)
    notes = repeater(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
        }
        """)


def test_Repeater_05():
    container = abjad.Staff(r"\time 3/4 c'4 d'4 e'4 f'2")
    repeater = auxjad.Repeater(container)
    notes = repeater(2)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
            \time 2/4
            f'2
            \time 3/4
            c'4
            d'4
            e'4
            \time 2/4
            f'2
        }
        """)


def test_Repeater_06():
    container = abjad.Staff(r"c'4 d'4 e'4")
    repeater = auxjad.Repeater(container,
                               omit_time_signatures=True,
                               )
    notes = repeater(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
        }
        """)


def test_Repeater_07():
    container = abjad.Staff(r"\time 5/4 c'2. d'4 e'4")
    repeater = auxjad.Repeater(container,
                               force_identical_time_signatures=True,
                               )
    notes = repeater(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 5/4
            c'2.
            d'4
            e'4
            \time 5/4
            c'2.
            d'4
            e'4
            \time 5/4
            c'2.
            d'4
            e'4
        }
        """)


def test_Repeater_08():
    container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'1")
    with pytest.raises(ValueError):
        assert auxjad.Repeater(container)


def test_Repeater_09():
    container = abjad.Staff(r"\clef bass f4\pp( e4) d4(")
    repeater = auxjad.Repeater(container)
    notes = repeater(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            \clef "bass"
            f4
            \pp
            (
            e4
            )
            d4
            (
            f4
            e4
            )
            d4
            (
            f4
            e4
            )
            d4
        }
        """)
    repeater = auxjad.Repeater(container,
                               reposition_clefs=False,
                               reposition_dynamics=False,
                               reposition_slurs=False,
                               )
    notes = repeater(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            \clef "bass"
            f4
            \pp
            (
            e4
            )
            d4
            (
            \clef "bass"
            f4
            \pp
            (
            e4
            )
            d4
            (
            \clef "bass"
            f4
            \pp
            (
            e4
            )
            d4
            (
        }
        """)


def test_Repeater_10():
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 \time 2/4 f'4 g'4")
    repeater = auxjad.Repeater(container,
                               omit_time_signatures=False,
                               force_identical_time_signatures=False,
                               reposition_clefs=True,
                               reposition_dynamics=True,
                               reposition_slurs=True,
                               )
    assert not repeater.omit_time_signatures
    assert not repeater.force_identical_time_signatures
    assert repeater.reposition_clefs
    assert repeater.reposition_dynamics
    assert repeater.reposition_slurs
    repeater.omit_time_signatures = True
    repeater.force_identical_time_signatures = True
    repeater.reposition_clefs = False
    repeater.reposition_dynamics = False
    repeater.reposition_slurs = False
    assert repeater.omit_time_signatures
    assert repeater.force_identical_time_signatures
    assert not repeater.reposition_clefs
    assert not repeater.reposition_dynamics
    assert not repeater.reposition_slurs


def test_Repeater_11():
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
    repeater = auxjad.Repeater(container)
    staff = abjad.Staff()
    for window in repeater:
        staff.append(window)
        if abjad.inspect(staff).duration() == abjad.Duration((9, 4)):
            break
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
            \time 3/4
            c'4
            d'4
            e'4
            \time 3/4
            c'4
            d'4
            e'4
        }
        """)
    auxjad.mutate(staff[:]).remove_repeated_time_signatures()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
        }
        """)


def test_Repeater_12():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    repeater = auxjad.Repeater(container)
    notes = repeater(2)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
            c'4
            d'4
            e'4
            f'4
        }
        """)
    repeater.contents = abjad.Container(r"c'16 d'16 e'16 f'16 g'2.")
    notes = repeater(2)
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
            c'16
            d'16
            e'16
            f'16
            g'2.
        }
        """)


def test_Repeater_13():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    repeater = auxjad.Repeater(container)
    notes = repeater.output_n(2)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
            c'4
            d'4
            e'4
            f'4
        }
        """)


def test_Repeater_14():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    repeater = auxjad.Repeater(container)
    notes = repeater()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
