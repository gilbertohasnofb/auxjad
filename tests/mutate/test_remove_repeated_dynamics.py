import abjad

import auxjad


def test_remove_repeated_dynamics_01():
    staff = abjad.Staff(r"c'4\pp d'8\pp | c'4\f d'8\f")
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            d'8
            \pp
            c'4
            \f
            d'8
            \f
        }
        """
    )
    auxjad.mutate.remove_repeated_dynamics(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            d'8
            c'4
            \f
            d'8
        }
        """
    )


def test_remove_repeated_dynamics_02():
    staff = abjad.Staff(r"c'4\p d'8 | e'4.\p | c'4\p d'8\f")
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \p
            d'8
            e'4.
            \p
            c'4
            \p
            d'8
            \f
        }
        """
    )
    auxjad.mutate.remove_repeated_dynamics(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \p
            d'8
            e'4.
            c'4
            d'8
            \f
        }
        """
    )


def test_remove_repeated_dynamics_03():
    staff = abjad.Staff([abjad.Note("c'2"),
                         abjad.Chord("<d' f'>2"),
                         abjad.Tuplet((2, 3), "g2 a2 b2"),
                         ])
    abjad.attach(abjad.Dynamic('ppp'), staff[0])
    abjad.attach(abjad.Dynamic('ppp'), staff[1])
    abjad.attach(abjad.Dynamic('ppp'), staff[2][0])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'2
            \ppp
            <d' f'>2
            \ppp
            \times 2/3
            {
                g2
                \ppp
                a2
                b2
            }
        }
        """
    )
    auxjad.mutate.remove_repeated_dynamics(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'2
            \ppp
            <d' f'>2
            \times 2/3
            {
                g2
                a2
                b2
            }
        }
        """
    )


def test_remove_repeated_dynamics_04():
    staff = abjad.Staff(r"c'4\pp\< d'8\f\> | c'4\f d'8\f")
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            \<
            d'8
            \f
            \>
            c'4
            \f
            d'8
            \f
        }
        """
    )
    auxjad.mutate.remove_repeated_dynamics(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            \<
            d'8
            \f
            \>
            c'4
            \f
            d'8
        }
        """
    )


def test_remove_repeated_dynamics_05():
    staff = abjad.Staff(r"c'4\pp\< d'8\f\> | c'4\f d'8\f")
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            \<
            d'8
            \f
            \>
            c'4
            \f
            d'8
            \f
        }
        """
    )
    auxjad.mutate.remove_repeated_dynamics(staff[:], ignore_hairpins=True)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            \<
            d'8
            \f
            \>
            c'4
            d'8
        }
        """
    )


def test_remove_repeated_dynamics_06():
    staff = abjad.Staff(r"c'4\pp r2. | c'1\pp")
    auxjad.mutate.remove_repeated_dynamics(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            r2.
            c'1
        }
        """
    )
    staff = abjad.Staff(r"c'4\pp r2. | c'1\pp")
    auxjad.mutate.remove_repeated_dynamics(staff[:], reset_after_rests=True)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            r2.
            c'1
            \pp
        }
        """
    )


def test_remove_repeated_dynamics_07():
    staff = abjad.Staff(r"c'4\pp r2. | c'1\pp")
    auxjad.mutate.remove_repeated_dynamics(staff[:],
                                           reset_after_rests=True,
                                           reset_after_duration=(4, 4),
                                           )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            r2.
            c'1
        }
        """
    )
    staff = abjad.Staff(r"c'4\pp r2. | c'1\pp")
    auxjad.mutate.remove_repeated_dynamics(staff[:],
                                           reset_after_rests=True,
                                           reset_after_duration=2 / 4,
                                           )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            r2.
            c'1
            \pp
        }
        """
    )


def test_remove_repeated_dynamics_08():
    staff = abjad.Staff(r"c'4\pp r2. | R1 | c'1\pp")
    auxjad.mutate.remove_repeated_dynamics(
        staff[:],
        reset_after_rests=True,
        reset_after_duration=abjad.Duration(4, 4),
    )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            r2.
            R1
            c'1
            \pp
        }
        """
    )
    staff = abjad.Staff(r"c'4\pp r2. | R1 | c'1\pp")
    auxjad.mutate.remove_repeated_dynamics(staff[:],
                                           reset_after_rests=True,
                                           reset_after_duration=2,
                                           )
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            r2.
            R1
            c'1
        }
        """
    )


def test_remove_repeated_dynamics_09():
    staff = abjad.Staff(r"c'4\pp d'8\pp | c'4\f d'8\f")
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            d'8
            \pp
            c'4
            \f
            d'8
            \f
        }
        """
    )
    abjad.mutate.remove_repeated_dynamics(staff[:])
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            d'8
            c'4
            \f
            d'8
        }
        """
    )


def test_remove_repeated_dynamics_10():
    staff1 = abjad.Staff(r"c'4\pp\> d' e' f'\! c'\pp\> d' e' f'\! g'1\pp")
    staff2 = abjad.Staff(r"c'4\pp d'\> e' f'\! c'\pp d'\> e' f'\! g'1\pp")
    abjad.mutate.remove_repeated_dynamics(staff1[:])
    abjad.mutate.remove_repeated_dynamics(staff2[:])
    assert abjad.lilypond(staff1) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            \>
            d'4
            e'4
            f'4
            \!
            c'4
            \pp
            \>
            d'4
            e'4
            f'4
            \!
            g'1
            \pp
        }
        """
    )
    assert abjad.lilypond(staff2) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            \pp
            d'4
            \>
            e'4
            f'4
            \!
            c'4
            \pp
            d'4
            \>
            e'4
            f'4
            \!
            g'1
            \pp
        }

        """
    )
