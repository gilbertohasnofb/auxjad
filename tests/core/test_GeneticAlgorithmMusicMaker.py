import random

import abjad

import auxjad


def test_GeneticAlgorithmMusicMaker_01():
    random.seed(78612)
    maker = auxjad.GeneticAlgorithmMusicMaker(
        pitch_target=["c'", "d'", "e'", "f'"],
        pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        attack_point_target=[0, 4, 8, 12],
        attack_point_genes=list(range(16)),
    )
    assert repr(maker) == abjad.String.normalize(
        r"""
        pitches: ["c'", "d'", "e'", "f'"]
        attack_points: [0, 4, 8, 12]
        """
    )
    assert len(maker) == 4
    notes = maker.target_music
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
        }
        """
    )
    notes = maker()
    assert maker.generation_number == 0
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            f'4
            ~
            f'8.
            e'16
            ~
            e'8
            a'8
        }
        """
    )
    notes = maker()
    assert maker.generation_number == 1
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            d'16
            e'8.
            ~
            e'4
            ~
            e'16
            g'8.
        }
        """
    )


def test_GeneticAlgorithmMusicMaker_02():
    random.seed(48891)
    maker = auxjad.GeneticAlgorithmMusicMaker(
        pitch_target=["c'", "d'", "e'", "f'"],
        pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        attack_point_target=[0, 4, 8, 12],
        attack_point_genes=list(range(16)),
    )
    notes = maker.output_n(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r4
            r16
            c'8.
            d'16
            d'8.
            f'4
            c'2
            d'16
            c''8.
            f'4
            r16
            c'8.
            d'4
            f'4.
            f'8
            c'4
            d'8.
            e'16
            ~
            e'4
            e'4
            c'4
            d'4
            ~
            d'16
            e'8.
            e'4
        }
        """
    )


def test_GeneticAlgorithmMusicMaker_03():
    random.seed(98119)
    maker = auxjad.GeneticAlgorithmMusicMaker(
        pitch_target=["c'", "d'", "e'", "f'"],
        pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        attack_point_target=[0, 8, 16, 24],
        attack_point_genes=list(range(32)),
        duration_unit=abjad.Duration((1, 32)),
        units_per_window=32,
    )
    notes = maker.output_n(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'8.
            e'16
            ~
            e'16.
            e'32
            ~
            e'8
            ~
            e'32
            b'4...
            c'8.
            d'16
            ~
            d'2
            f'4
            c'4
            d'8..
            e'32
            ~
            e'4
            c'4
            c'4
            d'8..
            e'32
            ~
            e'4
            e'4
            c'4
            d'8..
            e'32
            ~
            e'4
            f'4
        }
        """
    )


def test_GeneticAlgorithmMusicMaker_04():
    random.seed(66732)
    maker = auxjad.GeneticAlgorithmMusicMaker(
        pitch_target=["c'", "d'", "e'", "f'"],
        pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        attack_point_target=[0, 4, 8, 12],
        attack_point_genes=list(range(16)),
        duration_unit=abjad.Duration((1, 32)),
    )
    notes = maker.output_n(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            r16
            c'16
            d'16
            g'16
            ~
            g'8
            f'8
            c'32
            d'8..
            e'16
            f'8.
            c'8
            d'16
            e'16
            ~
            e'8
            f'8
            c'8
            d'16.
            e'32
            ~
            e'8
            f'8
            c'8
            d'16.
            e'32
            ~
            e'8
            f'8
        }
        """
    )


def test_GeneticAlgorithmMusicMaker_05():
    random.seed(81242)
    maker = auxjad.GeneticAlgorithmMusicMaker(
        pitch_target=["c'", "d'", "e'", "f'", "g'"],
        pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        attack_point_target=[0, 4, 8, 12, 16],
        attack_point_genes=list(range(20)),
        units_per_window=20,
    )
    notes = maker.output_n(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 5/4
            r8
            c'8
            d'8
            f'4.
            e'4..
            g'16
            c'8.
            d'16
            ~
            d'4
            ~
            d'16
            g'16
            f'8
            ~
            f'4
            g'4
            c'4
            d'8.
            e'16
            ~
            e'4
            a'4
            f'4
            c'4
            d'8.
            g'16
            ~
            g'4
            f'4
            g'4
            c'4
            d'4
            g'4
            f'4
            g'4
        }
        """
    )
    random.seed(81242)
    maker = auxjad.GeneticAlgorithmMusicMaker(
        pitch_target=["c'", "d'", "e'", "f'", "g'"],
        pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        attack_point_target=[0, 4, 8, 12, 16],
        attack_point_genes=list(range(20)),
        units_per_window=20,
        omit_time_signature=True,
    )
    notes = maker.output_n(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r8
            c'8
            d'8
            f'4.
            e'4..
            g'16
            c'8.
            d'4.
            g'16
            f'4.
            g'4
            c'4
            d'8.
            e'4
            ~
            e'16
            a'4
            f'4
            c'4
            d'8.
            g'4
            ~
            g'16
            f'4
            g'4
            c'4
            d'4
            g'4
            f'4
            g'4
        }
        """
    )


