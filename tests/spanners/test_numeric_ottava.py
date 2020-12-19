import abjad

import auxjad


def test_numeric_ottava_01():
    staff = abjad.Staff(
        r"c'''4 d'''4 e'''4 f'''4 g'''4 a'''4 b'''4 c''''4"
    )
    auxjad.numeric_ottava(staff[:4], 1)
    auxjad.numeric_ottava(staff[4:], 2)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \ottava #1 \set Staff.ottavation = "8"
            c'''4
            d'''4
            e'''4
            f'''4
            \ottava #0
            \ottava #2 \set Staff.ottavation = "15"
            g'''4
            a'''4
            b'''4
            c''''4
            \ottava #0
        }
        """)


def test_numeric_ottava_02():
    staff = abjad.Staff(
        r"\clef bass c,4 b,,4 a,,4 g,,4 f,,4 e,,4 d,,4 c,,4"
    )
    auxjad.numeric_ottava(staff[:4], -1)
    auxjad.numeric_ottava(staff[4:], -2)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \ottava #-1 \set Staff.ottavation = "8"
            \clef "bass"
            c,4
            b,,4
            a,,4
            g,,4
            \ottava #0
            \ottava #-2 \set Staff.ottavation = "15"
            f,,4
            e,,4
            d,,4
            c,,4
            \ottava #0
        }
        """)
