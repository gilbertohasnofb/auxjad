import abjad
import pytest

import auxjad


def test_extend_notes_01():
    staff = abjad.Staff(r"c'16 r2... d'8 r2.. e'8. r16 r2. f'4 r2.")
    auxjad.mutate.extend_notes(staff, abjad.Duration((1, 4)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            r2.
            d'4
            r2.
            e'4
            r2.
            f'4
            r2.
        }
        """
    )


def test_extend_notes_02():
    staff = abjad.Staff(
        r"\time 3/4 c'8 r8 r2 r4 <d' e' f'>4 r4 r8 g'16 r16 r2"
    )
    auxjad.mutate.extend_notes(staff, abjad.Duration((2, 4)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2
            r4
            r4
            <d' e' f'>2
            r8
            g'8
            ~
            g'4.
            r8
        }
        """
    )


def test_extend_notes_03():
    staff = abjad.Staff(r"c'16 r2... d'16 r2... e'16 r2... f'16 r2...")
    auxjad.mutate.extend_notes(staff, (1, 4))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            r2.
            d'4
            r2.
            e'4
            r2.
            f'4
            r2.
        }
        """
    )
    staff = abjad.Staff(r"c'16 r2... d'16 r2... e'16 r2... f'16 r2...")
    auxjad.mutate.extend_notes(staff, 0.25)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            r2.
            d'4
            r2.
            e'4
            r2.
            f'4
            r2.
        }
        """
    )
    staff = abjad.Staff(r"c'16 r2... d'16 r2... e'16 r2... f'16 r2...")
    auxjad.mutate.extend_notes(staff, 1 / 4)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            r2.
            d'4
            r2.
            e'4
            r2.
            f'4
            r2.
        }
        """
    )
    staff = abjad.Staff(r"c'16 r2... d'16 r2... e'16 r2... f'16 r2...")
    auxjad.mutate.extend_notes(staff, "1/4")
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            r2.
            d'4
            r2.
            e'4
            r2.
            f'4
            r2.
        }
        """
    )


def test_extend_notes_04():
    staff = abjad.Staff(r"c'16 r4.. d'16 r4.. e'16 r2... f'16 r4.. g'16 r4..")
    auxjad.mutate.extend_notes(staff, abjad.Duration((3, 4)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'2
            d'2
            e'2.
            r4
            f'2
            g'2
        }
        """
    )


def test_extend_notes_05():
    staff = abjad.Staff(
        r"c'16\ppp r2... d'16\ff r2... e'16\f r2... f'16\mp r2..."
    )
    auxjad.mutate.extend_notes(staff, abjad.Duration((3, 4)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'2.
            \ppp
            r4
            d'2.
            \ff
            r4
            e'2.
            \f
            r4
            f'2.
            \mp
            r4
        }
        """
    )


def test_extend_notes_06():
    staff = abjad.Staff(
        r"r16 c'16 r4. r16 d'16 r4. r16 e'16 r4. r16 f'16 r4."
    )
    auxjad.mutate.extend_notes(staff, abjad.Duration((1, 4)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r16
            c'8.
            ~
            c'16
            r8.
            r16
            d'8.
            ~
            d'16
            r8.
            r16
            e'8.
            ~
            e'16
            r8.
            r16
            f'8.
            ~
            f'16
            r8.
        }
        """
    )
    staff = abjad.Staff(
        r"r16. c'32 r4. r16. d'32 r4. r16. e'32 r4. r16. f'32 r4."
    )
    auxjad.mutate.extend_notes(staff, abjad.Duration((1, 4)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r16.
            c'32
            ~
            c'8
            ~
            c'16.
            r32
            r8
            r16.
            d'32
            ~
            d'8
            ~
            d'16.
            r32
            r8
            r16.
            e'32
            ~
            e'8
            ~
            e'16.
            r32
            r8
            r16.
            f'32
            ~
            f'8
            ~
            f'16.
            r32
            r8
        }
        """
    )


def test_extend_notes_07():
    staff = abjad.Staff(
        r"\time 3/4 c'16 r8. r2 \time 2/4 d'8 r8 e'8 r8 \time 3/4 r2 f'16 r8."
    )
    auxjad.mutate.extend_notes(staff, abjad.Duration((3, 4)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2.
            \time 2/4
            d'4
            e'4
            ~
            \time 3/4
            e'2
            f'4
        }
        """
    )


def test_extend_notes_08():
    staff = abjad.Staff(r"c'16 r4.. d'16 r4..")
    auxjad.mutate.extend_notes(staff,
                               abjad.Duration((1, 4)),
                               rewrite_meter=False,
                               )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'16
            ~
            c'8.
            r4
            d'16
            ~
            d'8.
            r4
        }
        """
    )


