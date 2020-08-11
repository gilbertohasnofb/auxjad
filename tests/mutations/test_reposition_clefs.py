import abjad

import auxjad


def test_reposition_clefs_01():
    staff = abjad.Staff(r"c'1 | d'1")
    abjad.attach(abjad.Clef('treble'), staff[0])
    abjad.attach(abjad.Clef('treble'), staff[1])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "treble"
            c'1
            \clef "treble"
            d'1
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "treble"
            c'1
            d'1
        }
        """)
    staff = abjad.Staff(r"c'1 | d'1")
    abjad.attach(abjad.Clef('treble'), staff[1])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \clef "treble"
            d'1
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            d'1
        }
        """)


def test_reposition_clefs_02():
    staff = abjad.Staff(r"c'1 | d'2 e'4 r4 | f'1")
    abjad.attach(abjad.Clef('treble'), staff[0])
    abjad.attach(abjad.Clef('treble'), staff[4])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "treble"
            c'1
            d'2
            e'4
            r4
            \clef "treble"
            f'1
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "treble"
            c'1
            d'2
            e'4
            r4
            f'1
        }
        """)
    staff = abjad.Staff(r"c'1 | d'2 e'4 r4 | f'1")
    abjad.attach(abjad.Clef('treble'), staff[4])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            d'2
            e'4
            r4
            \clef "treble"
            f'1
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            d'2
            e'4
            r4
            f'1
        }
        """)


def test_reposition_clefs_03():
    staff = abjad.Staff(r"c'1 | a,2 bf,4 r4 | f'1")
    abjad.attach(abjad.Clef('treble'), staff[0])
    abjad.attach(abjad.Clef('bass'), staff[1])
    abjad.attach(abjad.Clef('treble'), staff[4])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "treble"
            c'1
            \clef "bass"
            a,2
            bf,4
            r4
            \clef "treble"
            f'1
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "treble"
            c'1
            \clef "bass"
            a,2
            bf,4
            r4
            \clef "treble"
            f'1
        }
        """)
    staff = abjad.Staff(r"c'1 | a,2 bf,4 r4 | f'1")
    abjad.attach(abjad.Clef('bass'), staff[1])
    abjad.attach(abjad.Clef('treble'), staff[4])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \clef "bass"
            a,2
            bf,4
            r4
            \clef "treble"
            f'1
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \clef "bass"
            a,2
            bf,4
            r4
            \clef "treble"
            f'1
        }
        """)


def test_reposition_clefs_04():
    staff = abjad.Staff(r"c'1 | d'2 r2 | R1 | e'1")
    abjad.attach(abjad.Clef('treble'), staff[0])
    abjad.attach(abjad.Clef('treble'), staff[4])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "treble"
            c'1
            d'2
            r2
            R1
            \clef "treble"
            e'1
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "treble"
            c'1
            d'2
            r2
            R1
            e'1
        }
        """)
    staff = abjad.Staff(r"c'1 | d'2 r2 | R1 | e'1")
    abjad.attach(abjad.Clef('treble'), staff[4])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            d'2
            r2
            R1
            \clef "treble"
            e'1
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            d'2
            r2
            R1
            e'1
        }
        """)


def test_reposition_clefs_05():
    staff = abjad.Staff(r"c'1 | d'2 r2 | fs1")
    abjad.attach(abjad.Clef('treble'), staff[0])
    abjad.attach(abjad.Clef('bass'), staff[2])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "treble"
            c'1
            d'2
            \clef "bass"
            r2
            fs1
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "treble"
            c'1
            d'2
            r2
            \clef "bass"
            fs1
        }
        """)
    staff = abjad.Staff(r"c'1 | d'2 r2 | fs1")
    abjad.attach(abjad.Clef('bass'), staff[2])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            d'2
            \clef "bass"
            r2
            fs1
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            d'2
            r2
            \clef "bass"
            fs1
        }
        """)


