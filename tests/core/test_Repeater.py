import abjad
import pytest

import auxjad


def test_Repeater__init__():
    r"""Confirm correct initialisation of attributes."""
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    repeater = auxjad.Repeater(container)
    assert abjad.lilypond(repeater) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
        }
        """
    )
    notes = repeater()
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
        }
        """
    )
    notes = repeater.current_window
    with pytest.raises(AttributeError):
        repeater.current_window = abjad.Container(r"c''2 e''2")
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
        }
        """
    )


def test_Repeater__call__():
    r"""Confirm correct behaviour when calling instance."""
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    repeater = auxjad.Repeater(container)
    notes = repeater(2)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
        """
    )


def test_Repeater_time_signature():
    r"""Confirm function handles time signatures correctly."""
    container = abjad.Container(r"\time 3/4 c'2. \time 2/4 r2 g'2")
    repeater = auxjad.Repeater(container)
    notes = repeater(3)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
        """
    )


def test_Repeater_underfull_containers():
    r"""Confirm underfull containers get a time signature assigned to them."""
    container = abjad.Container(r"c'4 d'4 e'4")
    repeater = auxjad.Repeater(container)
    notes = repeater(3)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
        """
    )


def test_Repeater_underfull_containers_after_more_than_one_bar():
    r"""Confirm underfull containers with more than a single bar get a time
    signature assigned to them.
    """
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 f'2")
    repeater = auxjad.Repeater(container)
    notes = repeater(2)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
        """
    )


def test_Repeater_omit_time_signatures():
    r"""Confirm omit_time_signatures correctly prevents automatic time
    signature from being attached.
    """
    container = abjad.Container(r"c'4 d'4 e'4")
    repeater = auxjad.Repeater(container,
                               omit_time_signatures=True,
                               )
    notes = repeater(3)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
        """
    )


def test_Repeater_force_identical_time_signatures():
    r"""Confirm force_identical_time_signatures will attach time signatures at
    every repetition point.
    """
    container = abjad.Container(r"\time 5/4 c'2. d'4 e'4")
    repeater = auxjad.Repeater(container,
                               force_identical_time_signatures=True,
                               )
    notes = repeater(3)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
        """
    )


def test_Repeater_malformed_container():
    r"""Confirm malformed container raises ValueError."""
    container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'1")
    with pytest.raises(ValueError):
        repeater = auxjad.Repeater(container)  # noqa: F841


def test_Repeater_indicators():
    r"""Confirm correct handling of indicators such as dynamics and slurs."""
    container = abjad.Container(r"\clef bass f4\pp( e4) d4(")
    repeater = auxjad.Repeater(container)
    notes = repeater(3)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
        """
    )


def test_Repeater_disabling_reposition_of_indicators():
    r"""Confirm reposition of indicators can be disabled through individual
    arguments.
    """
    container = abjad.Container(r"\clef bass f4\pp( e4) d4(")
    repeater = auxjad.Repeater(container,
                               reposition_clefs=False,
                               reposition_dynamics=False,
                               reposition_slurs=False,
                               )
    notes = repeater(3)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
        """
    )


def test_Repeater_initialising_then_changing_attributes():
    r"""Confirm correct initialisation of attributes then confirm they are
    modifiable.
    """
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 \time 2/4 f'4 g'4")
    repeater = auxjad.Repeater(container,
                               repeat_type='volta',
                               include_2x_volta_text=False,
                               omit_time_signatures=False,
                               force_identical_time_signatures=False,
                               reposition_clefs=True,
                               reposition_dynamics=True,
                               reposition_slurs=True,
                               )
    assert repeater.repeat_type == 'volta'
    assert not repeater.include_2x_volta_text
    assert not repeater.omit_time_signatures
    assert not repeater.force_identical_time_signatures
    assert repeater.reposition_clefs
    assert repeater.reposition_dynamics
    assert repeater.reposition_slurs
    repeater.repeat_type = 'unfold'
    repeater.include_2x_volta_text = True
    repeater.omit_time_signatures = True
    repeater.force_identical_time_signatures = True
    repeater.reposition_clefs = False
    repeater.reposition_dynamics = False
    repeater.reposition_slurs = False
    assert repeater.repeat_type == 'unfold'
    assert repeater.include_2x_volta_text
    assert repeater.omit_time_signatures
    assert repeater.force_identical_time_signatures
    assert not repeater.reposition_clefs
    assert not repeater.reposition_dynamics
    assert not repeater.reposition_slurs


def test_Repeater_as_iterator():
    r"""Confirm instance can be used as an iterator."""
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
    repeater = auxjad.Repeater(container)
    staff = abjad.Staff()
    for window in repeater:
        staff.append(window)
        if abjad.get.duration(staff) == abjad.Duration((9, 4)):
            break
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
        """
    )
    auxjad.mutate.remove_repeated_time_signatures(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
        """
    )


def test_Repeater_change_of_contents_after_initialisation():
    r"""Confirm contents can be changed after initialisation."""
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    repeater = auxjad.Repeater(container)
    notes = repeater(2)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
        """
    )
    repeater.contents = abjad.Container(r"c'16 d'16 e'16 f'16 g'2.")
    notes = repeater(2)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
        """
    )


def test_Repeater_output_n():
    r"""Confirm output_n behaves exactly like __call__."""
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    repeater = auxjad.Repeater(container)
    notes = repeater.output_n(2)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
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
        """
    )


