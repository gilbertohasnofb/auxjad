from typing import Union

import abjad

from .. import mutate


def _make_rest_from_leaf(leaf: abjad.Leaf,
                         *,
                         ignore_dynamics: bool = False,
                         ) -> abjad.Rest:
    r"""Creates a rest of the same duration as a leaf and passes the
    relevant leaf indicators to the rest (such as time signature or bar
    lines, but not slurs or articulations)
    """
    rest = abjad.Rest(leaf.written_duration)
    for indicator in abjad.get.indicators(leaf):
        if isinstance(indicator, (abjad.BarLine,
                                  abjad.Clef,
                                  abjad.Dynamic,
                                  abjad.KeySignature,
                                  abjad.LilyPondLiteral,
                                  abjad.MetronomeMark,
                                  abjad.RehearsalMark,
                                  abjad.Repeat,
                                  abjad.StaffChange,
                                  abjad.StartHairpin,
                                  abjad.StartSlur,
                                  abjad.StopHairpin,
                                  abjad.StopSlur,
                                  abjad.TimeSignature,
                                  )):
            abjad.attach(indicator, rest)
    return rest


def staff_splitter(staff: Union[abjad.Staff, abjad.Selection],
                   *,
                   threshold: Union[int,
                                    float,
                                    str,
                                    abjad.Pitch,
                                    ] = abjad.NamedPitch("c'"),
                   upper_clef: Union[abjad.Clef, str] = abjad.Clef('treble'),
                   lower_clef: Union[abjad.Clef, str] = abjad.Clef('bass'),
                   add_clefs: bool = True,
                   dynamics_only_on_upper_staff: bool = False,
                   reposition_dynamics: bool = True,
                   reposition_slurs: bool = True,
                   use_multimeasure_rests: bool = True,
                   rewrite_meter: bool = True,
                   ) -> tuple:
    r"""Takes an |abjad.Staff| or |abjad.Selection| and splits it into two
    staves using a reference pitch as threshold. Returns a tuple of
    |abjad.Staff|'s.

    Basic usage:
        By default, this function splits notes using ``C4`` as the pitch
        threshold (any pitches equal to or higher than the threhold will be
        added to the upper staff, and any pitches lower than it will be added
        to the lower staff). It also automatically adds clefs to both staves.
        This function returns a tuple of two |abjad.Staff|'s, which can be
        input directly into an |abjad.Score|:

        >>> staff = abjad.Staff(r"a4 b4 c'4 d'4")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                a4
                b4
                c'4
                d'4
            }

        ..  figure:: ../_images/staff_splitter-h3b7QkOtTm.png

        >>> staves = auxjad.staff_splitter(staff)
        >>> score = abjad.Score(staves)
        >>> abjad.show(score)

        ..  docs::

            \new Score
            <<
                \new Staff
                {
                    \clef "treble"
                    r2
                    c'4
                    d'4
                }
                \new Staff
                {
                    \clef "bass"
                    a4
                    b4
                    r2
                }
            >>

        ..  figure:: ../_images/staff_splitter-WQoeWAkkmV.png

    Chords:
        Chords are split according to the threhold pitch:

        >>> staff = abjad.Staff(r"<g b>4 <a c'>4 <b d' f'>4 <a f c' e' g'>4")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                <g b>4
                <a c'>4
                <b d' f'>4
                <a f c' e' g'>4
            }

        ..  figure:: ../_images/staff_splitter-ICrujezDfk.png

        >>> staves = auxjad.staff_splitter(staff)
        >>> score = abjad.Score(staves)
        >>> abjad.show(score)

        ..  docs::

            \new Score
            <<
                \new Staff
                {
                    \clef "treble"
                    r4
                    c'4
                    <d' f'>4
                    <c' e' g'>4
                }
                \new Staff
                {
                    \clef "bass"
                    <g b>4
                    a4
                    b4
                    <f a>4
                }
            >>

        ..  figure:: ../_images/staff_splitter-KASqlXv1Fh.png

    ``threshold``:
        Set the keword argument ``threshold`` to a pitch to specify the
        threhold pitch. Notes lower than this pitch will be added to the lower
        staff whereas notes higher than or equal to this pitch will be added to
        the upper one. It can take an |abjad.NamedPitch|, an
        |abjad.NumberedPitch|, or a :obj:`str`, :obj:`int`, or :obj:`float`.

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 <d' f' a'>4")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                d'4
                e'4
                <d' f' a'>4
            }

        ..  figure:: ../_images/staff_splitter-nbVARRMPpG.png

        >>> staves = auxjad.staff_splitter(staff, threshold="e'")
        >>> score = abjad.Score(staves)
        >>> abjad.show(score)

        ..  docs::

            \new Score
            <<
                \new Staff
                {
                    \clef "treble"
                    r2
                    e'4
                    <f' a'>4
                }
                \new Staff
                {
                    \clef "bass"
                    c'4
                    d'4
                    r4
                    d'4
                }
            >>

        ..  figure:: ../_images/staff_splitter-hwD9HkFusx.png

    ``lower_clef`` and ``upper_clef``:
        By default, the clefs of the lower and upper staves are set to bass and
        treble clefs, respectively. Use the keyword arguments ``lower_clef``
        and ``upper_clef`` to change this. They can take either an |abjad.Clef|
        or an :obj:`str`.

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 <d' f' a'>4")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                d'4
                e'4
                <d' f' a'>4
            }

        ..  figure:: ../_images/staff_splitter-eJBqwmhPsj.png

        >>> staves = auxjad.staff_splitter(staff,
        ...                                threshold="e'",
        ...                                lower_clef='treble',
        ...                                )
        >>> score = abjad.Score(staves)
        >>> abjad.show(score)

        ..  docs::

            \new Score
            <<
                \new Staff
                {
                    \clef "treble"
                    r2
                    e'4
                    <f' a'>4
                }
                \new Staff
                {
                    \clef "treble"
                    c'4
                    d'4
                    r4
                    d'4
                }
            >>

        ..  figure:: ../_images/staff_splitter-87mg2UBDPn.png

        >>> staff = abjad.Staff(r"e4 f4 g4 <f a c'>4")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                e4
                f4
                g4
                <f a c'>4
            }

        ..  figure:: ../_images/staff_splitter-Nu9dNMM9gy.png

        >>> staves = auxjad.staff_splitter(staff,
        ...                                threshold='g',
        ...                                upper_clef='bass',
        ...                                )
        >>> score = abjad.Score(staves)
        >>> abjad.show(score)

        ..  docs::

            \new Score
            <<
                \new Staff
                {
                    \clef "bass"
                    r2
                    g4
                    <a c'>4
                }
                \new Staff
                {
                    \clef "bass"
                    e4
                    f4
                    r4
                    f4
                }
            >>

        ..  figure:: ../_images/staff_splitter-68Qhb2RuTj.png

    ``add_clefs``:
        To not add clefs to the output staves, set ``add_clefs`` to ``False``:

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 <d' f' a'>4")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                d'4
                e'4
                <d' f' a'>4
            }

        ..  figure:: ../_images/staff_splitter-uoSjmalLzc.png

        >>> staves = auxjad.staff_splitter(staff,
        ...                                threshold="e'",
        ...                                add_clefs=False,
        ...                                )
        >>> score = abjad.Score(staves)
        >>> abjad.show(score)

        ..  docs::

            \new Score
            <<
                \new Staff
                {
                    r2
                    e'4
                    <f' a'>4
                }
                \new Staff
                {
                    c'4
                    d'4
                    r4
                    d'4
                }
            >>

        ..  figure:: ../_images/staff_splitter-roBNy3fRus.png

        ..  note::

            Note how there are no clefs added to the LilyPond output. Note that
            in the image above that LilyPond automatically fallbacks to treble
            clefs when no clef is present in the input code.

            >>> staff = abjad.Staff(r"c'4 d'4 e'4 <d' f' a'>4")
            >>> staves = auxjad.staff_splitter(staff,
            ...                                threshold="e'",
            ...                                add_clefs=False,
            ...                                )
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    r2
                    e'4
                    <f' a'>4
                }
                \new Staff
                {
                    c'4
                    d'4
                    r4
                    d'4
                }
            >>

    ``use_multimeasure_rests``:
        By default, rests are converted to multi-measure rests.

        >>> staff = abjad.Staff(
        ...     r"\time 2/4 c'2 \times 2/3 {<g b d'>2 <e' f'>4}"
        ...     r"\times 2/3 {a2 <g b>4}"
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 2/4
                c'2
                \times 2/3
                {
                    <g b d'>2
                    <e' f'>4
                }
                \times 2/3
                {
                    a2
                    <g b>4
                }
            }

        ..  figure:: ../_images/staff_splitter-QkVo9lbpvB.png

        >>> staves = auxjad.staff_splitter(staff)
        >>> score = abjad.Score(staves)
        >>> abjad.show(score)

        ..  docs::

            \new Score
            <<
                \new Staff
                {
                    \time 2/4
                    \clef "treble"
                    c'2
                    \times 2/3
                    {
                        d'2
                        <e' f'>4
                    }
                    R1 * 1/2
                }
                \new Staff
                {
                    \time 2/4
                    \clef "bass"
                    R1 * 1/2
                    \times 2/3
                    {
                        <g b>2
                        r4
                    }
                    \times 2/3
                    {
                        a2
                        <g b>4
                    }
                }
            >>

        ..  figure:: ../_images/staff_splitter-gLP4jNpRXE.png

        Set ``use_multimeasure_rests`` to ``False`` to disable this behaviour.

        >>> staves = auxjad.staff_splitter(staff,
        ...                                use_multimeasure_rests=False,
        ...                                )
        >>> score = abjad.Score(staves)
        >>> abjad.show(score)

        ..  docs::

            \new Score
            <<
                \new Staff
                {
                    \time 2/4
                    \clef "treble"
                    c'2
                    \times 2/3
                    {
                        d'2
                        <e' f'>4
                    }
                    r2
                }
                \new Staff
                {
                    \time 2/4
                    \clef "bass"
                    r2
                    \times 2/3
                    {
                        <g b>2
                        r4
                    }
                    \times 2/3
                    {
                        a2
                        <g b>4
                    }
                }
            >>

        ..  figure:: ../_images/staff_splitter-s2Q7w1aVAC.png

    ``rewrite_meter``:
        By default, the |abjad.Meter.rewrite_meter()| mutation is applied to
        the output. Set ``rewrite_meter`` to ``False`` to disable it:

        >>> staff = abjad.Staff(r"a4 b4 c'4 d'4")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                a4
                b4
                c'4
                d'4
            }

        ..  figure:: ../_images/staff_splitter-JyRf5fsouP.png

        >>> staves = auxjad.staff_splitter(staff,
        ...                                rewrite_meter=False,
        ...                                )
        >>> score = abjad.Score(staves)
        >>> abjad.show(score)

        ..  docs::

            \new Score
            <<
                \new Staff
                {
                    \clef "treble"
                    r4
                    r4
                    c'4
                    d'4
                }
                \new Staff
                {
                    \clef "bass"
                    a4
                    b4
                    r4
                    r4
                }
            >>

        ..  figure:: ../_images/staff_splitter-hinmixCe4v.png

    ``reposition_dynamics``:
        By default, dynamics are split among the staves and then are mutated
        using :func:`auxjad.mutate.reposition_dynamics()`.

        >>> staff = abjad.Staff(
        ...     r"c'2\p <b d'>2\ff \times 2/3 {<g b d'>2\f <e' f'>1\mf}"
        ...     r"\times 2/3 {a2\pp <g b>1\mp}"
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'2
                \p
                <b d'>2
                \ff
                \times 2/3
                {
                    <g b d'>2
                    \f
                    <e' f'>1
                    \mf
                }
                \times 2/3
                {
                    a2
                    \pp
                    <g b>1
                    \mp
                }
            }

        ..  figure:: ../_images/staff_splitter-I42iFOOMEm.png

        >>> staves = auxjad.staff_splitter(staff)
        >>> score = abjad.Score(staves)
        >>> abjad.show(score)

        ..  docs::

            \new Score
            <<
                \new Staff
                {
                    \clef "treble"
                    c'2
                    \p
                    d'2
                    \ff
                    \times 2/3
                    {
                        d'2
                        \f
                        <e' f'>1
                        \mf
                    }
                    R1
                }
                \new Staff
                {
                    \clef "bass"
                    r2
                    b2
                    \ff
                    \times 2/3
                    {
                        <g b>2
                        \f
                        r1
                    }
                    \times 2/3
                    {
                        a2
                        \pp
                        <g b>1
                        \mp
                    }
                }
            >>

        ..  figure:: ../_images/staff_splitter-SYTT14sWJo.png

        Set ``reposition_dynamics`` to ``False`` to disable this behaviour:

        >>> staff = abjad.Staff(
        ...     r"c'2\p <b d'>2\ff \times 2/3 {<g b d'>2\f <e' f'>1\mf}"
        ...     r"\times 2/3 {a2\pp <g b>1\mp}"
        ... )
        >>> staves = auxjad.staff_splitter(staff,
        ...                                reposition_dynamics=False,
        ...                                )
        >>> score = abjad.Score(staves)
        >>> abjad.show(score)

        ..  docs::

            \new Score
            <<
                \new Staff
                {
                    \clef "treble"
                    c'2
                    \p
                    d'2
                    \ff
                    \times 2/3
                    {
                        d'2
                        \f
                        <e' f'>1
                        \mf
                    }
                    R1
                    \mp
                }
                \new Staff
                {
                    \clef "bass"
                    r2
                    \p
                    b2
                    \ff
                    \times 2/3
                    {
                        <g b>2
                        \f
                        r1
                        \mf
                    }
                    \times 2/3
                    {
                        a2
                        \pp
                        <g b>1
                        \mp
                    }
                }
            >>

        ..  figure:: ../_images/staff_splitter-sXrC86fy1J.png

        ..  note::

            It is important to note that dynamics can easily become problematic
            in the output when dealing with complex input staves. When
            possible, it is always best to handle containers without dynamics
            or those with very simple dynamics.

    ``dynamics_only_on_upper_staff``:
        Dynamics are distributed to both staves by default. To keep the
        dynamics only to the upper staff, set ``dynamics_only_on_upper_staff``
        to ``True``

        >>> staff = abjad.Staff(
        ...     r"c'2\p <b d'>2\ff \times 2/3 {<g b d'>2\f <e' f'>1\mf}"
        ...     r"\times 2/3 {a2\pp <g b>1\mp}"
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'2
                \p
                <b d'>2
                \ff
                \times 2/3
                {
                    <g b d'>2
                    \f
                    <e' f'>1
                    \mf
                }
                \times 2/3
                {
                    a2
                    \pp
                    <g b>1
                    \mp
                }
            }

        ..  figure:: ../_images/staff_splitter-f6E9w8Lpn7.png

        >>> staves = auxjad.staff_splitter(staff,
        ...                                dynamics_only_on_upper_staff=True,
        ...                                )
        >>> score = abjad.Score(staves)
        >>> abjad.show(score)

        ..  docs::

            \new Score
            <<
                \new Staff
                {
                    \clef "treble"
                    c'2
                    \p
                    d'2
                    \ff
                    \times 2/3
                    {
                        d'2
                        \f
                        <e' f'>1
                        \mf
                    }
                    R1
                }
                \new Staff
                {
                    \clef "bass"
                    r2
                    b2
                    \times 2/3
                    {
                        <g b>2
                        r1
                    }
                    \times 2/3
                    {
                        a2
                        <g b>1
                    }
                }
            >>

        ..  figure:: ../_images/staff_splitter-bVcVinE5cG.png

        ..  note::

            Similarly to the previous note about dynamics, it is important to
            note that, once again, dynamics can easily become problematic in
            the output. If there are rests or multi-measure rests in the upper
            staff, the dynamics can get lost. The best approach is to add them
            after the split.

    Slurs and articulations:
        This function will automatically handle slurs and articulations:

        >>> staff = abjad.Staff(
        ...     r"\time 2/4 a8( b c' d') \times 2/3 {<g b d'>2 <e' f'>4}"
        ...     r"\time 3/4 <d a c' g'>4--  r8 <f a bf>4."
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 2/4
                a8
                (
                b8
                c'8
                d'8
                )
                \times 2/3
                {
                    <g b d'>2
                    <e' f'>4
                }
                \time 3/4
                <d a c' g'>4
                - \tenuto
                r8
                <f a bf>4.
            }

        ..  figure:: ../_images/staff_splitter-SZjT1IJCsn.png

        >>> staves = auxjad.staff_splitter(staff)
        >>> score = abjad.Score(staves)
        >>> abjad.show(score)

        ..  docs::

            \new Score
            <<
                \new Staff
                {
                    \time 2/4
                    \clef "treble"
                    r4
                    c'8
                    (
                    d'8
                    )
                    \times 2/3
                    {
                        d'2
                        <e' f'>4
                    }
                    \time 3/4
                    <c' g'>4
                    - \tenuto
                    r2
                }
                \new Staff
                {
                    \time 2/4
                    \clef "bass"
                    a8
                    (
                    b8
                    )
                    r4
                    \times 2/3
                    {
                        <g b>2
                        r4
                    }
                    \time 3/4
                    <d a>4
                    - \tenuto
                    r8
                    <f a bf>4.
                }
            >>

        ..  figure:: ../_images/staff_splitter-RbPPaLUzjO.png
    """
    if not isinstance(staff, (abjad.Staff, abjad.Selection)):
        raise TypeError("'staff' must be 'abjad.Staff' or 'abjad.Selection'")
    if isinstance(threshold, str):
        threshold = abjad.NamedPitch(threshold)
    elif isinstance(threshold, (int, float)):
        threshold = abjad.NumberedPitch(threshold)
    elif not isinstance(threshold, abjad.Pitch):
        raise TypeError("'threshold' must be 'abjad.Pitch' (or child class), "
                        "'str', 'int', or 'float'")
    if isinstance(upper_clef, str):
        upper_clef = abjad.Clef(upper_clef)
    elif not isinstance(upper_clef, abjad.Clef):
        raise TypeError("'upper_clef' must be 'abjad.Clef' or 'str'")
    if isinstance(lower_clef, str):
        lower_clef = abjad.Clef(lower_clef)
    elif not isinstance(lower_clef, abjad.Clef):
        raise TypeError("'lower_clef' must be 'abjad.Clef' or 'str'")
    if not isinstance(add_clefs, bool):
        raise TypeError("'add_clefs' must be 'bool'")
    if not isinstance(dynamics_only_on_upper_staff, bool):
        raise TypeError("'dynamics_only_on_upper_staff' must be 'bool'")
    if not isinstance(reposition_dynamics, bool):
        raise TypeError("'reposition_dynamics' must be 'bool'")
    if not isinstance(reposition_slurs, bool):
        raise TypeError("'reposition_slurs' must be 'bool'")
    if not isinstance(use_multimeasure_rests, bool):
        raise TypeError("'use_multimeasure_rests' must be 'bool'")
    if not isinstance(rewrite_meter, bool):
        raise TypeError("'rewrite_meter' must be 'bool'")

    upper_staff = abjad.mutate.copy(staff)
    lower_staff = abjad.mutate.copy(staff)
    if isinstance(staff, abjad.Selection):
        upper_staff = abjad.Staff(upper_staff)
        lower_staff = abjad.Staff(lower_staff)

    for leaf in abjad.select(upper_staff).leaves():
        if isinstance(leaf, abjad.Note) and leaf.written_pitch < threshold:
            rest = _make_rest_from_leaf(leaf)
            abjad.mutate.replace(leaf, rest)
        elif isinstance(leaf, abjad.Chord):
            if all([pitch < threshold for pitch in leaf.written_pitches]):
                rest = _make_rest_from_leaf(leaf)
                abjad.mutate.replace(leaf, rest)
            else:
                new_pitches = []
                for pitch in leaf.written_pitches:
                    if pitch >= threshold:
                        new_pitches.append(pitch)
                if len(new_pitches) > 1:
                    leaf.written_pitches = new_pitches
                else:
                    new_leaf = abjad.Note(new_pitches[0],
                                          leaf.written_duration,
                                          )
                    for indicator in abjad.get.indicators(leaf):
                        abjad.attach(indicator, new_leaf)
                    abjad.mutate.replace(leaf, new_leaf)

    for leaf in abjad.select(lower_staff).leaves():
        if isinstance(leaf, abjad.Note):
            if leaf.written_pitch >= threshold:
                rest = _make_rest_from_leaf(leaf)
                abjad.mutate.replace(leaf, rest)
        if isinstance(leaf, abjad.Chord):
            if all([pitch >= threshold for pitch in leaf.written_pitches]):
                rest = _make_rest_from_leaf(leaf)
                abjad.mutate.replace(leaf, rest)
            else:
                new_pitches = []
                for pitch in leaf.written_pitches:
                    if pitch < threshold:
                        new_pitches.append(pitch)
                if len(new_pitches) > 1:
                    leaf.written_pitches = new_pitches
                else:
                    new_leaf = abjad.Note(new_pitches[0],
                                          leaf.written_duration,
                                          )
                    for indicator in abjad.get.indicators(leaf):
                        abjad.attach(indicator, new_leaf)
                    abjad.mutate.replace(leaf, new_leaf)

    if add_clefs:
        abjad.attach(upper_clef, abjad.select(upper_staff).leaf(0))
        abjad.attach(lower_clef, abjad.select(lower_staff).leaf(0))

    if dynamics_only_on_upper_staff:
        for leaf in abjad.select(lower_staff).leaves():
            for indicator in abjad.get.indicators(leaf):
                if isinstance(indicator, (abjad.Dynamic,
                                          abjad.StartHairpin,
                                          abjad.StopHairpin,
                                          )):
                    abjad.detach(indicator, leaf)

    if reposition_dynamics:
        mutate.reposition_dynamics(upper_staff[:])
        if not dynamics_only_on_upper_staff:
            mutate.reposition_dynamics(lower_staff[:])

    if reposition_slurs:
        mutate.reposition_slurs(upper_staff[:])
        mutate.reposition_slurs(lower_staff[:])

    if use_multimeasure_rests:
        mutate.rests_to_multimeasure_rest(upper_staff[:])
        mutate.rests_to_multimeasure_rest(lower_staff[:])

    if rewrite_meter:
        mutate.auto_rewrite_meter(upper_staff)
        mutate.auto_rewrite_meter(lower_staff)

    return upper_staff, lower_staff


### EXTENSION FUNCTIONS ###

abjad.staff_splitter = staff_splitter
