import abjad
import pytest

import auxjad


def test_contract_notes_01():
    staff = abjad.Staff(r"c'4 r2. d'2 r2 e'2. r4 f'1")
    auxjad.mutate.contract_notes(staff, abjad.Duration((1, 8)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            r2..
            d'4.
            r8
            r2
            e'2
            ~
            e'8
            r4.
            f'2..
            r8
        }
        """
    )


def test_contract_notes_02():
    staff = abjad.Staff(r"\time 3/4 c'2. <d' e' f'>2 r4 g'4 r2")
    auxjad.mutate.contract_notes(staff, abjad.Duration((1, 16)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2
            ~
            c'8.
            r16
            <d' e' f'>4..
            r16
            r4
            g'8.
            r16
            r2
        }
        """
    )


def test_contract_notes_03():
    staff = abjad.Staff(r"c'4 r2. d'2 r2 e'2. r4 f'1")
    auxjad.mutate.contract_notes(staff, abjad.Duration((1, 2)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            R1
            R1
            e'4
            r2.
            f'2
            r2
        }
        """
    )


def test_contract_notes_04():
    staff = abjad.Staff(r"c'4\ppp r2. d'2\ff r2 e'2.\f r4 f'1\mp")
    auxjad.mutate.contract_notes(staff, abjad.Duration((1, 8)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            \ppp
            r2..
            d'4.
            \ff
            r8
            r2
            e'2
            \f
            ~
            e'8
            r4.
            f'2..
            \mp
            r8
        }
        """
    )


def test_contract_notes_05():
    staff = abjad.Staff(
        r"\time 3/4 c'4 r2 "
        r"\time 2/4 d'2 "
        r"\time 3/4 e'2. "
        r"\time 4/4 f'1"
    )
    auxjad.mutate.contract_notes(staff, abjad.Duration((1, 8)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'8
            r8
            r2
            \time 2/4
            d'4.
            r8
            \time 3/4
            e'2
            ~
            e'8
            r8
            \time 4/4
            f'2..
            r8
        }
        """
    )


def test_contract_notes_06():
    staff = abjad.Staff(r"c'4 r2. d'2 r2 e'2. r4 f'1")
    auxjad.mutate.contract_notes(staff,
                                 abjad.Duration((1, 2)),
                                 minimum_duration=abjad.Duration((1, 8)),
                                 )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            r2..
            d'8
            r2..
            e'4
            r2.
            f'2
            r2
        }
        """
    )


def test_contract_notes_07():
    staff = abjad.Staff(
        r"\time 4/4 c'4 r2. \time 3/4 d'4 r2 \time 4/4 e'4 r2."
    )
    auxjad.mutate.contract_notes(staff, abjad.Duration((1, 2)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            R1
            \time 3/4
            R1 * 3/4
            \time 4/4
            R1
        }
        """
    )
    staff = abjad.Staff(
        r"\time 4/4 c'4 r2. \time 3/4 d'4 r2 \time 4/4 e'4 r2."
    )
    auxjad.mutate.contract_notes(staff,
                                 abjad.Duration((1, 2)),
                                 use_multimeasure_rests=False,
                                 )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r1
            \time 3/4
            r2.
            \time 4/4
            r1
        }
        """
    )


def test_contract_notes_08():
    staff = abjad.Staff(r"\time 3/4 r8 c'8 ~ c'2 r8 d'8 ~ d'2")
    auxjad.mutate.contract_notes(staff, abjad.Duration((1, 8)))
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            r8
            c'8
            ~
            c'4.
            ~
            r8
            r8
            d'8
            ~
            d'4.
            ~
            r8
        }
        """
    )
    staff = abjad.Staff(r"\time 3/4 r8 c'8 ~ c'2 r8 d'8 ~ d'2")
    auxjad.mutate.contract_notes(staff,
                                 abjad.Duration((1, 8)),
                                 rewrite_meter=False,
                                 )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            r8
            c'2
            ~
            r8
            r8
            d'2
            ~
            r8
        }
        """
    )


def test_contract_notes_09():
    staff = abjad.Staff(r"c'4 r4 \times 2/3 {r4 d'4 r4} e'4 r2.")
    with pytest.raises(ValueError):
        auxjad.mutate.contract_notes(staff, abjad.Duration((1, 8)))
