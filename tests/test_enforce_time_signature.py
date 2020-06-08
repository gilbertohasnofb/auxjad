import abjad
import pytest
import auxjad


def test_enforce_time_signature_01():
    staff = abjad.Staff(r"c'1 d'1")
    time_signatures = abjad.TimeSignature((2, 4))
    auxjad.enforce_time_signature(staff, time_signatures)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            c'2
            ~
            c'2
            d'2
            ~
            d'2
        }
        """)


def test_enforce_time_signature_02():
    staff = abjad.Staff(r"c'1 d'1")
    auxjad.enforce_time_signature(staff, (3, 4))
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2.
            ~
            c'4
            d'2
            ~
            d'2
            r4
        }
        """)


def test_enforce_time_signature_03():
    staff = abjad.Staff(r"c'1 d'1 e'1 f'1")
    auxjad.enforce_time_signature(staff,
                          abjad.TimeSignature((3, 4)),
                          close_container=True,
                          )
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2.
            ~
            c'4
            d'2
            ~
            d'2
            e'4
            ~
            e'2.
            f'2.
            ~
            \time 1/4
            f'4
        }
        """)


def test_enforce_time_signature_04():
    staff = abjad.Staff(r"c'1 d'1 e'1 f'1")
    auxjad.enforce_time_signature(staff,
                          abjad.TimeSignature((3, 4)),
                          fill_with_rests=False,
                          )
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2.
            ~
            c'4
            d'2
            ~
            d'2
            e'4
            ~
            e'2.
            f'2.
            ~
            f'4
        }
        """)


def test_enforce_time_signature_05():
    staff = abjad.Staff(r"c'1 d'1")
    time_signatures = [abjad.TimeSignature((3, 4)),
                       abjad.TimeSignature((5, 4)),
                       ]
    auxjad.enforce_time_signature(staff, time_signatures)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'2.
            ~
            \time 5/4
            c'4
            d'1
        }
        """)


def test_enforce_time_signature_06():
    staff = abjad.Staff(r"c'1 d'1 e'1 f'1")
    time_signatures = [(2, 4),
                       (2, 4),
                       (4, 4),
                       ]
    auxjad.enforce_time_signature(staff, time_signatures)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            c'2
            ~
            c'2
            \time 4/4
            d'1
            e'1
            f'1
        }
        """)


def test_enforce_time_signature_07():
    staff = abjad.Staff(r"c'1 d'1 e'1 f'1")
    time_signatures = [abjad.TimeSignature((3, 8)),
                       abjad.TimeSignature((2, 8)),
                       ]
    auxjad.enforce_time_signature(staff,
                                  time_signatures,
                                  cyclic=True,
                                  )
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/8
            c'4.
            ~
            \time 2/8
            c'4
            ~
            \time 3/8
            c'4.
            \time 2/8
            d'4
            ~
            \time 3/8
            d'4.
            ~
            \time 2/8
            d'4
            ~
            \time 3/8
            d'8
            e'4
            ~
            \time 2/8
            e'4
            ~
            \time 3/8
            e'4.
            ~
            \time 2/8
            e'8
            f'8
            ~
            \time 3/8
            f'4.
            ~
            \time 2/8
            f'4
            ~
            \time 3/8
            f'4
            r8
        }
        """)


def test_enforce_time_signature_08():
    staff = abjad.Staff(r"\times 2/3 {c'2 d'2 e'2} f'1")
    time_signatures = [abjad.TimeSignature((2, 4)),
                       abjad.TimeSignature((3, 4)),
                       ]
    auxjad.enforce_time_signature(staff, time_signatures)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                \time 2/4
                c'2
                d'4
                ~
            }
            \times 2/3 {
                \time 3/4
                d'4
                e'2
            }
            f'4
            ~
            f'2.
        }
        """)


def test_enforce_time_signature_09():
    staff = staff = abjad.Staff(r"\time 3/4 c'2. d'2. e'2. f'2.")
    time_signatures = [abjad.TimeSignature((5, 8)),
                       abjad.TimeSignature((1, 16)),
                       abjad.TimeSignature((2, 4)),
                       ]
    auxjad.enforce_time_signature(staff,
                                  time_signatures,
                                  cyclic=True,
                                  )
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 5/8
            c'4.
            ~
            c'4
            ~
            \time 1/16
            c'16
            ~
            \time 2/4
            c'16
            d'4..
            ~
            \time 5/8
            d'4
            ~
            d'16
            e'4
            ~
            e'16
            ~
            \time 1/16
            e'16
            ~
            \time 2/4
            e'4.
            f'8
            ~
            \time 5/8
            f'2
            ~
            f'8
        }
        """)


def test_enforce_time_signature_10():
    staff = abjad.Staff(r"c'2. d'4 ~ d'2 e'2 ~ e'4 f'2.")
    time_signatures = [abjad.TimeSignature((3, 4), partial=(1, 4)),
                       abjad.TimeSignature((3, 4)),
                       abjad.TimeSignature((4, 4)),
                       ]
    auxjad.enforce_time_signature(staff, time_signatures)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \partial 4
            \time 3/4
            c'4
            ~
            c'2
            d'4
            ~
            d'2
            e'4
            ~
            \time 4/4
            e'2
            f'2
            ~
            f'4
            r2.
        }
        """)

def test_enforce_time_signature_11():
    staff = abjad.Staff(r"c'1 d'1 e'1 f'1")
    time_signatures = [(2, 4),
                       None,
                       None,
                       (3, 4),
                       None,
                       (4, 4),
                       ]
    auxjad.enforce_time_signature(staff, time_signatures)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            c'2
            ~
            c'2
            d'2
            ~
            \time 3/4
            d'2
            e'4
            ~
            e'2.
            \time 4/4
            f'1
        }
        """)


def test_enforce_time_signature_12():
    staff = abjad.Staff(r"r8 c'1 d'1 e'1 f'1")
    time_signatures = [abjad.TimeSignature((2, 4), partial=(1, 8)),
                       None,
                       None,
                       abjad.TimeSignature((3, 4)),
                       None,
                       abjad.TimeSignature((4, 4)),
                       ]
    auxjad.enforce_time_signature(staff, time_signatures)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \partial 8
            \time 2/4
            r8
            c'2
            ~
            c'2
            d'2
            ~
            \time 3/4
            d'2
            e'4
            ~
            e'2.
            \time 4/4
            f'1
        }
        """)


def test_enforce_time_signature_13():
    staff = abjad.Staff(r"c'1 d'1 e'1 f'1")
    time_signatures = [None,
                       (4, 4),
                       ]
    with pytest.raises(ValueError):
        auxjad.enforce_time_signature(staff, time_signatures)
