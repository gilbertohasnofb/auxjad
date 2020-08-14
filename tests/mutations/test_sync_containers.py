import abjad
import pytest

import auxjad


def test_sync_containers_01():
    container1 = abjad.Staff(r"\time 4/4 g'2.")
    container2 = abjad.Staff(r"\time 4/4 c'1")
    auxjad.mutate([container1, container2]).sync_containers()
    assert (abjad.inspect(container1).duration()
            == abjad.inspect(container2).duration())
    assert format(container1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            g'2.
            r4
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
        }
        """)


def test_sync_containers_02():
    container1 = abjad.Staff(r"\time 4/4 g'1 | f'4")
    container2 = abjad.Staff(r"\time 4/4 c'1")
    auxjad.mutate([container1, container2]).sync_containers()
    assert (abjad.inspect(container1).duration()
            == abjad.inspect(container2).duration())
    assert format(container1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            g'1
            \time 1/4
            f'4
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            \time 1/4
            R1 * 1/4
        }
        """)


def test_sync_containers_03():
    container1 = abjad.Staff(r"\time 4/4 g'1 | f'4")
    container2 = abjad.Staff(r"\time 4/4 c'1 | d'1")
    auxjad.mutate([container1, container2]).sync_containers()
    assert (abjad.inspect(container1).duration()
            == abjad.inspect(container2).duration())
    assert format(container1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            g'1
            f'4
            r2.
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            d'1
        }
        """)


def test_sync_containers_04():
    container1 = abjad.Staff(r"\time 4/4 g'1")
    container2 = abjad.Staff(r"\time 4/4 c'1 | d'1")
    auxjad.mutate([container1, container2]).sync_containers()
    assert (abjad.inspect(container1).duration()
            == abjad.inspect(container2).duration())
    assert format(container1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            g'1
            R1
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            d'1
        }
        """)


def test_sync_containers_05():
    container1 = abjad.Staff(r"\time 4/4 g'1")
    container2 = abjad.Staff(r"\time 4/4 c'1 | d'1")
    auxjad.mutate([container1, container2]).sync_containers(
        use_multimeasure_rests=False,
    )
    assert (abjad.inspect(container1).duration()
            == abjad.inspect(container2).duration())
    assert format(container1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            g'1
            r1
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            d'1
        }
        """)


def test_sync_containers_06():
    container1 = abjad.Staff(r"\time 3/4 g'2.")
    container2 = abjad.Staff(r"\time 3/4 c'2. | d'2.")
    auxjad.mutate([container1, container2]).sync_containers()
    assert (abjad.inspect(container1).duration()
            == abjad.inspect(container2).duration())
    assert format(container1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            g'2.
            R1 * 3/4
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2.
            d'2.
        }
        """)


def test_sync_containers_07():
    container1 = abjad.Staff(r"\time 4/4 c'1 | g'4")
    container2 = abjad.Staff(r"\time 4/4 c'1 | g'2")
    container3 = abjad.Staff(r"\time 4/4 c'1 | g'2.")
    container4 = abjad.Staff(r"\time 4/4 c'1")
    containers = [container1, container2, container3, container4]
    auxjad.mutate(containers).sync_containers()
    assert (abjad.inspect(container1).duration()
            == abjad.inspect(container2).duration()
            == abjad.inspect(container3).duration()
            == abjad.inspect(container4).duration())
    assert format(container1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            \time 3/4
            g'4
            r2
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            \time 3/4
            g'2
            r4
        }
        """)
    assert format(container3) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            \time 3/4
            g'2.
        }
        """)
    assert format(container4) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            \time 3/4
            R1 * 3/4
        }
        """)


def test_sync_containers_08():
    container1 = abjad.Staff(r"\time 4/4 c'1 | g'4")
    container2 = abjad.Staff(r"\time 4/4 c'1 | g'2")
    container3 = abjad.Staff(r"\time 4/4 c'1 | g'2.")
    container4 = abjad.Staff(r"\time 4/4 c'1")
    containers = [container1,
                  container2,
                  container3,
                  container4,
                  ]
    auxjad.mutate(containers).sync_containers(
        use_multimeasure_rests=False,
    )
    assert (abjad.inspect(container1).duration()
            == abjad.inspect(container2).duration()
            == abjad.inspect(container3).duration()
            == abjad.inspect(container4).duration())
    assert format(container1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            \time 3/4
            g'4
            r2
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            \time 3/4
            g'2
            r4
        }
        """)
    assert format(container3) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            \time 3/4
            g'2.
        }
        """)
    assert format(container4) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            \time 3/4
            r2.
        }
        """)


