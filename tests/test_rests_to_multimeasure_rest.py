import abjad
import auxjad


def test_rests_to_multimeasure_rest_01():
    container = abjad.Container(r"r1")
    auxjad.rests_to_multimeasure_rest(container)
    assert format(container) == abjad.String.normalize(
        r"""
        {
            R1
        }
        """)


def test_rests_to_multimeasure_rest_02():
    container = abjad.Container(r"\time 3/4 r4 r8.. r32 r4")
    auxjad.rests_to_multimeasure_rest(container)
    assert format(container) == abjad.String.normalize(
        r"""
        {
            %%% \time 3/4 %%%
            R1 * 3/4
        }
        """)


def test_rests_to_multimeasure_rest_03():
    container = abjad.Container(r"\time 3/4 r2. | "
                                r"\time 6/8 r2. | "
                                r"\time 5/4 c'1 ~ c'4 | r1 r4"
                                )
    auxjad.rests_to_multimeasure_rest(container)
    assert format(container) == abjad.String.normalize(
        r"""
        {
            %%% \time 3/4 %%%
            R1 * 3/4
            %%% \time 6/8 %%%
            R1 * 3/4
            %%% \time 5/4 %%%
            c'1
            ~
            c'4
            R1 * 5/4
        }
        """)
