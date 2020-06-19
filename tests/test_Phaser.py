import random
import abjad
import pytest
import auxjad


def test_Phaser_01():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    phaser = auxjad.Phaser(container)
    assert format(phaser) == abjad.String.normalize(
        r"""
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    notes = phaser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    notes = phaser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8.
            d'16
            ~
            d'8.
            e'16
            ~
            e'8.
            f'16
            ~
            f'8.
            c'16
        }
        """)
    notes = phaser.current_window
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8.
            d'16
            ~
            d'8.
            e'16
            ~
            e'8.
            f'16
            ~
            f'8.
            c'16
        }
        """)


def test_Phaser_02():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    phaser = auxjad.Phaser(container,
                           step_size=(1, 8),
                           )
    notes = phaser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    notes = phaser()
    staff.append(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
            c'8
            d'8
            ~
            d'8
            e'8
            ~
            e'8
            f'8
            ~
            f'8
            c'8
        }
        """)


def test_Phaser_03():
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 ~ e'2.")
    phaser = auxjad.Phaser(container,
                           step_size=(1, 4),
                           )
    notes = phaser.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
            ~
            e'2.
        }
        """)
    notes = phaser.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            d'4
            e'2
            ~
            e'2
            c'4
        }
        """)
    notes = phaser.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            e'2.
            ~
            e'4
            c'4
            d'4
        }
        """)
    notes = phaser.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            e'2.
            c'4
            d'4
            e'4
        }
        """)
    notes = phaser.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            e'2
            c'4
            d'4
            e'2
        }
        """)
    notes = phaser.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            e'4
            c'4
            d'4
            e'2.
        }
        """)
    with pytest.raises(StopIteration):
        assert phaser.__next__()


def test_Phaser_04():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    phaser = auxjad.Phaser(container,
                           step_size=(5, 8),
                           max_steps=2,
                           forward_bias=0.2,
                           remove_unterminated_ties=True,
                           )
    assert phaser.step_size == abjad.Duration((5, 8))
    assert phaser.max_steps == 2
    assert phaser.forward_bias == 0.2
    assert phaser.remove_unterminated_ties
    phaser.step_size = (1, 4)
    phaser.max_steps = 3
    phaser.forward_bias = 0.8
    phaser.remove_unterminated_ties = False
    assert phaser.step_size == abjad.Duration((1, 4))
    assert phaser.max_steps == 3
    assert phaser.forward_bias == 0.8
    assert not phaser.remove_unterminated_ties


def test_Phaser_05():
    container = abjad.Container(r"\time 3/4 c'4. d'4.")
    phaser = auxjad.Phaser(container,
                           step_size=(1, 4),
                           )
    notes = phaser.output_all()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4.
            d'4.
            c'8
            d'8
            ~
            d'4
            c'4
            d'4
            c'4
            ~
            c'8
            d'8
            c'4.
            d'4.
        }
        """)
    phaser = auxjad.Phaser(container,
                           step_size=(1, 4),
                           )
    notes = phaser.output_all(cycle_back_to_first=False)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4.
            d'4.
            c'8
            d'8
            ~
            d'4
            c'4
            d'4
            c'4
            ~
            c'8
            d'8
        }
        """)


def test_Phaser_06():
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 ~ e'2.")
    phaser = auxjad.Phaser(container,
                           step_size=(1, 4),
                           )
    notes = phaser.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
            ~
            e'2.
        }
        """)
    notes = phaser.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            d'4
            e'2
            ~
            e'2
            c'4
        }
        """)
    phaser.step_size = (1, 16)
    notes = phaser.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            d'8.
            e'16
            ~
            e'2
            ~
            e'4
            ~
            e'8.
            c'16
            ~
            c'8.
            d'16
        }
        """)
    notes = phaser.__next__()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            d'8
            e'8
            ~
            e'2
            ~
            e'4
            ~
            e'8
            c'8
            ~
            c'8
            d'8
        }
        """)


