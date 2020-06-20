import random
import abjad
import pytest
import auxjad


def test_Shuffler_01():
    random.seed(87234)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    shuffler = auxjad.Shuffler(container)
    assert format(shuffler) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            d'4
            c'4
            f'4
            e'4
        }
        """)
    notes = shuffler.current_window
    with pytest.raises(AttributeError):
        shuffler.current_window = abjad.Container(r"c''2 e''2")
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            d'4
            c'4
            f'4
            e'4
        }
        """)


def test_Shuffler_02():
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 \time 2/4 f'4 g'4")
    shuffler = auxjad.Shuffler(container,
                               output_single_measure=False,
                               disable_rewrite_meter=False,
                               force_time_signatures=False,
                               omit_time_signatures=True,
                               boundary_depth=0,
                               maximum_dot_count=1,
                               rewrite_tuplets=False,
                               )
    assert not shuffler.output_single_measure
    assert not shuffler.disable_rewrite_meter
    assert not shuffler.force_time_signatures
    assert shuffler.omit_time_signatures
    assert shuffler.boundary_depth == 0
    assert shuffler.maximum_dot_count == 1
    assert not shuffler.rewrite_tuplets
    shuffler.output_single_measure = True
    shuffler.disable_rewrite_meter = True
    shuffler.force_time_signatures = True
    shuffler.omit_time_signatures = False
    shuffler.boundary_depth = 1
    shuffler.maximum_dot_count = 2
    shuffler.rewrite_tuplets = True
    assert shuffler.output_single_measure
    assert shuffler.disable_rewrite_meter
    assert shuffler.force_time_signatures
    assert not shuffler.omit_time_signatures
    assert shuffler.boundary_depth == 1
    assert shuffler.maximum_dot_count == 2
    assert shuffler.rewrite_tuplets


def test_Shuffler_03():
    random.seed(99961)
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 \time 2/4 f'4 g'4")
    shuffler = auxjad.Shuffler(container,
                               output_single_measure=True,
                               )
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 5/4
            f'4
            d'4
            e'4
            g'4
            c'4
        }
        """)


def test_Shuffler_04():
    random.seed(17453)
    container = abjad.Container(r"\time 3/4 c'16 d'4.. e'4 \time 2/4 f'2")
    shuffler = auxjad.Shuffler(container,
                               output_single_measure=True,
                               disable_rewrite_meter=True,
                               )
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 5/4
            d'4..
            f'2
            c'16
            e'4
        }
        """)


def test_Shuffler_05():
    random.seed(18892)
    container = abjad.Container(r"\time 3/4 c'16 d'4.. e'4 | r4 f'2")
    shuffler = auxjad.Shuffler(container)
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            d'4..
            e'16
            ~
            e'8.
            f'16
            ~
            f'4..
            r16
            r8.
            c'16
        }
        """)
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'16
            e'8.
            ~
            e'16
            f'4..
            ~
            f'16
            r8.
            r16
            d'4..
        }
        """)
    shuffler.force_time_signatures = True
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            d'4..
            r16
            r8.
            c'16
            f'2
            e'4
        }
        """)


def test_Shuffler_06():
    random.seed(98231)
    container = abjad.Container(r"\time 2/4 c'16 d'4.. | r4 e'8. f'16")
    shuffler = auxjad.Shuffler(container)
    notes = shuffler.output_n(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            d'4..
            f'16
            c'16
            e'8.
            r4
            d'4..
            e'16
            ~
            e'8
            f'16
            r16
            r8.
            c'16
            r4
            d'4
            ~
            d'8.
            f'16
            c'16
            e'8.
        }
        """)


def test_Shuffler_07():
    random.seed(77347)
    container = abjad.Container(
        r"\time 3/4 c'16 d'8. ~ d'4 e'4 r4 f'4 ~ f'8.. g'32")
    shuffler = auxjad.Shuffler(container)
    notes = shuffler.shuffle_pitches()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
    r"""
    \new Staff
    {
        \time 3/4
        e'16
        c'8.
        ~
        c'4
        d'4
        r4
        f'4
        ~
        f'8..
        g'32
    }
    """)