def test_GeneticAlgorithmMusicMaker_06():
    random.seed(22714)
    maker = auxjad.GeneticAlgorithmMusicMaker(
        pitch_target=["c'", "d'", "e'", "f'"],
        pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        attack_point_target=[0, 4, 8, 12],
        attack_point_genes=list(range(16)),
        duration_unit=abjad.Duration((1, 32)),
    )
    notes = maker.output_n(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            r32
            c''16.
            ~
            c''32
            f'16.
            ~
            f'32
            e'16.
            f'8
            r32
            c'16.
            d'8
            ~
            d'16
            e'16
            e'8
            c'8.
            d'16
            e'8
            f'8
            r32
            c'16.
            d'8
            e'8
            f'8
            r32
            c'16.
            d'8
            e'8
            f'8
        }
        """
    )
    random.seed(22714)
    maker = auxjad.GeneticAlgorithmMusicMaker(
        pitch_target=["c'", "d'", "e'", "f'"],
        pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        attack_point_target=[0, 4, 8, 12],
        attack_point_genes=list(range(16)),
        duration_unit=abjad.Duration((1, 32)),
        time_signatures=abjad.TimeSignature((2, 2))
    )
    notes = maker.output_n(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/2
            r32
            c''16.
            ~
            c''32
            f'16.
            ~
            f'32
            e'16.
            f'8
            r2
            r32
            c'16.
            d'8
            ~
            d'16
            e'16
            e'8
            r2
            c'8.
            d'16
            e'8
            f'8
            r2
            r32
            c'16.
            d'8
            e'8
            f'8
            r2
            r32
            c'16.
            d'8
            e'8
            f'8
            r2
        }
        """
    )


def test_GeneticAlgorithmMusicMaker_07():
    random.seed(81242)
    maker = auxjad.GeneticAlgorithmMusicMaker(
        pitch_target=["c'", "d'", "e'", "f'", "g'"],
        pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        attack_point_target=[0, 4, 8, 12, 16],
        attack_point_genes=list(range(20)),
        duration_unit=abjad.Duration((1, 16)),
        units_per_window=20,
        time_signatures=[abjad.TimeSignature((2, 4)),
                         abjad.TimeSignature((3, 4)),
                         ],
    )
    notes = maker.output_n(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 2/4
            r8
            c'8
            d'8
            f'8
            ~
            \time 3/4
            f'4
            e'4..
            g'16
            \time 2/4
            c'8.
            d'16
            ~
            d'4
            ~
            \time 3/4
            d'16
            g'16
            f'4.
            g'4
            \time 2/4
            c'4
            d'8.
            e'16
            ~
            \time 3/4
            e'4
            a'4
            f'4
            \time 2/4
            c'4
            d'8.
            g'16
            ~
            \time 3/4
            g'4
            f'4
            g'4
            \time 2/4
            c'4
            d'4
            \time 3/4
            g'4
            f'4
            g'4
        }
        """
    )


def test_GeneticAlgorithmMusicMaker_08():
    random.seed(77132)
    maker = auxjad.GeneticAlgorithmMusicMaker(
        pitch_target=["c'", "d'", "e'", "f'"],
        pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        attack_point_target=[0, 4, 8, 12],
        attack_point_genes=list(range(16)),
    )
    notes = maker.output_n(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r16
            c'8
            d'16
            ~
            d'4
            f'4
            d'4
            r16
            c'8.
            d'8
            e'8
            ~
            e'8.
            f'16
            ~
            f'4
            c'4
            d'4
            e'4
            f'4
            c'4
            d'4
            e'4
            f'4
            c'4
            d'4
            e'4
            f'4
        }
        """
    )
    maker = auxjad.GeneticAlgorithmMusicMaker(
        pitch_target=["c'", "d'", "e'", "f'"],
        pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        attack_point_target=[0, 4, 8, 12],
        attack_point_genes=list(range(16)),
        pitch_score_bias=0.95,
    )
    notes = maker.output_n(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            r8
            c'16
            d'16
            ~
            d'4
            ~
            d'8
            e'4
            d'8
            r8
            c'16
            d'16
            ~
            d'2
            ~
            d'16
            e'8.
            c'16
            d'8.
            ~
            d'8.
            e'16
            ~
            e'4
            f'4
            c'16
            d'8.
            ~
            d'8.
            e'16
            ~
            e'4
            f'4
            c'4
            ~
            c'16
            d'8
            e'16
            ~
            e'4
            f'4
        }
        """
    )
    maker = auxjad.GeneticAlgorithmMusicMaker(
        pitch_target=["c'", "d'", "e'", "f'"],
        pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        attack_point_target=[0, 4, 8, 12],
        attack_point_genes=list(range(16)),
        pitch_score_bias=0.05,
    )
    notes = maker.output_n(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            e'16
            c''4..
            f'4
            c''4
            e'4
            d'4
            d'4
            f'4
            e'4
            d'4
            d'4
            f'4
            e'4
            d'4
            d'4
            f'4
            e'4
            d'4
            d'4
            f'4
        }
        """
    )


