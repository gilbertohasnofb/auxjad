import abjad

import auxjad


def test_reposition_dynamics_01():
    staff = abjad.Staff(r"c'1\p d'2 r2\f r1 e'1")
    auxjad.mutate(staff[:]).reposition_dynamics()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            d'2
            r2
            r1
            e'1
            \f
        }
        """)


def test_reposition_dynamics_02():
    staff = abjad.Staff(r"c'1\p d'1 e'1\f e'1")
    auxjad.mutate(staff[:]).reposition_dynamics()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            d'1
            e'1
            \f
            e'1
        }
        """)


def test_reposition_dynamics_03():
    staff = abjad.Staff(r"c'1\p d'2 r2\f r1\mf e'1\pp")
    auxjad.mutate(staff[:]).reposition_dynamics()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            d'2
            r2
            r1
            e'1
            \pp
        }
        """)


def test_reposition_dynamics_04():
    staff = abjad.Staff(r"c'1\p d'1 r1\f e'1\p")
    auxjad.mutate(staff[:]).reposition_dynamics()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            d'1
            r1
            e'1
        }
        """)


def test_reposition_dynamics_05():
    staff = abjad.Staff(r"c'1\p d'1 e'1\p f'1")
    auxjad.mutate(staff[:]).reposition_dynamics()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            d'1
            e'1
            f'1
        }
        """)
    staff = abjad.Staff(r"c'1\p d'1 e'1\p f'1")
    auxjad.mutate(staff[:]).reposition_dynamics(remove_repeated_dynamics=False)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            d'1
            e'1
            \p
            f'1
        }
        """)


def test_reposition_dynamics_06():
    staff = abjad.Staff(r"c'1\p d'1 r1\f e'1\p")
    auxjad.mutate(staff[:]).reposition_dynamics()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            d'1
            r1
            e'1
        }
        """)
    staff = abjad.Staff(r"c'1\p d'1 r1\f e'1\p")
    auxjad.mutate(staff[:]).reposition_dynamics(remove_repeated_dynamics=False)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            d'1
            r1
            e'1
            \p
        }
        """)


def test_reposition_dynamics_07():
    staff = abjad.Staff(r"c'1\p\< d'2 r2 r1\f e'1")
    auxjad.mutate(staff[:]).reposition_dynamics()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            \<
            d'2
            r2
            \!
            r1
            e'1
            \f
        }
        """)


def test_reposition_dynamics_08():
    staff = abjad.Staff(r"c'1\p\< d'2 r2 r1\f e'1")
    auxjad.mutate(staff[:]).reposition_dynamics(
        allow_hairpins_under_rests=True,
    )
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            \<
            d'2
            r2
            r1
            e'1
            \f
        }
        """)


def test_reposition_dynamics_09():
    staff = abjad.Staff(r"c'1\p\> d'1\f\> e'1\p")
    auxjad.mutate(staff[:]).reposition_dynamics()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            d'1
            \f
            \>
            e'1
            \p
        }
    """)
    staff = abjad.Staff(r"c'1\p\> d'1\f\> e'1\p")
    auxjad.mutate(staff[:]).reposition_dynamics(check_hairpin_trends=False)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            \>
            d'1
            \f
            \>
            e'1
            \p
        }
        """)


def test_reposition_dynamics_10():
    staff = abjad.Staff(r"c'1\p\> d'1\! e'1\f\> f'1\p")
    auxjad.mutate(staff[:]).reposition_dynamics()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            \>
            d'1
            \!
            e'1
            \f
            \>
            f'1
            \p
        }
    """)


def test_reposition_dynamics_11():
    staff = abjad.Staff(r"c'1 d'1 e'1 r1\mf r1\ff f'1 r1 g'1")
    abjad.attach(abjad.Dynamic('niente', hide=True), staff[0])
    abjad.attach(abjad.Dynamic('niente', hide=True), staff[7])
    abjad.attach(abjad.StartHairpin('o<'), staff[0])
    abjad.attach(abjad.StartHairpin('>o'), staff[4])
    abjad.attach(abjad.StopHairpin(), staff[7])
    auxjad.mutate(staff[:]).reposition_dynamics()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            - \tweak circled-tip ##t
            \<
            d'1
            e'1
            r1
            \mf
            r1
            f'1
            \ff
            - \tweak circled-tip ##t
            \>
            r1
            \!
            g'1
        }
        """)


def test_reposition_dynamics_12():
    staff = abjad.Staff(r"c'1\p d'1\f\> e'1\ff\< r1\fff f'1\p\> g'1\ppp")
    abjad.attach(abjad.StartHairpin('--'), staff[0])
    auxjad.mutate(staff[:]).reposition_dynamics()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            - \tweak stencil #constante-hairpin
            \<
            d'1
            \f
            e'1
            \ff
            \<
            r1
            \fff
            f'1
            \p
            \>
            g'1
            \ppp
        }
        """)


def test_reposition_dynamics_13():
    staff = abjad.Staff(r"c'1\p R1\f d'1")
    auxjad.mutate(staff[:]).reposition_dynamics()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            R1
            d'1
            \f
        }
        """)


def test_reposition_dynamics_14():
    staff = abjad.Staff(r"c'1\p\< d'2 r2\f r1 e'1")
    auxjad.mutate(staff[:]).reposition_dynamics()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            \<
            d'2
            r2
            \f
            r1
            e'1
        }
        """)
    staff = abjad.Staff(r"c'1\p\< d'2 r2\f r1 e'1")
    auxjad.mutate(staff[:]).reposition_dynamics(
        allow_hairpin_to_rest_with_dynamic=False,
    )
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            \<
            d'2
            r2
            \!
            r1
            e'1
            \f
        }
        """)


def test_reposition_dynamics_15():
    staff = abjad.Staff(r"c'1\p d'2 r2\f r1 e'1")
    abjad.mutate(staff[:]).reposition_dynamics()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \p
            d'2
            r2
            r1
            e'1
            \f
        }
        """)
