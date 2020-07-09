import abjad


def reposition_clefs(container: abjad.Container,
                     *,
                     shift_clef_to_notes: bool = True,
                     implicit_clef: abjad.Clef = abjad.Clef('treble'),
                     ):
    r"""Mutates an input container (of type ``abjad.Container`` or child class)
    in place and has no return value; this function removes all consecutive
    repeated clefs. It can also be used to shift clefs from rests to pitched
    leaves.

    Example:
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

        .. figure:: ../_images/image-reposition_clefs-1.png

        >>> auxjad.reposition_clefs(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            \clef "treble"
            c'1
            d'1
        }

        .. figure:: ../_images/image-reposition_clefs-2.png

    Example:
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

        .. figure:: ../_images/image-reposition_clefs-3.png

        This function handles fallback clefs too:

        >>> auxjad.reposition_clefs(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
        }

        .. figure:: ../_images/image-reposition_clefs-4.png

    Example:
        The function also removes clefs that are separated by anarbitrary
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

        .. figure:: ../_images/image-reposition_clefs-5.png

        >>> auxjad.reposition_clefs(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'2
            e'4
            r4
            f'1
        }

        .. figure:: ../_images/image-reposition_clefs-6.png

    Example:
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

        .. figure:: ../_images/image-reposition_clefs-7.png

        >>> auxjad.reposition_clefs(staff)
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

        .. figure:: ../_images/image-reposition_clefs-8.png

    Example:
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

        .. figure:: ../_images/image-reposition_clefs-9.png

        >>> auxjad.reposition_clefs(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'2
            r2
            R1
            e'1
        }

        .. figure:: ../_images/image-reposition_clefs-10.png

    Example:
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

        .. figure:: ../_images/image-reposition_clefs-11.png

        >>> auxjad.reposition_clefs(staff)
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

        .. figure:: ../_images/image-reposition_clefs-12.png

        Set ``shift_clef_to_notes`` to ``False`` to disable this behaviour.

        >>> staff = abjad.Staff(r"c'1 | d'2 r2 | fs1")
        >>> abjad.attach(abjad.Clef('treble'), staff[0])
        >>> abjad.attach(abjad.Clef('bass'), staff[2])
        >>> auxjad.reposition_clefs(staff, shift_clef_to_notes=False)
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

        .. figure:: ../_images/image-reposition_clefs-13.png

    Example:
        Clefs are shifted even if the container has multi-measure rests.

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

        .. figure:: ../_images/image-reposition_clefs-14.png

        >>> auxjad.reposition_clefs(staff)
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

        .. figure:: ../_images/image-reposition_clefs-15.png

    Example:
        The input container can also handle subcontainers, including cases in
        which the clefs are attached to leaves of subcontainers:

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

        .. figure:: ../_images/image-reposition_clefs-16.png

        >>> auxjad.reposition_clefs(staff)
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

        .. figure:: ../_images/image-reposition_clefs-17.png

    Example:
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

        .. figure:: ../_images/image-reposition_clefs-18.png

        >>> auxjad.reposition_clefs(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            c'1
            d'1
        }

        .. figure:: ../_images/image-reposition_clefs-19.png

        Set the argument ``implicit_clef`` to a different ``abjad.Clef`` to
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

        .. figure:: ../_images/image-reposition_clefs-20.png

        >>> auxjad.reposition_clefs(staff, implicit_clef=abjad.Clef('bass'))
        >>> abjad.f(staff)
        \new Staff
        {
            c1
            d1
        }

        .. figure:: ../_images/image-reposition_clefs-21.png

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

        .. figure:: ../_images/image-reposition_clefs-22.png
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")
    if not isinstance(shift_clef_to_notes, bool):
        raise TypeError("'shift_clef_to_notes' must be 'bool'")
    if not isinstance(implicit_clef, abjad.Clef):
        raise TypeError("'implicit_clef' must be 'abjad.Clef'")

    leaves = abjad.select(container[:]).leaves()

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
