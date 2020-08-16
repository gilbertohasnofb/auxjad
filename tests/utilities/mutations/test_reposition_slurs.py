import abjad

import auxjad


def test_reposition_slurs_01():
    staff = abjad.Staff(r"c'1( d'2 r2) r1 e'1")
    auxjad.mutate(staff[:]).reposition_slurs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            (
            d'2
            )
            r2
            r1
            e'1
        }
        """)


def test_reposition_slurs_02():
    staff = abjad.Staff(r"c'1 r2( d'2 e'1)")
    auxjad.mutate(staff[:]).reposition_slurs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            r2
            d'2
            (
            e'1
            )
        }
        """)


def test_reposition_slurs_03():
    staff = abjad.Staff(r"c'1( d'2 r2 r1) e'1")
    auxjad.mutate(staff[:]).reposition_slurs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            (
            d'2
            )
            r2
            r1
            e'1
        }
        """)


def test_reposition_slurs_04():
    staff = abjad.Staff(r"c'1 r2( r1 d'2 e'1)")
    auxjad.mutate(staff[:]).reposition_slurs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            r2
            r1
            d'2
            (
            e'1
            )
        }
        """)


def test_reposition_slurs_05():
    staff = abjad.Staff(r"c'1( d'2 e'2 f'1)")
    auxjad.mutate(staff[:]).reposition_slurs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            (
            d'2
            e'2
            f'1
            )
        }
        """)


def test_reposition_slurs_06():
    staff = abjad.Staff(r"c'1( d'2 r2 e'1 f'1)")
    auxjad.mutate(staff[:]).reposition_slurs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            (
            d'2
            )
            r2
            e'1
            (
            f'1
            )
        }
        """)


def test_reposition_slurs_07():
    staff = abjad.Staff(r"c'1( d'2 r2 e'1 f'1)")
    auxjad.mutate(staff[:]).reposition_slurs(allow_slurs_under_rests=True)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            (
            d'2
            r2
            e'1
            f'1
            )
        }
        """)


def test_reposition_slurs_08():
    staff = abjad.Staff(r"r1( c'1 d'2 r2 e'1 f'1)")
    auxjad.mutate(staff[:]).reposition_slurs(allow_slurs_under_rests=True)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r1
            c'1
            (
            d'2
            r2
            e'1
            f'1
            )
        }
        """)


def test_reposition_slurs_09():
    staff = abjad.Staff(r"c'1( r2 d'2 e'1)")
    auxjad.mutate(staff[:]).reposition_slurs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            r2
            d'2
            (
            e'1
            )
        }
        """)


def test_reposition_slurs_10():
    staff = abjad.Staff(r"c'1( d'2 r2 e'1)")
    auxjad.mutate(staff[:]).reposition_slurs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            (
            d'2
            )
            r2
            e'1
        }
        """)


def test_reposition_slurs_11():
    staff = abjad.Staff(r"c'1( d'2 r2 e'2 f'2) g'1( a'1")
    auxjad.mutate(staff[:]).reposition_slurs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            (
            d'2
            )
            r2
            e'2
            (
            f'2
            )
            g'1
            (
            a'1
            )
        }
        """)
    staff = abjad.Staff(r"c'1( d'2 r2 e'2 f'2) g'1( a'1")
    auxjad.mutate(staff[:]).reposition_slurs(
        close_unterminated_final_slur=False
    )
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            (
            d'2
            )
            r2
            e'2
            (
            f'2
            )
            g'1
            (
            a'1
        }
        """)
    staff = abjad.Staff(r"c'1( d'2 r2 e'2 f'2) g'1( r1")
    auxjad.mutate(staff[:]).reposition_slurs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            (
            d'2
            )
            r2
            e'2
            (
            f'2
            )
            g'1
            r1
        }
        """)
    staff = abjad.Staff(r"c'1( d'2 r2 e'2 f'2) g'1(")
    auxjad.mutate(staff[:]).reposition_slurs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            (
            d'2
            )
            r2
            e'2
            (
            f'2
            )
            g'1
        }
        """)


def test_reposition_slurs_12():
    staff = abjad.Staff(r"c'1( d'2) e'2) f'2( g'2( a'1)")
    auxjad.mutate(staff[:]).reposition_slurs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            (
            d'2
            )
            e'2
            f'2
            (
            g'2
            a'1
            )
        }
        """)


def test_reposition_slurs_13():
    staff = abjad.Staff(r"c'1( d'2 r2) r1 e'1")
    abjad.mutate(staff[:]).reposition_slurs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            (
            d'2
            )
            r2
            r1
            e'1
        }
        """)