def test_Shuffler_08():
    random.seed(17231)
    container = abjad.Container(r"\time 5/4 r4 \times 2/3 {c'4 d'2} e'4. f'8")
    shuffler = auxjad.Shuffler(container)
    notes = shuffler.output_n_shuffled_pitches(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
    r"""
    \new Staff
    {
        \time 5/4
        r4
        \times 2/3 {
            f'4
            e'2
        }
        d'4.
        c'8
        r4
        \times 2/3 {
            d'4
            c'2
        }
        f'4.
        e'8
        r4
        \times 2/3 {
            d'4
            f'2
        }
        c'4.
        e'8
    }
    """)


def test_Shuffler_09():
    container = abjad.Container(
        r"\time 3/4 c'16 d'8. ~ d'4 e'4 r4 f'4 ~ f'8.. g'32")
    shuffler = auxjad.Shuffler(container)
    notes = shuffler.rotate_pitches()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
    r"""
    \new Staff
    {
        \time 3/4
        d'16
        e'8.
        ~
        e'4
        f'4
        r4
        g'4
        ~
        g'8..
        c'32
    }
    """)


def test_Shuffler_10():
    container = abjad.Container(
        r"\time 3/4 c'16 d'8. ~ d'4 e'4 r4 f'4 ~ f'8.. g'32")
    shuffler = auxjad.Shuffler(container)
    notes = shuffler.rotate_pitches(anticlockwise=True, n_rotations=2)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
    r"""
    \new Staff
    {
        \time 3/4
        f'16
        g'8.
        ~
        g'4
        c'4
        r4
        d'4
        ~
        d'8..
        e'32
    }
    """)


def test_Shuffler_11():
    container = abjad.Container(r"\time 5/4 r4 \times 2/3 {c'4 d'2} e'4. f'8")
    shuffler = auxjad.Shuffler(container)
    notes = shuffler.output_n_rotated_pitches(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
    r"""
    \new Staff
    {
        \time 5/4
        r4
        \times 2/3 {
            d'4
            e'2
        }
        f'4.
        c'8
        r4
        \times 2/3 {
            e'4
            f'2
        }
        c'4.
        d'8
        r4
        \times 2/3 {
            f'4
            c'2
        }
        d'4.
        e'8
    }
    """)


def test_Shuffler_12():
    random.seed(87234)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    shuffler = auxjad.Shuffler(container)
    notes = shuffler.shuffle()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            d'4
            c'4
            f'4
            e'4
        }
        """)


def test_Shuffler_13():
    random.seed(18892)
    container = abjad.Container(r"\time 3/4 c'16 d'4.. e'4 | r4 f'2")
    shuffler = auxjad.Shuffler(container,
                               omit_time_signatures=True,
                               )
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            d'4..
            e'16
            ~
            e'8.
            f'16
            ~
            f'4..
            r16
            r8.
            c'16
        }
        """)
    assert shuffler.omit_time_signatures
    shuffler.omit_time_signatures = False
    assert not shuffler.omit_time_signatures


def test_Shuffler_14():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    shuffler = auxjad.Shuffler(container)
    assert format(shuffler.contents) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    shuffler()
    assert format(shuffler.contents) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    shuffler.contents = abjad.Container(r"cs2 ds2")
    assert format(shuffler.contents) == abjad.String.normalize(
        r"""
        {
            cs2
            ds2
        }
        """)


def test_Shuffler_15():
    container = abjad.Container(r"c'2 d'2")
    shuffler = auxjad.Shuffler(container)
    assert len(shuffler) == 2
    container = abjad.Container(r"c'4 d'4 e'4 f'4 ~ | f'2 g'2")
    shuffler = auxjad.Shuffler(container)
    assert len(shuffler) == 5


def test_Shuffler_16():
    container = abjad.Container(r"c'2 \times 2/3 {d'4 e'2}")
    shuffler = auxjad.Shuffler(container)
    with pytest.raises(TypeError):
        notes = shuffler()


def test_Shuffler_17():
    random.seed(98604)
    container = abjad.Container(r"c'4. d'8 e'2")
    shuffler = auxjad.Shuffler(container)
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            e'2
            c'4.
            d'8
        }
        """)
    random.seed(98604)
    shuffler = auxjad.Shuffler(container,
                               boundary_depth=1,
                               )
    notes = shuffler()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            e'2
            c'4
            ~
            c'8
            d'8
        }
        """)