def test_extend_notes_09():
    staff = abjad.Staff(r"c'16 r2... d'16 r2... e'16 r2... f'16 r2...")
    abjad.mutate.extend_notes(staff, abjad.Duration((1, 4)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            r2.
            d'4
            r2.
            e'4
            r2.
            f'4
            r2.
        }
        """
    )


def test_extend_notes_10():
    staff = abjad.Staff(r"c'16 r2... d'2 r2 e'2. r4 f'1")
    auxjad.mutate.extend_notes(staff, abjad.Duration((1, 4)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            r2.
            d'2
            r2
            e'2.
            r4
            f'1
        }
        """
    )


def test_extend_notes_11():
    staff = abjad.Staff(
        r"r8 c'8 r2. r8 "
        r"d'8 ~ d'4 r2 "
        r"r16 e'8. ~ e'4 r2 "
        r"r16 f'8. ~ f'2."
    )
    auxjad.mutate.extend_notes(staff, abjad.Duration((3, 4)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r8
            c'8
            ~
            c'2
            ~
            c'8
            r8
            r8
            d'8
            ~
            d'2
            ~
            d'8
            r8
            r16
            e'8.
            ~
            e'2
            ~
            e'16
            r8.
            r16
            f'2...
        }
        """
    )


def test_extend_notes_12():
    staff = abjad.Staff(r"r4 c'4 r4 c'4 r8 c'8 r2")
    auxjad.mutate.extend_notes(staff, abjad.Duration((2, 4)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r4
            c'2
            c'4
            ~
            c'8
            c'8
            ~
            c'4
            ~
            c'8
            r4.
        }
        """
    )


def test_extend_notes_13():
    staff = abjad.Staff(r"\time 3/4 r8 c'8 r4 c'4 R1 * 3/4 r8 c'8 r2 R1 * 3/4")
    auxjad.mutate.extend_notes(staff, abjad.Duration((2, 4)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            r8
            c'4.
            c'4
            ~
            c'4
            r2
            r8
            c'8
            ~
            c'4.
            r8
            R1 * 3/4
        }
        """
    )
    staff = abjad.Staff(r"\time 3/4 r8 c'8 r4 c'4 r2. r8 c'8 r2 r2.")
    auxjad.mutate.extend_notes(staff, abjad.Duration((2, 4)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            r8
            c'4.
            c'4
            ~
            c'4
            r2
            r8
            c'8
            ~
            c'4.
            r8
            R1 * 3/4
        }
        """
    )
    staff = abjad.Staff(r"\time 3/4 r8 c'8 r4 c'4 R1 * 3/4 r8 c'8 r2 R1 * 3/4")
    auxjad.mutate.extend_notes(staff,
                               abjad.Duration((2, 4)),
                               use_multimeasure_rests=False,
                               )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            r8
            c'4.
            c'4
            ~
            c'4
            r2
            r8
            c'8
            ~
            c'4.
            r8
            r2.
        }
        """
    )


def test_extend_notes_14():
    staff = abjad.Staff(r"c'4 r4 d'4 r4 e'4 r2.")
    auxjad.mutate.extend_notes(staff,
                               abjad.Duration((2, 4)),
                               gap=abjad.Duration((1, 16)),
                               )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4..
            r16
            d'4..
            r16
            e'2
            r2
        }
        """
    )


def test_extend_notes_15():
    staff = abjad.Staff(r"c'2 d'4 r4 e'4 r4 f'2 ~ f'2 r2")
    auxjad.mutate.extend_notes(staff,
                               abjad.Duration((2, 4)),
                               gap=abjad.Duration((1, 16)),
                               )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'2
            d'4..
            r16
            e'4..
            r16
            f'2
            ~
            f'2
            r2
        }
        """
    )


def test_extend_notes_16():
    staff = abjad.Staff(r"c'16 r8. d'16 r8. e'16 r8. f'16 r8.")
    auxjad.mutate.extend_notes(staff,
                               abjad.Duration((1, 4)),
                               gap=abjad.Duration((1, 16)),
                               )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8.
            r16
            d'8.
            r16
            e'8.
            r16
            f'4
        }
        """
    )
    staff = abjad.Staff(r"c'16 r8. d'16 r8. e'16 r8. f'16 r8.")
    auxjad.mutate.extend_notes(staff,
                               abjad.Duration((1, 4)),
                               gap=abjad.Duration((1, 16)),
                               gap_before_end=True,
                               )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8.
            r16
            d'8.
            r16
            e'8.
            r16
            f'8.
            r16
        }
        """
    )


def test_extend_notes_17():
    staff = abjad.Staff(r"c'4 r4 \times 2/3 {r4 d'4 r4} e'4 r2.")
    with pytest.raises(ValueError):
        auxjad.mutate.extend_notes(staff, abjad.Duration((1, 4)))