def test_Phaser_07():
    container = abjad.Container(r"\times 2/3 {c'8 d'8 e'8} d'2.")
    phaser = auxjad.Phaser(container)
    staff = abjad.Staff()
    for _ in range(3):
        window = phaser()
        staff.append(window)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            d'2.
            \times 2/3 {
                c'32
                d'16
                ~
                d'16
                e'32
                ~
                e'16.
            }
            d'16
            ~
            d'2
            ~
            d'8.
            \times 2/3 {
                c'16.
            }
            \times 2/3 {
                d'16
                e'8
            }
            d'8
            ~
            d'2
            ~
            d'8
            \times 2/3 {
                c'8
                d'16
            }
        }
        """)


def test_Phaser_08():
    wrong_type_input = 'foobar'
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    with pytest.raises(TypeError):
        assert auxjad.Phaser(wrong_type_input)
        assert auxjad.Phaser(container, step_size=62.3j)
        assert auxjad.Phaser(container, max_steps='foo')
        assert auxjad.Phaser(container, forward_bias='bar')
        assert auxjad.Phaser(container, phase_on_first_call='xyz')
        assert auxjad.Phaser(container, remove_ties_connecting_windows=17j)
    with pytest.raises(ValueError):
        assert auxjad.Phaser(container, max_steps=-1)
        assert auxjad.Phaser(container, forward_bias=-0.3)
        assert auxjad.Phaser(container, forward_bias=1.4)


def test_Phaser_09():
    container = abjad.Container(r"c'2 d'2")
    phaser = auxjad.Phaser(container,
                           step_size=(1, 8),
                           )
    staff = abjad.Staff()
    for _ in range(4):
        music = phaser()
        staff.append(music)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'2
            d'2
            c'4
            ~
            c'8
            d'8
            ~
            d'4
            ~
            d'8
            c'8
            c'4
            d'2
            c'4
            c'8
            d'8
            ~
            d'4
            ~
            d'8
            c'8
            ~
            c'4
        }
        """)
    phaser = auxjad.Phaser(container,
                           step_size=(1, 8),
                           remove_unterminated_ties=True,
                           )
    staff = abjad.Staff()
    for _ in range(4):
        music = phaser()
        staff.append(music)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'2
            d'2
            c'4
            ~
            c'8
            d'8
            ~
            d'4
            ~
            d'8
            c'8
            c'4
            d'2
            c'4
            c'8
            d'8
            ~
            d'4
            ~
            d'8
            c'8
            ~
            c'4
        }
        """)


def test_Phaser_10():
    container = abjad.Container(r"<d' fs' a'>2 c'2")
    phaser = auxjad.Phaser(container,
                           step_size=(1, 8),
                           )
    staff = abjad.Staff()
    for _ in range(4):
        music = phaser()
        staff.append(music)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            <d' fs' a'>2
            c'2
            <d' fs' a'>4
            ~
            <d' fs' a'>8
            c'8
            ~
            c'4
            ~
            c'8
            <d' fs' a'>8
            <d' fs' a'>4
            c'2
            <d' fs' a'>4
            <d' fs' a'>8
            c'8
            ~
            c'4
            ~
            c'8
            <d' fs' a'>8
            ~
            <d' fs' a'>4
        }
        """)
    phaser = auxjad.Phaser(container,
                           step_size=(1, 8),
                           remove_unterminated_ties=False,
                           )
    staff = abjad.Staff()
    for _ in range(4):
        music = phaser()
        staff.append(music)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            <d' fs' a'>2
            c'2
            <d' fs' a'>4
            ~
            <d' fs' a'>8
            c'8
            ~
            c'4
            ~
            c'8
            <d' fs' a'>8
            ~
            <d' fs' a'>4
            c'2
            <d' fs' a'>4
            ~
            <d' fs' a'>8
            c'8
            ~
            c'4
            ~
            c'8
            <d' fs' a'>8
            ~
            <d' fs' a'>4
            ~
        }
        """)


def test_Phaser_11():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    phaser = auxjad.Phaser(container,
                           step_size=(1, 32),
                           )
    notes = phaser.output_n(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
            c'8..
            d'32
            ~
            d'8..
            e'32
            ~
            e'8..
            f'32
            ~
            f'8..
            c'32
            c'8.
            d'16
            ~
            d'8.
            e'16
            ~
            e'8.
            f'16
            ~
            f'8.
            c'16
        }
        """)


def test_Phaser_12():
    container = abjad.Container(r"\time 3/8 c'8 d'8 e'8")
    phaser = auxjad.Phaser(container)
    notes = phaser.output_n(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/8
            c'8
            d'8
            e'8
            c'16
            d'16
            ~
            d'16
            e'16
            ~
            e'16
            c'16
            d'8
            e'8
            c'8
        }
        """)
    phaser = auxjad.Phaser(container,
                           forward_bias=0.0,
                           )
    notes = phaser.output_n(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/8
            c'8
            d'8
            e'8
            e'16
            c'16
            ~
            c'16
            d'16
            ~
            d'16
            e'16
            e'8
            c'8
            d'8
        }
        """)


def test_Phaser_13():
    container = abjad.Container(r"\time 3/8 c'8 d'8 e'8")
    phaser = auxjad.Phaser(container,
                           step_size=(1, 8),
                           forward_bias=0.0,
                           )
    notes = phaser.output_all()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
    r"""
    \new Staff
    {
        \time 3/8
        c'8
        d'8
        e'8
        e'8
        c'8
        d'8
        d'8
        e'8
        c'8
        c'8
        d'8
        e'8
    }
    """)


def test_Phaser_14():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    phaser = auxjad.Phaser(container,
                           phase_on_first_call=True,
                           )
    notes = phaser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
    r"""
    \new Staff
    {
        \time 4/4
        c'8.
        d'16
        ~
        d'8.
        e'16
        ~
        e'8.
        f'16
        ~
        f'8.
        c'16
    }
    """)