def test_GeneticAlgorithmMusicMaker_09():
    random.seed(87111)
    maker = auxjad.GeneticAlgorithmMusicMaker(
        pitch_target=["c'", "d'", "e'", "f'"],
        pitch_genes=["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        attack_point_target=[0, 4, 8, 12],
        attack_point_genes=list(range(16)),
        attack_points_mode=True,
    )
    notes = maker.output_n(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            e'16
            r8.
            c'16
            r16
            r16
            g'16
            r4
            f'16
            r8.
            c'16
            r8.
            d'16
            r8.
            e'16
            c'16
            r4.
            c'16
            r8.
            d'16
            r16
            r16
            e'16
            r4
            f'16
            r8.
            c'16
            r8.
            d'16
            r8.
            e'16
            r8.
            f'16
            r8.
            c'16
            r8.
            d'16
            r8.
            e'16
            r8.
            f'16
            r8.
        }
        """
    )


def test_GeneticAlgorithmMusicMaker_10():
    random.seed(71441)
    maker = auxjad.GeneticAlgorithmMusicMaker(
        pitch_target=["c'", None, "e'", ("g'", "bf'")],
        pitch_genes=[None,
                     "c'",
                     "d'",
                     "e'",
                     "f'",
                     "g'",
                     ("g'", "a'"),
                     ("g'", "bf'"),
                     ("g'", "c''"),
                     ],
        attack_point_target=[0, 4, 8, 12],
        attack_point_genes=list(range(16)),
        population_size=50,
    )
    notes = maker.output_n(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            <g' c''>4
            g'4
            ~
            g'16
            <g' c''>8.
            <g' c''>4
            c'2
            e'8.
            r16
            r4
            c'4
            r4
            r16
            e'8.
            <g' a'>4
            c'4
            r4
            e'8.
            <g' a'>16
            ~
            <g' a'>4
            c'4
            r4
            e'8.
            <g' a'>16
            ~
            <g' a'>4
        }
        """
    )


def test_GeneticAlgorithmMusicMaker_11():
    random.seed(71441)
    maker = auxjad.GeneticAlgorithmMusicMaker(
        pitch_target=[0, None, 4, (7, 10)],
        pitch_genes=[None, 0, 2, 4, 5, 7, (7, 9), (7, 10), (7, 12)],
        attack_point_target=[0, 4, 8, 12],
        attack_point_genes=list(range(16)),
        population_size=50,
    )
    notes = maker.output_n(5)
    staff = abjad.Staff(notes)
    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            <g' c''>4
            g'4
            ~
            g'16
            <g' c''>8.
            <g' c''>4
            c'2
            e'8.
            r16
            r4
            c'4
            r4
            r16
            e'8.
            <g' a'>4
            c'4
            r4
            e'8.
            <g' a'>16
            ~
            <g' a'>4
            c'4
            r4
            e'8.
            <g' a'>16
            ~
            <g' a'>4
        }
        """
    )
