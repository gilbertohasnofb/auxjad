import abjad
import auxjad


def test_remove_repeated_time_signatures_01():
    staff = abjad.Staff(r"c'4 d'8 | c'4 d'8")
    abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
    abjad.attach(abjad.TimeSignature((3, 8)), staff[2])
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            \time 3/8
            c'4
            d'8
        }
        ''')
    staff = auxjad.remove_repeated_time_signatures(staff)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            c'4
            d'8
        }
        ''')


def test_remove_repeated_time_signatures_02():
    staff = abjad.Staff(r"c'4 d'8 | e'4. | c'4 d'8")
    abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
    abjad.attach(abjad.TimeSignature((3, 8)), staff[3])
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            e'4.
            \time 3/8
            c'4
            d'8
        }
        ''')
    staff = auxjad.remove_repeated_time_signatures(staff)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            e'4.
            c'4
            d'8
        }
        ''')


def test_remove_repeated_time_signatures_03():
    staff = abjad.Staff([abjad.Note("c'2"),
                         abjad.Chord("<d' f'>2"),
                         abjad.Tuplet((2, 3), "g2 a2 b2"),
                         ])
    abjad.attach(abjad.TimeSignature((2, 2)), staff[0])
    abjad.attach(abjad.TimeSignature((2, 2)), staff[2][0])
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 2/2
            c'2
            <d' f'>2
            \times 2/3 {
                \time 2/2
                g2
                a2
                b2
            }
        }
        ''')
    staff = auxjad.remove_repeated_time_signatures(staff)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 2/2
            c'2
            <d' f'>2
            \times 2/3 {
                g2
                a2
                b2
            }
        }
        ''')
