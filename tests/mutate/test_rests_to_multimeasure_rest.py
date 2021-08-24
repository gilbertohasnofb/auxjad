import abjad

import auxjad


def test_rests_to_multimeasure_rest_01():
    staff = abjad.Staff(r"r1")
    auxjad.mutate.rests_to_multimeasure_rest(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            R1
        }
        """
    )


def test_rests_to_multimeasure_rest_02():
    staff = abjad.Staff(r"r2 r8.. r32 r16 r8 r16")
    auxjad.mutate.rests_to_multimeasure_rest(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            R1
        }
        """
    )


def test_rests_to_multimeasure_rest_03():
    staff = abjad.Staff(
        r"\time 3/4 r2. | \time 6/8 r2. | \time 5/4 c'1 ~ c'4 | r1 r4"
    )
    auxjad.mutate.rests_to_multimeasure_rest(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            R1 * 3/4
            \time 6/8
            R1 * 3/4
            \time 5/4
            c'1
            ~
            c'4
            R1 * 5/4
        }
        """
    )


def test_rests_to_multimeasure_rest_04():
    staff = abjad.Staff(r"\times 2/3 {r2 r2 r2}")
    auxjad.mutate.rests_to_multimeasure_rest(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            R1
        }
        """
    )
    staff = abjad.Staff(
        r"r2 \times 2/3 {r2 r4} \times 4/5 {r2. \times 2/3 {r2 r4}}"
    )
    auxjad.mutate.rests_to_multimeasure_rest(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            R1
            R1
        }
        """
    )


def test_rests_to_multimeasure_rest_05():
    staff = abjad.Staff(
        r"r2 \times 2/3 {r2 r4} \times 4/5 {r2. \times 2/3 {r2 r4}}"
    )
    auxjad.mutate.rests_to_multimeasure_rest(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            R1
            R1
        }
        """
    )


def test_rests_to_multimeasure_rest_06():
    staff = abjad.Staff(r"r2 r8.. r32 r16 r8 r16")
    abjad.mutate.rests_to_multimeasure_rest(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            R1
        }
        """
    )


def test_rests_to_multimeasure_rest_07():
    staff = abjad.Staff(
        r"\clef bass r4 r4 \times 2/3 {r4 r8} r4 "
        r"\time 3/4 \clef treble r2. "
        r"\time 5/4 r2 \clef bass r2."
    )
    abjad.mutate.rests_to_multimeasure_rest(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "bass"
            R1
            \time 3/4
            \clef "treble"
            R1 * 3/4
            \time 5/4
            \clef "bass"
            R1 * 5/4
        }
        """
    )
    staff = abjad.Staff(
        r"\clef bass r4 r4 \times 2/3 {r4 r8} r4 "
        r"\time 3/4 \clef treble r2. "
        r"\time 5/4 r2 \clef bass r2."
    )
    abjad.mutate.rests_to_multimeasure_rest(staff[:], ignore_clefs=True)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            R1
            \time 3/4
            R1 * 3/4
            \time 5/4
            R1 * 5/4
        }
        """
    )


def test_rests_to_multimeasure_rest_08():
    staff = abjad.Staff(r"c'1\p\< r2\! r2 d'1\f\> r2 r2\ppp")
    abjad.mutate.rests_to_multimeasure_rest(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            \<
            R1
            \!
            d'1
            \f
            \>
            R1
            \ppp
        }
        """
    )
    staff = abjad.Staff(r"c'1\p\< r2\! r2 d'1\f\> r2 r2\ppp")
    abjad.mutate.rests_to_multimeasure_rest(staff[:], ignore_dynamics=True)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            \<
            R1
            d'1
            \f
            \>
            R1
        }
        """
    )
