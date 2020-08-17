import abjad


def respell_accidentals(selection: abjad.Selection,
                        *,
                        include_multiples: bool = False,
                        respell_by_pitch_class: bool = False,
                        ):
    r"""Mutates an input |abjad.Selection| in place and has no return value;
    this function changes the accidentals of individual pitches of all chords
    in a container in order to avoid augmented unisons.

    Basic usage:
        To use this function, apply it to a selection that contains chords that
        have augmented unisons.

        >>> container = abjad.Container(r"c'4 r4 <ef' e'>4 g'4 <c' cs'>4 r2.")
        >>> auxjad.mutate(container[:]).respell_accidentals()
        >>> abjad.f(container)
        {
            c'4
            r4
            <ds' e'>4
            g'4
            <c' df'>4
            r2.
        }

        .. figure:: ../_images/respell_accidentals-x33afbbamt.png

    .. note::

        Auxjad automatically adds this function as an extension method to
        |abjad.mutate()|. It can thus be used from either
        :func:`auxjad.mutate()` or |abjad.mutate()|. Therefore, the two lines
        below are equivalent:

        >>> auxjad.mutate(staff[:]).respell_accidentals()
        >>> abjad.mutate(staff[:]).respell_accidentals()

    2-note chords:
        The example below shows the default spelling of 2-note chords in
        Abjad in the upper staff, and the respelt 2-note chords in the bottom
        staff.

        >>> staff1 = abjad.Staff()
        >>> staff2 = abjad.Staff()
        >>> for pitch in range(12):
        ...     staff1.append(abjad.Chord([pitch, pitch + 1], (1, 16)))
        ...     staff2.append(abjad.Chord([pitch, pitch + 1], (1, 16)))
        >>> auxjad.mutate(staff2[:]).respell_accidentals()
        >>> literal = abjad.LilyPondLiteral(r'\accidentalStyle dodecaphonic')
        >>> abjad.attach(literal, staff1)
        >>> abjad.attach(literal, staff2)
        >>> score = abjad.Score([staff1, staff2])
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                \accidentalStyle dodecaphonic
                <c' cs'>16
                <cs' d'>16
                <d' ef'>16
                <ef' e'>16
                <e' f'>16
                <f' fs'>16
                <fs' g'>16
                <g' af'>16
                <af' a'>16
                <a' bf'>16
                <bf' b'>16
                <b' c''>16
            }
            \new Staff
            {
                \accidentalStyle dodecaphonic
                <c' df'>16
                <cs' d'>16
                <d' ef'>16
                <ds' e'>16
                <e' f'>16
                <f' gf'>16
                <fs' g'>16
                <g' af'>16
                <gs' a'>16
                <a' bf'>16
                <as' b'>16
                <b' c''>16
            }
        >>

        .. figure:: ../_images/respell_accidentals-jvg032q24il.png

    augmented unissons in larger chords:
        The function looks for all augmented unissons in chords of 3 or more
        pitches:

        >>> container1 = abjad.Container(r"<a c' cs' f'>1")
        >>> container2 = abjad.Container(r"<a c' cs' f'>1")
        >>> auxjad.mutate(container2[:]).respell_accidentals()
        >>> staff = abjad.Staff([container1, container2])
        >>> abjad.f(staff)
        \new Staff
        {
            {
                <a c' cs' f'>1
            }
            {
                <a c' df' f'>1
            }
        }

        .. figure:: ../_images/respell_accidentals-gyficck05p.png

        It is not a problem if the pitches are input out of order.

        >>> container1 = abjad.Container(r"<e' cs' g' ef'>1")
        >>> container2 = abjad.Container(r"<e' cs' g' ef'>1")
        >>> auxjad.mutate(container2[:]).respell_accidentals()
        >>> staff = abjad.Staff([container1, container2])
        >>> abjad.f(staff)
        \new Staff
        {
            {
                <cs' ef' e' g'>1
            }
            {
                <cs' ds' e' g'>1
            }
        }

        .. figure:: ../_images/respell_accidentals-xbu6u6mu6qo.png

    ``include_multiples``:
        By default, this function only changes spelling for pitches that are
        1 semitone apart.

        >>> container1 = abjad.Container(r"<c' cs''>1")
        >>> container2 = abjad.Container(r"<c' cs''>1")
        >>> auxjad.mutate(container2[:]).respell_accidentals()
        >>> staff = abjad.Staff([container1, container2])
        >>> abjad.f(staff)
        \new Staff
        {
            {
                <c' cs''>1
            }
            {
                <c' cs''>1
            }
        }

        .. figure:: ../_images/respell_accidentals-uszf11qb72d.png

        To consider pitches in different octaves (thus including augmented
        unisons, augmented octaves, augmented fifteenths, etc.), call this
        function with the keyword argument ``include_multiples`` set to
        ``True``.

        >>> container1 = abjad.Container(r"<c' cs''>1")
        >>> container2 = abjad.Container(r"<c' cs''>1")
        >>> auxjad.mutate(container2[:]).respell_accidentals(
        ...     include_multiples=True,
        ... )
        >>> staff = abjad.Staff([container1, container2])
        >>> abjad.f(staff)
        \new Staff
        {
            {
                <c' cs''>1
            }
            {
                <c' df''>1
            }
        }

        .. figure:: ../_images/respell_accidentals-8am8cu2rmgi.png

    ``respell_by_pitch_class``:
        By default, when this function changes the spelling of a pitch, it does
        not change the spelling of all other pitches with the same pitch-class.

        >>> container1 = abjad.Container(r"<c' cs' cs''>1")
        >>> container2 = abjad.Container(r"<c' cs' cs''>1")
        >>> auxjad.mutate(container2[:]).respell_accidentals()
        >>> staff = abjad.Staff([container1, container2])
        >>> abjad.f(staff)
        \new Staff
        {
            {
                <c' cs' cs''>1
            }
            {
                <c' df' cs''>1
            }
        }

        .. figure:: ../_images/respell_accidentals-47d16xk6gvs.png

        To alter all pitch-classes, call this function with the keyword
        argument ``respell_by_pitch_class`` set to ``True``.

        >>> container1 = abjad.Container(r"<c' cs' cs''>1")
        >>> container2 = abjad.Container(r"<c' cs' cs''>1")
        >>> auxjad.mutate(container2[:]).respell_accidentals(
        ...     respell_by_pitch_class=True,
        ... )
        >>> staff = abjad.Staff([container1, container2])
        >>> abjad.f(staff)
        \new Staff
        {
            {
                <c' cs' cs''>1
            }
            {
                <c' df' df''>1
            }
        }

        .. figure:: ../_images/respell_accidentals-kobft0oq9sl.png
    """
    if not isinstance(selection, abjad.Selection):
        raise TypeError("argument must be 'abjad.Selection'")
    if not isinstance(respell_by_pitch_class, bool):
        raise TypeError("'respell_by_pitch_class' must be 'bool'")
    if not isinstance(include_multiples, bool):
        raise TypeError("'include_multiples' must be 'bool'")

    for leaf in selection.leaves():
        if isinstance(leaf, abjad.Chord):
            accidentals = [pitch.accidental for pitch in leaf.written_pitches]
            if not include_multiples:
                # dealing only with intervals of size equal to 1 semitone
                for i in range(len(leaf.written_pitches) - 1):
                    p1 = leaf.written_pitches[i]
                    p2 = leaf.written_pitches[i + 1]
                    interval12 = p1 - p2
                    try:
                        p3 = leaf.written_pitches[i + 2]
                        interval23 = p2 - p3
                    except IndexError:
                        p3 = None
                        interval23 = None
                    if (interval12 == abjad.NamedInterval('+A1')
                            and interval23 != abjad.NamedInterval('+A1')
                            and interval23 != abjad.NamedInterval('+m2')):
                        if not respell_by_pitch_class:
                            # respelling only one single note
                            if p1.accidental == abjad.Accidental('f'):
                                accidentals[i] = abjad.Accidental('s')
                            elif p1.accidental == abjad.Accidental(''):
                                accidentals[i + 1] = abjad.Accidental('f')
                        else:
                            # respelling all matching pitch-classes
                            if p1.accidental == abjad.Accidental('f'):
                                for j, p in enumerate(leaf.written_pitches):
                                    if p.pitch_class == p1.pitch_class:
                                        accidentals[j] = abjad.Accidental('s')
                            elif p1.accidental == abjad.Accidental(''):
                                for j, p in enumerate(leaf.written_pitches):
                                    if p.pitch_class == p2.pitch_class:
                                        accidentals[j] = abjad.Accidental('f')
            else:
                # dealing with augmented unisons as well as augmented 8as,
                # 15ths, etc.
                for i in range(len(leaf.written_pitches) - 1):
                    for j in range(i + 1, len(leaf.written_pitches)):
                        # no p3 this time since p1 and p2 are not necessary
                        # consecutive pitches in the chord
                        p1 = leaf.written_pitches[i]
                        p2 = leaf.written_pitches[j]
                        interval = abjad.NamedIntervalClass(p1 - p2)
                        if (interval in (abjad.NamedIntervalClass('+A1'),
                                         abjad.NamedIntervalClass('-d1'),
                                         )):
                            # no need for respell_by_pitch_class since this
                            # will go through all notes in the chord anyway
                            if p1.accidental == abjad.Accidental('f'):
                                accidentals[i] = abjad.Accidental('s')
                            if p1.accidental == abjad.Accidental('s'):
                                accidentals[i] = abjad.Accidental('f')
                            elif p1.accidental == abjad.Accidental(''):
                                if p2.accidental == abjad.Accidental('s'):
                                    accidentals[j] = abjad.Accidental('f')
                                elif p2.accidental == abjad.Accidental('f'):
                                    accidentals[j] = abjad.Accidental('s')
            # rewritting chord with new spelling
            respelt_pitches = []
            for pitch, accidental in zip(leaf.written_pitches, accidentals):
                if accidental == abjad.Accidental('f'):
                    respelt_pitches.append(pitch._respell_with_flats())
                elif accidental == abjad.Accidental('s'):
                    respelt_pitches.append(pitch._respell_with_sharps())
                else:
                    respelt_pitches.append(pitch)
            leaf.written_pitches = respelt_pitches
