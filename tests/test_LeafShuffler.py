import random
import abjad
import auxjad


def test_LeafShuffler_01():
    random.seed(87234)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    assert repr(container) == 'Container("c\'4 d\'4 e\'4 f\'4")'
    shuffler = auxjad.LeafShuffler(container)
    music = shuffler()
    staff = abjad.Staff(music)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 4/4
            d'4
            c'4
            f'4
            e'4
        }
        ''')
    music = shuffler.current_container
    staff = abjad.Staff(music)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 4/4
            d'4
            c'4
            f'4
            e'4
        }
        ''')


def test_LeafShuffler_02():
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 \time 2/4 f'4 g'4")
    shuffler = auxjad.LeafShuffler(container,
                                   output_single_measure=False,
                                   disable_rewrite_meter=False,
                                   force_time_signatures=False,
                                   )
    assert not shuffler.output_single_measure
    assert not shuffler.disable_rewrite_meter
    assert not shuffler.force_time_signatures
    shuffler.output_single_measure = True
    shuffler.disable_rewrite_meter = True
    shuffler.force_time_signatures = True
    assert shuffler.output_single_measure
    assert shuffler.disable_rewrite_meter
    assert shuffler.force_time_signatures


def test_LeafShuffler_03():
    random.seed(99961)
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 \time 2/4 f'4 g'4")
    shuffler = auxjad.LeafShuffler(container,
                                   output_single_measure=True,
                                   )
    music = shuffler()
    staff = abjad.Staff(music)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 5/4
            f'4
            d'4
            e'4
            g'4
            c'4
        }
        ''')


def test_LeafShuffler_04():
    random.seed(17453)
    container = abjad.Container(r"\time 3/4 c'16 d'4.. e'4 \time 2/4 f'2")
    shuffler = auxjad.LeafShuffler(container,
                                   output_single_measure=True,
                                   disable_rewrite_meter=True,
                                   )
    music = shuffler()
    staff = abjad.Staff(music)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 5/4
            d'4..
            f'2
            c'16
            e'4
        }
        ''')


def test_LeafShuffler_05():
    random.seed(18892)
    container = abjad.Container(r"\time 3/4 c'16 d'4.. e'4 | r4 f'2")
    shuffler = auxjad.LeafShuffler(container)
    music = shuffler()
    staff = abjad.Staff(music)
    assert format(staff) == abjad.String.normalize(
        r'''
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
        ''')
    music = shuffler()
    staff = abjad.Staff(music)
    assert format(staff) == abjad.String.normalize(
        r'''
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
        ''')
    shuffler.force_time_signatures = True
    music = shuffler()
    staff = abjad.Staff(music)
    assert format(staff) == abjad.String.normalize(
        r'''
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
        ''')


def test_LeafShuffler_06():
    random.seed(98231)
    container = abjad.Container(r"\time 2/4 c'16 d'4.. | r4 e'8. f'16")
    shuffler = auxjad.LeafShuffler(container)
    music = shuffler.output_n(3)
    staff = abjad.Staff(music)
    assert format(staff) == abjad.String.normalize(
        r'''
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
        ''')


def test_LeafShuffler_07():
    random.seed(77347)
    container = abjad.Container(r"\time 3/4 c'16 d'4.. | r4 e'8. f'16")
    shuffler = auxjad.LeafShuffler(container)
    music = shuffler.shuffle_pitches()
    staff = abjad.Staff(music)
    assert format(staff) == abjad.String.normalize(
    r'''
    \new Staff
    {
        \time 3/4
        e'16
        c'4..
        r4
        d'8.
        f'16
    }
    ''')


def test_LeafShuffler_08():
    random.seed(17231)
    container = abjad.Container(r"\times 2/3 {\time 5/4 c'4 d'2} r4 e'4. f'8")
    shuffler = auxjad.LeafShuffler(container)
    music = shuffler.output_n_shuffled_pitches(3)
    staff = abjad.Staff(music)
    assert format(staff) == abjad.String.normalize(
    r'''
    \new Staff
    {
        \times 2/3 {
            \time 5/4
            f'4
            e'2
        }
        r4
        d'4.
        c'8
        \times 2/3 {
            d'4
            c'2
        }
        r4
        f'4.
        e'8
        \times 2/3 {
            d'4
            f'2
        }
        r4
        c'4.
        e'8
    }
    ''')


def test_LeafShuffler_09():
    container = abjad.Container(r"\time 3/4 c'16 d'4.. | r4 e'8. f'16")
    shuffler = auxjad.LeafShuffler(container)
    music = shuffler.rotate_pitches()
    staff = abjad.Staff(music)
    assert format(staff) == abjad.String.normalize(
    r'''
    \new Staff
    {
        \time 3/4
        d'16
        e'4..
        r4
        f'8.
        c'16
    }
    ''')


def test_LeafShuffler_10():
    container = abjad.Container(r"\time 3/4 c'16 d'4.. | r4 e'8. f'16")
    shuffler = auxjad.LeafShuffler(container)
    music = shuffler.rotate_pitches(anticlockwise=True, n_rotations=2)
    staff = abjad.Staff(music)
    assert format(staff) == abjad.String.normalize(
    r'''
    \new Staff
    {
        \time 3/4
        e'16
        f'4..
        r4
        c'8.
        d'16
    }
    ''')


def test_LeafShuffler_11():
    container = abjad.Container(r"\times 2/3 {\time 5/4 c'4 d'2} r4 e'4. f'8")
    shuffler = auxjad.LeafShuffler(container)
    music = shuffler.output_n_rotated_pitches(3)
    staff = abjad.Staff(music)
    assert format(staff) == abjad.String.normalize(
    r'''
    \new Staff
    {
        \times 2/3 {
            \time 5/4
            d'4
            e'2
        }
        r4
        f'4.
        c'8
        \times 2/3 {
            e'4
            f'2
        }
        r4
        c'4.
        d'8
        \times 2/3 {
            f'4
            c'2
        }
        r4
        d'4.
        e'8
    }
    ''')


def test_LeafShuffler_12():
    random.seed(87234)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    shuffler = auxjad.LeafShuffler(container)
    music = shuffler.shuffle_leaves()
    staff = abjad.Staff(music)
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff
        {
            \time 4/4
            d'4
            c'4
            f'4
            e'4
        }
        ''')


def test_LeafShuffler_13():
    random.seed(18892)
    container = abjad.Container(r"\time 3/4 c'16 d'4.. e'4 | r4 f'2")
    shuffler = auxjad.LeafShuffler(container,
                                   omit_time_signatures=True,
                                   )
    music = shuffler()
    staff = abjad.Staff(music)
    abjad.f(staff)
    assert format(staff) == abjad.String.normalize(
        r'''
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
        ''')
    assert shuffler.omit_time_signatures
    shuffler.omit_time_signatures = False
    assert not shuffler.omit_time_signatures