def test_Repeater_testing_different_container_types():
    r"""Confirm correct behaviour with any types of containers, including
    Tuplet, Voice, Staff, Score, etc.
    """
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    repeater = auxjad.Repeater(container)
    assert isinstance(repeater(), abjad.Selection)

    tuplet = abjad.Tuplet('3:2', r"c'2 d'2 e'2")
    repeater = auxjad.Repeater(tuplet)
    assert isinstance(repeater(), abjad.Selection)

    voice = abjad.Voice(r"c'4 d'4 e'4 f'4")
    repeater = auxjad.Repeater(voice)
    assert isinstance(repeater(), abjad.Selection)

    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    repeater = auxjad.Repeater(staff)
    assert isinstance(repeater(), abjad.Selection)

    score = abjad.Score([abjad.Staff(r"c'4 d'4 e'4 f'4")])
    repeater = auxjad.Repeater(score)
    assert isinstance(repeater(), abjad.Selection)

    voice = abjad.Voice(r"c'4 d'4 e'4 f'4")
    staff = abjad.Staff([voice])
    repeater = auxjad.Repeater(staff)
    assert isinstance(repeater(), abjad.Selection)

    staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
    score = abjad.Score([staff])
    repeater = auxjad.Repeater(score)
    assert isinstance(repeater(), abjad.Selection)


def test_Repeater_no_parallel_containers():
    r"""Confirm parallel containers (two voices in staff, two staves in score)
    raise ValueError.
    """
    voice1 = abjad.Voice(r"c'4 d'4 e'4 f'4")
    voice2 = abjad.Voice(r"g2 f2")
    staff = abjad.Staff([voice1, voice2], simultaneous=True)
    with pytest.raises(ValueError):
        repeater = auxjad.Repeater(staff)  # noqa: F841

    staff1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
    staff2 = abjad.Staff(r"g2 f2")
    score = abjad.Score([staff1, staff2])
    with pytest.raises(ValueError):
        repeater = auxjad.Repeater(score)  # noqa: F841


def test_Repeater_repeat_type():
    r"""Confirm repeat_type can be used for both unfold and volta types of
    repeat.
    """
    container = abjad.Container(r"c'2 d'2")
    repeater = auxjad.Repeater(container,
                               repeat_type='unfold'
                               )
    notes = repeater(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'2
            d'2
            c'2
            d'2
            c'2
            d'2
            c'2
            d'2
            c'2
            d'2
        }
        """
    )
    container = abjad.Container(r"c'2 d'2")
    repeater = auxjad.Repeater(container,
                               repeat_type='volta'
                               )
    notes = repeater(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \repeat volta 5
            {
                c'2
                d'2
                \tweak RehearsalMark.self-alignment-X #RIGHT
                \tweak RehearsalMark.break-visibility #begin-of-line-invisible
                \mark \markup{\box "5×"}
            }
        }
        """
    )


def test_Repeater_complex_example_with_volta_repeat():
    r"""Confirm correct behaviour with volta repeat, including the creation of
    markups with "Nx" above repeat bars.
    """
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    repeater = auxjad.Repeater(container,
                               repeat_type='volta',
                               )
    notes = repeater(3)
    staff = abjad.Staff(notes)
    repeater.contents = abjad.Container(r"g'2 a'2")
    notes = repeater(2)
    staff.append(notes)
    repeater.contents = abjad.Container(r"b'16 c''16 d''16 e''16 r2.")
    notes = repeater(5)
    staff.append(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \repeat volta 3
            {
                c'4
                d'4
                e'4
                f'4
                \tweak RehearsalMark.self-alignment-X #RIGHT
                \tweak RehearsalMark.break-visibility #begin-of-line-invisible
                \mark \markup{\box "3×"}
            }
            \repeat volta 2
            {
                g'2
                a'2
                \tweak RehearsalMark.self-alignment-X #RIGHT
                \tweak RehearsalMark.break-visibility #begin-of-line-invisible
                \mark \markup{\box "2×"}
            }
            \repeat volta 5
            {
                b'16
                c''16
                d''16
                e''16
                r2.
                \tweak RehearsalMark.self-alignment-X #RIGHT
                \tweak RehearsalMark.break-visibility #begin-of-line-invisible
                \mark \markup{\box "5×"}
            }
        }

        """
    )


def test_Repeater_disabling_2x_volta_text():
    r"""Confirm include_2x_volta_text can be disabled, resulting in repeat bars
    showing "Nx" only for N > 2.
    """
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    repeater = auxjad.Repeater(container,
                               repeat_type='volta',
                               include_2x_volta_text=False,
                               )
    notes = repeater(3)
    staff = abjad.Staff(notes)
    repeater.contents = abjad.Container(r"g'2 a'2")
    notes = repeater(2)
    staff.append(notes)
    repeater.contents = abjad.Container(r"b'16 c''16 d''16 e''16 r2.")
    notes = repeater(5)
    staff.append(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \repeat volta 3
            {
                c'4
                d'4
                e'4
                f'4
                \tweak RehearsalMark.self-alignment-X #RIGHT
                \tweak RehearsalMark.break-visibility #begin-of-line-invisible
                \mark \markup{\box "3×"}
            }
            \repeat volta 2
            {
                g'2
                a'2
            }
            \repeat volta 5
            {
                b'16
                c''16
                d''16
                e''16
                r2.
                \tweak RehearsalMark.self-alignment-X #RIGHT
                \tweak RehearsalMark.break-visibility #begin-of-line-invisible
                \mark \markup{\box "5×"}
            }
        }
        """
    )
