import abjad

import auxjad


def test_merge_hairpins_01():
    staff = abjad.Staff(r"c'4\pp\< d'4 e'4\p\< f'4 g'1\mp")
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            \<
            d'4
            e'4
            \p
            \<
            f'4
            g'1
            \mp
        }
        """
    )
    auxjad.mutate.merge_hairpins(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            \<
            d'4
            e'4
            f'4
            g'1
            \mp
        }
        """
    )


def test_merge_hairpins_02():
    staff = abjad.Staff(r"c'4\ff\> d'4 e'4\mf\> f'4 g'1\pp")
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \ff
            \>
            d'4
            e'4
            \mf
            \>
            f'4
            g'1
            \pp
        }
        """
    )
    auxjad.mutate.merge_hairpins(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \ff
            \>
            d'4
            e'4
            f'4
            g'1
            \pp
        }
        """
    )


def test_merge_hairpins_03():
    staff = abjad.Staff(r"c'4\pp\< d'4 e'4\mf\> f'4 g'1\pp")
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            \<
            d'4
            e'4
            \mf
            \>
            f'4
            g'1
            \pp
        }
        """
    )
    auxjad.mutate.merge_hairpins(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            \<
            d'4
            e'4
            \mf
            \>
            f'4
            g'1
            \pp
        }
        """
    )


def test_merge_hairpins_04():
    staff = abjad.Staff(
        r"c'1\pp\< d'2\f d'2\< e'1\ff f'1\f\> g'2\mp g'2\> a'1\! b'1\ppp"
    )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \pp
            \<
            d'2
            \f
            d'2
            \<
            e'1
            \ff
            f'1
            \f
            \>
            g'2
            \mp
            g'2
            \>
            a'1
            \!
            b'1
            \ppp
        }
        """
    )
    auxjad.mutate.merge_hairpins(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \pp
            \<
            d'2
            \f
            d'2
            \<
            e'1
            \ff
            f'1
            \f
            \>
            g'2
            \mp
            g'2
            \>
            a'1
            \!
            b'1
            \ppp
        }
        """
    )


def test_merge_hairpins_05():
    staff = abjad.Staff(
        r"c'4\pp\< d'4 e'4\p\< f'4 g'4\mp\< a'4 b'4\mf\< c''4"
        r"d''4\f\> c''4 b'4\mf\> a'4 g'4\mp\> f'4 e'4\p\> d'4"
        r"c'1\pp"
    )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            \<
            d'4
            e'4
            \p
            \<
            f'4
            g'4
            \mp
            \<
            a'4
            b'4
            \mf
            \<
            c''4
            d''4
            \f
            \>
            c''4
            b'4
            \mf
            \>
            a'4
            g'4
            \mp
            \>
            f'4
            e'4
            \p
            \>
            d'4
            c'1
            \pp
        }
        """
    )
    auxjad.mutate.merge_hairpins(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            \<
            d'4
            e'4
            f'4
            g'4
            a'4
            b'4
            c''4
            d''4
            \f
            \>
            c''4
            b'4
            a'4
            g'4
            f'4
            e'4
            d'4
            c'1
            \pp
        }
        """
    )


def test_merge_hairpins_06():
    staff = abjad.Staff(r"c'4\pp\< d'4 e'4\p\> f'4 g'1\pp")
    abjad.mutate.merge_hairpins(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            \<
            d'4
            e'4
            \p
            \>
            f'4
            g'1
            \pp
        }
        """
    )


def test_merge_hairpins_07():
    staff = abjad.Staff(r"c'4\pp\< d'4 e'4\p\< f'4 g'1\mp")
    abjad.mutate.merge_hairpins(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            \<
            d'4
            e'4
            f'4
            g'1
            \mp
        }
        """
    )