def test_Phaser_15():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    phaser = auxjad.Phaser(container,
                           phase_on_first_call=True,
                           remove_unterminated_ties=False,
                           )
    notes = phaser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
    r"""
    \new Staff
    {
        \time 4/4
        c'8.
        d'16
        ~
        d'8.
        e'16
        ~
        e'8.
        f'16
        ~
        f'8.
        c'16
        ~
    }
    """)


def test_Phaser_16():
    container = abjad.Container(r"c'4-.\p\< d'4--\f e'4->\p f'4")
    phaser = auxjad.Phaser(container,
                           step_size=(1, 8),
                           )
    notes = phaser.output_n(5)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
    r"""
    \new Staff
    {
        c'4
        \p
        - \staccato
        \<
        d'4
        \f
        - \tenuto
        e'4
        \p
        - \accent
        f'4
        c'8
        \p
        - \staccato
        \<
        d'8
        \f
        - \tenuto
        ~
        d'8
        e'8
        \p
        - \accent
        ~
        e'8
        f'8
        ~
        f'8
        c'8
        \p
        - \staccato
        d'4
        \f
        - \tenuto
        e'4
        \p
        - \accent
        f'4
        c'4
        \p
        - \staccato
        \<
        d'8
        \f
        - \tenuto
        e'8
        \p
        - \accent
        ~
        e'8
        f'8
        ~
        f'8
        c'8
        \p
        - \staccato
        ~
        c'8
        \<
        d'8
        \f
        - \tenuto
        e'4
        \p
        - \accent
        f'4
        c'4
        \p
        - \staccato
        \<
        d'4
        \f
        - \tenuto
    }
    """)


def test_Phaser_17():
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    phaser = auxjad.Phaser(container)
    notes = phaser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
        }
        """)
    notes = phaser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8.
            d'16
            ~
            d'8.
            e'16
            ~
            e'8.
            f'16
            ~
            f'8.
            c'16
        }
        """)
    phaser.contents = abjad.Container(r"c'16 d'16 e'16 f'16 g'2.")
    notes = phaser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'16
            d'16
            e'16
            f'16
            g'2.
        }
        """)
    notes = phaser()
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            d'16
            e'16
            f'16
            g'16
            ~
            g'2
            ~
            g'8.
            c'16
        }
        """)


def test_Phaser_18():
    container = abjad.Container(r"c'1")
    phaser = auxjad.Phaser(container)
    assert len(phaser) == 16
    container = abjad.Container(r"c'1 d'1 e'1 f'1")
    phaser = auxjad.Phaser(container)
    assert len(phaser) == 64
    container = abjad.Container(r"c'1")
    phaser = auxjad.Phaser(container,
                           step_size=(1, 4),
                           )
    assert len(phaser) == 4
    container = abjad.Container(r"\time 3/4 c'2.")
    phaser = auxjad.Phaser(container,
                           step_size=(1, 4),
                           )
    assert len(phaser) == 3
    container = abjad.Container(r"\time 3/4 c'2.")
    phaser = auxjad.Phaser(container,
                           step_size=(1, 2),
                           )
    assert len(phaser) == 3


def test_Phaser_19():
    container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
    phaser = auxjad.Phaser(container,
                           step_size=(1, 8),
                           )
    notes1 = phaser()
    notes2 = phaser(force_time_signature=True)
    staff = abjad.Staff(notes2)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 3/4
            c'8
            d'8
            ~
            d'8
            e'8
            ~
            e'8
            c'8
        }
        """)


def test_Phaser_20():
    container = abjad.Container(
        r"\time 2/4 c'2 \time 3/8 d'4. \time 2/4 e'2")
    phaser = auxjad.Phaser(container,
                           step_size=(1, 8),
                           )
    notes = phaser.output_n(3)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            c'2
            \time 3/8
            d'4.
            \time 2/4
            e'2
            c'4
            ~
            c'8
            d'8
            ~
            \time 3/8
            d'4
            e'8
            ~
            \time 2/4
            e'4
            ~
            e'8
            c'8
            c'4
            d'4
            ~
            \time 3/8
            d'8
            e'4
            ~
            \time 2/4
            e'4
            c'4
        }
        """)


def test_Phaser_21():
    random.seed(98451)
    container = abjad.Container(r"c'4 d'4 e'4 f'4")
    phaser = auxjad.Phaser(container,
                           step_size=(1, 4),
                           forward_bias=0.5,
                           )
    notes = phaser.output_n(5)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
            d'4
            e'4
            f'4
            c'4
            c'4
            d'4
            e'4
            f'4
            f'4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
            f'4
        }
        """)


def test_Phaser_22():
    random.seed(12365)
    container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    phaser = auxjad.Phaser(container,
                           step_size=(1, 8),
                           max_steps=4,
                           )
    notes = phaser.output_n(5)
    staff = abjad.Staff(notes)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
            b'8
            c''8
            f'8
            g'8
            a'8
            b'8
            c''8
            c'8
            d'8
            e'8
            c''8
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
            b'8
            f'8
            g'8
            a'8
            b'8
            c''8
            c'8
            d'8
            e'8
            a'8
            b'8
            c''8
            c'8
            d'8
            e'8
            f'8
            g'8
        }
        """)