def test_reposition_clefs_06():
    staff = abjad.Staff(r"c'1 | d'2 r2 | fs1")
    abjad.attach(abjad.Clef('treble'), staff[0])
    abjad.attach(abjad.Clef('bass'), staff[2])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "treble"
            c'1
            d'2
            \clef "bass"
            r2
            fs1
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs(shift_clef_to_notes=False)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "treble"
            c'1
            d'2
            \clef "bass"
            r2
            fs1
        }
        """)
    staff = abjad.Staff(r"c'1 | d'2 r2 | fs1")
    abjad.attach(abjad.Clef('bass'), staff[2])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            d'2
            \clef "bass"
            r2
            fs1
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs(shift_clef_to_notes=False)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            d'2
            \clef "bass"
            r2
            fs1
        }
        """)


def test_reposition_clefs_07():
    staff = abjad.Staff([abjad.Note("c'2"),
                         abjad.Chord("<d' f'>2"),
                         abjad.Tuplet((2, 3), "g'2 a'2 b'2"),
                         ])
    abjad.attach(abjad.Clef('treble'), staff[0])
    abjad.attach(abjad.Clef('treble'), staff[2][1])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "treble"
            c'2
            <d' f'>2
            \times 2/3 {
                g'2
                \clef "treble"
                a'2
                b'2
            }
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "treble"
            c'2
            <d' f'>2
            \times 2/3 {
                g'2
                a'2
                b'2
            }
        }
        """)
    staff = abjad.Staff([abjad.Note("c'2"),
                         abjad.Chord("<d' f'>2"),
                         abjad.Tuplet((2, 3), "g'2 a'2 b'2"),
                         ])
    abjad.attach(abjad.Clef('treble'), staff[2][1])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'2
            <d' f'>2
            \times 2/3 {
                g'2
                \clef "treble"
                a'2
                b'2
            }
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'2
            <d' f'>2
            \times 2/3 {
                g'2
                a'2
                b'2
            }
        }
        """)


def test_reposition_clefs_08():
    staff = abjad.Staff(r"c'1 | d'1")
    abjad.attach(abjad.Clef('treble'), staff[1])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \clef "treble"
            d'1
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            d'1
        }
        """)


def test_reposition_clefs_09():
    staff = abjad.Staff(r"c1 | d1")
    abjad.attach(abjad.Clef('bass'), staff[1])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c1
            \clef "bass"
            d1
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs(implicit_clef=abjad.Clef('bass'))
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c1
            d1
        }
        """)


def test_reposition_clefs_10():
    staff = abjad.Staff(r"c'1 | r1 | d'1")
    abjad.attach(abjad.Clef('bass'), staff[1])
    abjad.attach(abjad.Clef('treble'), staff[2])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \clef "bass"
            r1
            \clef "treble"
            d'1
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs(shift_clef_to_notes=False)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            \clef "bass"
            r1
            \clef "treble"
            d'1
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'1
            r1
            d'1
        }
        """)


def test_reposition_clefs_11():
    staff = abjad.Staff(r"\time 3/4 c'2. | d'4 r2 | R1 * 3/4 | e'2.")
    abjad.attach(abjad.Clef('treble'), staff[0])
    abjad.attach(abjad.Clef('bass'), staff[2])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            \clef "treble"
            c'2.
            d'4
            \clef "bass"
            r2
            R1 * 3/4
            e'2.
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs(shift_clef_to_notes=False)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            \clef "treble"
            c'2.
            d'4
            \clef "bass"
            r2
            R1 * 3/4
            e'2.
        }
        """)
    auxjad.mutate(staff[:]).reposition_clefs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            \clef "treble"
            c'2.
            d'4
            r2
            R1 * 3/4
            \clef "bass"
            e'2.
        }
        """)


def test_reposition_clefs_12():
    staff = abjad.Staff(r"c'1 | d'1")
    abjad.attach(abjad.Clef('treble'), staff[0])
    abjad.attach(abjad.Clef('treble'), staff[1])
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "treble"
            c'1
            \clef "treble"
            d'1
        }
        """)
    abjad.mutate(staff[:]).reposition_clefs()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \clef "treble"
            c'1
            d'1
        }
        """)
