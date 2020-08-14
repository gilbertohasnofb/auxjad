import abjad
import pytest

import auxjad


def test_sustain_notes_01():
    staff = abjad.Staff(r"c'16 r8. d'16 r8. e'16 r8. f'16 r8.")
    auxjad.mutate(staff).sustain_notes()
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


def test_sustain_notes_02():
    staff = abjad.Staff(r"c'16 r8. c'16 r8. c'16 r8. c'16 r8.")
    auxjad.mutate(staff).sustain_notes()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            c'4
            c'4
            c'4
        }
        """)


def test_sustain_notes_03():
    staff = abjad.Staff(r"<c' e'>16 r8. <c' e'>4 <c' e'>4 <c' e'>16 r8.")
    auxjad.mutate(staff).sustain_notes()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            <c' e'>4
            <c' e'>4
            <c' e'>4
            <c' e'>4
        }
        """)


def test_sustain_notes_04():
    staff = abjad.Staff(r"\times 2/3 {c'4 d'4 r4} r8 e'8 \times 2/3 {f'8 r4}")
    auxjad.mutate(staff).sustain_notes()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                c'4
                d'2
                ~
            }
            d'8
            e'8
            f'4
        }
        """)


def test_sustain_notes_05():
    staff = abjad.Staff(r"c'16 r8. d'16 r8. r8 r32 <e' g'>32 r16 r4 "
                        r"\times 2/3 {r4 f'4 r4} r4 g'8 r8 a'4 ~ "
                        r"a'16 r8. b'4 c''8 r8 "
                        r"r4. d''8 \times 4/5 {r8 d''2}"
                        )
    auxjad.mutate(staff).sustain_notes()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            ~
            d'8
            ~
            d'32
            <e' g'>16.
            ~
            <e' g'>4
            ~
            \times 2/3 {
                <e' g'>4
                f'2
                ~
            }
            f'4
            g'4
            a'2
            b'4
            c''4
            ~
            c''4.
            d''8
            ~
            \times 4/5 {
                d''8
                d''2
            }
        }
        """)


def test_sustain_notes_06():
    staff = abjad.Staff(r"c'16 r8. c'16 r8. c'4 c'16 r8.")
    with pytest.raises(TypeError):
        auxjad.mutate(staff[:]).sustain_notes()
