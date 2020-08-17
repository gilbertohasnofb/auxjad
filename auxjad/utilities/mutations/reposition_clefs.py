import abjad


def reposition_clefs(selection: abjad.Selection,
                     *,
                     shift_clef_to_notes: bool = True,
                     implicit_clef: abjad.Clef = abjad.Clef('treble'),
                     ):
    r"""Mutates an input |abjad.Selection| in place and has no return value;
    this function removes all consecutive repeated clefs. It can also be used
    to shift clefs from rests to pitched leaves.

    Basic usage:
        When consecutive clefs are the same, the second one is removed:

        >>> staff = abjad.Staff(r"c'1 | d'1")
        >>> abjad.attach(abjad.Clef('treble'), staff[0])
        >>> abjad.attach(abjad.Clef('treble'), staff[1])
        >>> abjad.f(staff)
        \new Staff
        {
            \clef "treble"
            c'1
            \clef "treble"
            d'1
        }

        .. figure:: ../_images/reposition_clefs-ve7c2iykuyb.png

        >>> auxjad.mutate(staff[:]).reposition_clefs()
        >>> abjad.f(staff)
        \new Staff
        {
            \clef "treble"
            c'1
            d'1
        }

        .. figure:: ../_images/reposition_clefs-w6sbmg4iihr.png

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.mutate()|. It can thus be used from either
        :func:`auxjad.mutate()` or |abjad.mutate()|. Therefore, the two lines
        below are equivalent:

        >>> auxjad.mutate(staff[:]).reposition_clefs()
        >>> abjad.mutate(staff[:]).reposition_clefs()

    LilyPond's fallback clef:
        As seen above, LilyPond automatically omits repeated clefs unless the
        first clef is omitted. In that case, it uses a treble clef as fallback,
        although it won't then remove a subsequent repeated treble clef:

        >>> staff = abjad.Staff(r"c'1 | d'1")
        >>> abjad.attach(abjad.Clef('treble'), staff[1])
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \clef "treble"
            d'1
        }

        .. figure:: ../_images/reposition_clefs-ozr2sz3jugc.png

        This function handles fallback clefs too:

        >>> auxjad.mutate(staff[:]).reposition_clefs()
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
        }

        .. figure:: ../_images/reposition_clefs-0620w7q00lsr.png

    Clef structure:
        The function also removes clefs that are separated by an arbitrary
        number of leaves without clefs:

        >>> staff = abjad.Staff(r"c'1 | d'2 e'4 r4 | f'1")
        >>> abjad.attach(abjad.Clef('treble'), staff[4])
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'2
            e'4
            r4
            \clef "treble"
            f'1
        }

        .. figure:: ../_images/reposition_clefs-1dwpu3agebe.png

        >>> auxjad.mutate(staff[:]).reposition_clefs()
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'2
            e'4
            r4
            f'1
        }

        .. figure:: ../_images/reposition_clefs-wjmmwbhtaq.png

    Inputs with optimal clef structure:
        The function will not alter the container if the clef changes are
        already optimal.

        >>> staff = abjad.Staff(r"c'1 | a,2 bf,4 r4 | f'1")
        >>> abjad.attach(abjad.Clef('bass'), staff[1])
        >>> abjad.attach(abjad.Clef('treble'), staff[4])
        >>> abjad.f(staff)
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

        .. figure:: ../_images/reposition_clefs-ooacruvoibr.png

        >>> auxjad.mutate(staff[:]).reposition_clefs()
        >>> abjad.f(staff)
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

        .. figure:: ../_images/reposition_clefs-8z0s96frl4x.png

    Multi-measure rests:
        The function handles rests and multi-measure rests.

        >>> staff = abjad.Staff(r"c'1 | d'2 r2 | R1 | e'1")
        >>> abjad.attach(abjad.Clef('treble'), staff[0])
        >>> abjad.attach(abjad.Clef('treble'), staff[4])
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'2
            r2
            R1
            \clef "treble"
            e'1
        }

        .. figure:: ../_images/reposition_clefs-wpuzqrszs7i.png

        >>> auxjad.mutate(staff[:]).reposition_clefs()
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'2
            r2
            R1
            e'1
        }

        .. figure:: ../_images/reposition_clefs-os7dqkh11vl.png

    ``shift_clef_to_notes``:
        By default, clefs attached to rests are shifted to the first pitched
        leaf.

        >>> staff = abjad.Staff(r"c'1 | d'2 r2 | fs1")
        >>> abjad.attach(abjad.Clef('treble'), staff[0])
        >>> abjad.attach(abjad.Clef('bass'), staff[2])
        >>> abjad.f(staff)
        \new Staff
        {
            \clef "treble"
            c'1
            d'2
            \clef "bass"
            r2
            fs1
        }

        .. figure:: ../_images/reposition_clefs-jft5tljn0ni.png

        >>> auxjad.mutate(staff[:]).reposition_clefs()
        >>> abjad.f(staff)
        \new Staff
        {
            \clef "treble"
            c'1
            d'2
            r2
            \clef "bass"
            fs1
        }

        .. figure:: ../_images/reposition_clefs-pirrrq3p6di.png

        Set ``shift_clef_to_notes`` to ``False`` to disable this behaviour.

        >>> staff = abjad.Staff(r"c'1 | d'2 r2 | fs1")
        >>> abjad.attach(abjad.Clef('treble'), staff[0])
        >>> abjad.attach(abjad.Clef('bass'), staff[2])
        >>> auxjad.mutate(staff[:]).reposition_clefs(shift_clef_to_notes=False)
        >>> abjad.f(staff)
        \new Staff
        {
            \clef "treble"
            c'1
            d'2
            \clef "bass"
            r2
            fs1
        }

        .. figure:: ../_images/reposition_clefs-srrb69k33oe.png

    Multiple multi-measure rests:
        Clefs are shifted even if the container has multiple multi-measure
        rests.

        >>> staff = abjad.Staff(r"\time 3/4 c'2. | d'4 r2 | R1 * 3/4 | e'2.")
        >>> abjad.attach(abjad.Clef('treble'), staff[0])
        >>> abjad.attach(abjad.Clef('bass'), staff[2])
        >>> abjad.f(staff)
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

        .. figure:: ../_images/reposition_clefs-1l1ws1tqqt5.png

        >>> auxjad.mutate(staff[:]).reposition_clefs()
        >>> abjad.f(staff)
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

        .. figure:: ../_images/reposition_clefs-gmh7uqxjjrf.png

    Subcontainers:
        The container from which the selection is made can also have
        subcontainers, including cases in which the clefs are attached to
        leaves of subcontainers:

        >>> staff = abjad.Staff([abjad.Note("c'2"),
        ...                      abjad.Chord("<d' f'>2"),
        ...                      abjad.Tuplet((2, 3), "g'2 a'2 b'2"),
        ...                      ])
        >>> abjad.attach(abjad.Clef('treble'), staff[2][1])
        >>> abjad.f(staff)
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

        .. figure:: ../_images/reposition_clefs-vwygykrmjd.png

        >>> auxjad.mutate(staff[:]).reposition_clefs()
        >>> abjad.f(staff)
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

        .. figure:: ../_images/reposition_clefs-9gaqlf92kc.png

    ``implicit_clef``:
        By default, when the first leaf doesn't have a clef the function
        assumes that the music is written in treble clef (which is the default
        fallback clef in LilyPond).

        >>> staff = abjad.Staff(r"c'1 | d'1")
        >>> abjad.attach(abjad.Clef('treble'), staff[1])
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            \clef "treble"
            d'1
        }

        .. figure:: ../_images/reposition_clefs-tuxicnsglgk.png

        >>> auxjad.mutate(staff[:]).reposition_clefs()
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
        }

        .. figure:: ../_images/reposition_clefs-co27o4xxato.png

        Set the argument ``implicit_clef`` to a different |abjad.Clef| to
        change the implicit clef.

        >>> staff = abjad.Staff(r"c1 | d1")
        >>> abjad.attach(abjad.Clef('bass'), staff[1])
        >>> abjad.f(staff)
        \new Staff
        {
            c1
            \clef "bass"
            d1
        }

        .. figure:: ../_images/reposition_clefs-jyp5xd92vgi.png

        >>> auxjad.mutate(staff[:]).reposition_clefs(
        ...     implicit_clef=abjad.Clef('bass')
        ... )
        >>> abjad.f(staff)
        \new Staff
        {
            c1
            d1
        }

        .. figure:: ../_images/reposition_clefs-o7bi4n2n58.png

        This can be useful when extending a container that already has a
        specific clef.

        >>> music = abjad.Staff(r"\clef bass c4 d4 e4 f4")
        >>> music.extend(staff)
        >>> abjad.f(music)
        \new Staff
        {
            \clef "bass"
            c4
            d4
            e4
            f4
            c1
            d1
        }

        .. figure:: ../_images/reposition_clefs-7y32wepotnf.png

    .. warning::

        The input selection must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containing
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(selection, abjad.Selection):
        raise TypeError("argument must be 'abjad.Selection'")
    if not selection.leaves().are_contiguous_logical_voice():
        raise ValueError("argument must be contiguous logical voice")
    if not isinstance(shift_clef_to_notes, bool):
        raise TypeError("'shift_clef_to_notes' must be 'bool'")
    if not isinstance(implicit_clef, abjad.Clef):
        raise TypeError("'implicit_clef' must be 'abjad.Clef'")

    leaves = selection.leaves()

    # shifting clefs from rests to notes
    if shift_clef_to_notes:
        shifted_clef = None
        for leaf in leaves[1:]:
            clef = abjad.inspect(leaf).indicator(abjad.Clef)
            if isinstance(leaf, (abjad.Rest, abjad.MultimeasureRest)):
                if abjad.inspect(leaf).indicator(abjad.Clef) is not None:
                    shifted_clef = abjad.inspect(leaf).indicator(abjad.Clef)
                    abjad.detach(abjad.Clef, leaf)
            else:
                if (abjad.inspect(leaf).indicator(abjad.Clef) is None
                        and shifted_clef is not None):
                    abjad.attach(shifted_clef, leaf)
                shifted_clef = None

    # removing repeated clefs
    previous_clef = abjad.inspect(leaves[0]).indicator(abjad.Clef)
    if previous_clef is None:
        previous_clef = implicit_clef
    for leaf in leaves[1:]:
        clef = abjad.inspect(leaf).indicator(abjad.Clef)
        if clef == previous_clef:
            abjad.detach(abjad.Clef, leaf)
        elif clef is not None:
            previous_clef = clef
