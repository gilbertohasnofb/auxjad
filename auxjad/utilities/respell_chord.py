import abjad


def respell_chord(chord: abjad.Chord,
                  *,
                  include_multiples: bool = False,
                  respell_by_pitch_class: bool = False,
                  ):
    r"""Mutates an input chord (of type ``abjad.Chord`` or child class) in
    place and has no return value. This function changes the accidentals of
    individual pitches of a chord in order to avoid augmented unisons.

    ..  container:: example

        To use this function, apply it to a chord that contains augmented
        unisons.

        >>> chord = abjad.Chord("<c' cs'>4")
        >>> auxjad.respell_chord(chord)
        >>> abjad.f(chord)
        <c' df'>4

        .. figure:: ../_images/image-respell_chord-1.png

    ..  container:: example

        The example below shows the default spelling of 2-note chords by
        ``Abjad`` in the upper staff, and the respelt 2-note chords in the
        bottom staff.

        >>> staff1 = abjad.Staff()
        >>> staff2 = abjad.Staff()
        >>> for pitch in range(12):
        ...     staff1.append(abjad.Chord([pitch, pitch + 1], (1, 16)))
        ...     chord = abjad.Chord([pitch, pitch + 1], (1, 16))
        ...     auxjad.respell_chord(chord)
        ...     staff2.append(chord)
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

        .. figure:: ../_images/image-respell_chord-2.png

    ..  container:: example

        The function looks for all augmented unissons in chords of 3 or more
        pitches:

        >>> chord1 = abjad.Chord(r"<a c' cs' f'>1")
        >>> chord2 = abjad.Chord(r"<a c' cs' f'>1")
        >>> auxjad.respell_chord(chord2)
        >>> staff = abjad.Staff([chord1, chord2])
        >>> abjad.f(staff)
        \new Staff
        {
            <a c' cs' f'>1
            <a c' df' f'>1
        }

        .. figure:: ../_images/image-respell_chord-3.png

        It is not a problem if the pitches are input out of order.

        >>> chord1 = abjad.Chord(r"<e' cs' g' ef'>1")
        >>> chord2 = abjad.Chord(r"<e' cs' g' ef'>1")
        >>> auxjad.respell_chord(chord2)
        >>> staff = abjad.Staff([chord1, chord2])
        >>> abjad.f(staff)
        \new Staff
        {
            <cs' ef' e' g'>1
            <cs' ds' e' g'>1
        }

        .. figure:: ../_images/image-respell_chord-4.png

    ..  container:: example

        By default, this function only changes spelling for pitches that are
        1 semitone apart.

        >>> chord1 = abjad.Chord(r"<c' cs''>1")
        >>> chord2 = abjad.Chord(r"<c' cs''>1")
        >>> auxjad.respell_chord(chord2)
        >>> staff = abjad.Staff([chord1, chord2])
        >>> abjad.f(staff)
        \new Staff
        {
            <c' cs''>1
            <c' cs''>1
        }

        .. figure:: ../_images/image-respell_chord-5.png

        To consider pitches in different octaves (thus including augmented
        unisons, augmented octaves, augmented fifteenths, etc.), call this
        function with the keyword argument ``include_multiples`` set to
        ``True``.

        >>> chord1 = abjad.Chord(r"<c' cs''>1")
        >>> chord2 = abjad.Chord(r"<c' cs''>1")
        >>> auxjad.respell_chord(chord2, include_multiples=True)
        >>> staff = abjad.Staff([chord1, chord2])
        >>> abjad.f(staff)
        \new Staff
        {
            <c' cs''>1
            <c' df''>1
        }

        .. figure:: ../_images/image-respell_chord-6.png

    ..  container:: example

        By default, when this function changes the spelling of a pitch, it does
        not change the spelling of all other pitches with the same pitch-class.

        >>> chord1 = abjad.Chord(r"<c' cs' cs''>1")
        >>> chord2 = abjad.Chord(r"<c' cs' cs''>1")
        >>> auxjad.respell_chord(chord2)
        >>> staff = abjad.Staff([chord1, chord2])
        >>> abjad.f(staff)
        \new Staff
        {
            <c' cs' cs''>1
            <c' df' cs''>1
        }

        .. figure:: ../_images/image-respell_chord-7.png

        To alter all pitch-classes, call this function with the keyword
        argument ``respell_by_pitch_class`` set to ``True``.

        >>> chord1 = abjad.Chord(r"<c' cs' cs''>1")
        >>> chord2 = abjad.Chord(r"<c' cs' cs''>1")
        >>> auxjad.respell_chord(chord2, respell_by_pitch_class=True)
        >>> staff = abjad.Staff([chord1, chord2])
        >>> abjad.f(staff)
        \new Staff
        {
            <c' cs' cs''>1
            <c' df' df''>1
        }

        .. figure:: ../_images/image-respell_chord-8.png
    """
    if not isinstance(chord, abjad.Chord):
        raise TypeError("argument must be 'abjad.Chord'")
    if not isinstance(respell_by_pitch_class, bool):
        raise TypeError("'respell_by_pitch_class' must be 'bool'")
    if not isinstance(include_multiples, bool):
        raise TypeError("'include_multiples' must be 'bool'")

    pitch_accidentals = [pitch.accidental for pitch in chord.written_pitches]

    if not include_multiples:
        # dealing only with intervals of size equal to 1 semitone
        for i in range(len(chord.written_pitches) - 1):
            p1 = chord.written_pitches[i]
            p2 = chord.written_pitches[i + 1]
            interval12 = p1 - p2
            try:
                p3 = chord.written_pitches[i + 2]
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
                        pitch_accidentals[i] = abjad.Accidental('s')
                    elif p1.accidental == abjad.Accidental(''):
                        pitch_accidentals[i + 1] = abjad.Accidental('f')
                else:
                    # respelling all matching pitch-classes
                    if p1.accidental == abjad.Accidental('f'):
                        for k, p in enumerate(chord.written_pitches):
                            if p.pitch_class == p1.pitch_class:
                                pitch_accidentals[k] = abjad.Accidental('s')
                    elif p1.accidental == abjad.Accidental(''):
                        for k, p in enumerate(chord.written_pitches):
                            if p.pitch_class == p2.pitch_class:
                                pitch_accidentals[k] = abjad.Accidental('f')
    else:
        # dealing with augmented unisons as well as augmented 8as, 15ths, etc.
        for i in range(len(chord.written_pitches) - 1):
            for j in range(i + 1, len(chord.written_pitches)):
                # no p3 this time since p1 and p2 are not necessary consecutive
                # pitches in the chord
                p1 = chord.written_pitches[i]
                p2 = chord.written_pitches[j]
                interval = abjad.NamedIntervalClass(p1 - p2)
                if (interval == abjad.NamedIntervalClass('+A1')
                        or interval == abjad.NamedIntervalClass('-d1')):
                    # no need for respell_by_pitch_class since this will go
                    # through all notes in the chord anyway
                    if p1.accidental == abjad.Accidental('f'):
                        pitch_accidentals[i] = abjad.Accidental('s')
                    if p1.accidental == abjad.Accidental('s'):
                        pitch_accidentals[i] = abjad.Accidental('f')
                    elif p1.accidental == abjad.Accidental(''):
                        if p2.accidental == abjad.Accidental('s'):
                            pitch_accidentals[j] = abjad.Accidental('f')
                        elif p2.accidental == abjad.Accidental('f'):
                            pitch_accidentals[j] = abjad.Accidental('s')

    # rewritting chord with new spelling
    respelt_pitches = []
    for pitch, accidental in zip(chord.written_pitches, pitch_accidentals):
        if accidental == abjad.Accidental('f'):
            respelt_pitches.append(pitch._respell_with_flats())
        elif accidental == abjad.Accidental('s'):
            respelt_pitches.append(pitch._respell_with_sharps())
        else:
            respelt_pitches.append(pitch)
    chord.written_pitches = respelt_pitches
