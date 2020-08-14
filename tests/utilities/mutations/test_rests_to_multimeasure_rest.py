import abjad

import auxjad


def test_rests_to_multimeasure_rest_01():
    staff = abjad.Staff(r"r1")
    auxjad.mutate(staff[:]).rests_to_multimeasure_rest()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            R1
        }
        """)


def test_rests_to_multimeasure_rest_02():
    staff = abjad.Staff(r"r2 r8.. r32 r16 r8 r16")
    auxjad.mutate(staff[:]).rests_to_multimeasure_rest()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            R1
        }
        """)


def test_rests_to_multimeasure_rest_03():
    staff = abjad.Staff(
        r"\time 3/4 r2. | \time 6/8 r2. | \time 5/4 c'1 ~ c'4 | r1 r4"
    )
    auxjad.mutate(staff[:]).rests_to_multimeasure_rest()
    assert format(staff) == abjad.String.normalize(
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
        """)


def test_rests_to_multimeasure_rest_04():
    staff = abjad.Staff(r"\times 2/3 {r2 r2 r2}")
    auxjad.mutate(staff[:]).rests_to_multimeasure_rest()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            R1
        }
        """)
    staff = abjad.Staff(
        r"r2 \times 2/3 {r2 r4} \times 4/5 {r2. \times 2/3 {r2 r4}}"
    )
    auxjad.mutate(staff[:]).rests_to_multimeasure_rest()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            R1
            R1
        }
        """)


def test_rests_to_multimeasure_rest_05():
    staff = abjad.Staff(
        r"r2 \times 2/3 {r2 r4} \times 4/5 {r2. \times 2/3 {r2 r4}}"
    )
    auxjad.mutate(staff[:]).rests_to_multimeasure_rest()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            R1
            R1
        }
        """)


def test_rests_to_multimeasure_rest_06():
    staff = abjad.Staff(r"r2 r8.. r32 r16 r8 r16")
    abjad.mutate(staff[:]).rests_to_multimeasure_rest()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            R1
        }
        """)