def test_sync_containers_09():
    container1 = abjad.Staff(r"\time 4/4 c'1 | g'4")
    container2 = abjad.Staff(r"\time 4/4 c'1 | g'2")
    container3 = abjad.Staff(r"\time 4/4 c'1 | g'2.")
    container4 = abjad.Staff(r"\time 4/4 c'1")
    containers = [container1,
                  container2,
                  container3,
                  container4,
                  ]
    auxjad.mutate(containers).sync_containers(
        adjust_last_time_signature=False,
    )
    assert (abjad.inspect(container1).duration()
            == abjad.inspect(container2).duration()
            == abjad.inspect(container3).duration()
            == abjad.inspect(container4).duration())
    assert format(container1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            g'4
            r2
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            g'2
            r4
        }
        """)
    assert format(container3) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            g'2.
        }
        """)
    assert format(container4) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
            r2.
        }
        """)


def test_sync_containers_10():
    container1 = abjad.Staff(r"\time 4/4 c'4 d'4 e'4 f'4")
    container2 = abjad.Staff(r"\time 3/4 a2. \time 4/4 c'4")
    container3 = abjad.Staff(r"\time 5/4 g''1 ~ g''4")
    container4 = abjad.Staff(r"\time 6/8 c'2")
    containers = [container1, container2, container3, container4]
    auxjad.mutate(containers).sync_containers()
    assert (abjad.inspect(container1).duration()
            == abjad.inspect(container2).duration()
            == abjad.inspect(container3).duration()
            == abjad.inspect(container4).duration())
    assert format(container1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
            \time 1/4
            R1 * 1/4
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            a2.
            \time 2/4
            c'4
            r4
        }
        """)
    assert format(container3) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 5/4
            g''1
            ~
            g''4
        }
        """)
    assert format(container4) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 6/8
            c'2
            r4
            \time 2/4
            R1 * 1/2
        }
        """)


def test_sync_containers_11():
    container1 = abjad.Container(r"\time 4/4 g'1 | f'4")
    container2 = abjad.Container(r"\time 5/4 c'1 | \time 4/4 d'4")
    with pytest.raises(ValueError):
        assert auxjad.mutate([container1, container2]).sync_containers()


def test_sync_containers_12():
    container1 = abjad.Staff(r"\time 4/4 g'2.")
    container2 = abjad.Staff(r"\time 4/4 c'1")
    auxjad.mutate([container1, container2]).sync_containers()
    assert (abjad.inspect(container1).duration()
            == abjad.inspect(container2).duration())
    assert format(container1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            g'2.
            r4
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'1
        }
        """)


def test_sync_containers_13():
    container1 = abjad.Staff(r"\time 3/4 g'2.")
    container2 = abjad.Staff(r"\time 3/4 c'2.")
    auxjad.mutate([container1, container2]).sync_containers()
    assert (abjad.inspect(container1).duration()
            == abjad.inspect(container2).duration())
    assert format(container1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            g'2.
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2.
        }
        """)


def test_sync_containers_14():
    container1 = abjad.Staff(r"\time 5/4 g'1~g'4 | R1 * 5/4")
    container2 = abjad.Staff(r"\time 5/4 c'2.")
    auxjad.mutate([container1, container2]).sync_containers()
    assert (abjad.inspect(container1).duration()
            == abjad.inspect(container2).duration())
    assert format(container1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 5/4
            g'1
            ~
            g'4
            R1 * 5/4
        }
        """)
    assert format(container2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 5/4
            c'2.
            r2
            R1 * 5/4
        }
        """)


def test_sync_containers_15():
    container1 = abjad.Staff(r"\time 7/4 a'1 ~ a'2.")
    container2 = abjad.Staff(r"\time 3/4 c'2.")
    auxjad.mutate([container1, container2]).sync_containers()
    assert format(container2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2.
            R1 * 3/4
            \time 1/4
            R1 * 1/4
        }
        """)


def test_sync_containers_16():
    staff1 = abjad.Staff(r"\time 3/8 c'4. | d'4")
    staff2 = abjad.Staff(r"\time 3/8 c'4. | d'8")
    staff3 = abjad.Staff(r"\time 3/8 c'4. | d'16")
    staff4 = abjad.Staff(r"\time 3/8 c'4.")
    score = abjad.Score([staff1,
                         staff2,
                         staff3,
                         staff4,
                         ])
    auxjad.mutate(score).sync_containers()
    assert format(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \time 3/8
                c'4.
                \time 1/4
                d'4
            }
            \new Staff
            {
                \time 3/8
                c'4.
                \time 1/4
                d'8
                r8
            }
            \new Staff
            {
                \time 3/8
                c'4.
                \time 1/4
                d'16
                r8.
            }
            \new Staff
            {
                \time 3/8
                c'4.
                \time 1/4
                R1 * 1/4
            }
        >>
        """)
