from typing import Optional, Union

import abjad


def _generate_harmonics_from_pitch(fundamental: abjad.Pitch,
                                   upper_bound: abjad.Pitch,
                                   ) -> list:
    r"""Private function used by |auxjad.get.virtual_fundamental()|. Generates
    the harmonic series for a given fundamental pitch up to a given upper
    bound.
    """
    harmonic_intervals = [12, 7, 5, 4, 3, 3, 2, 2, 2, 1, 2, 1, 2, 1, 1]
    harmonics = [fundamental]
    for interval in harmonic_intervals:
        harmonic = harmonics[-1] + interval
        if harmonic > upper_bound:
            break
        harmonics.append(harmonic)
    else:  # if upper bound not reached yet, harmonics go in semitones
        while harmonics[-1] < upper_bound:
            harmonic = harmonics[-1] + 1
            harmonics.append(harmonic)
    return harmonics


def virtual_fundamental(pitches: Union[abjad.PitchSegment, abjad.Chord],
                        *,
                        min_fundamental: Optional[abjad.Pitch] = None,
                        ) -> abjad.NamedPitch:
    r"""Returns the virtual fundamental (highest common fundamental) for all
    pitches in a |abjad.PitchSegment| or |abjad.Chord|. Return value is of type
    |abjad.NamedPitch|.

    Basic usage:
        This function will look for the highest fundamental whose harmonic
        series contains all notes in a given collection of pitches. E.g.:

        >>> pitches = abjad.PitchSegment(r"c'' g''")
        >>> auxjad.get.virtual_fundamental(pitches)
        c'

        >>> pitches = abjad.PitchSegment(r"c'' e'' g''")
        >>> auxjad.get.virtual_fundamental(pitches)
        c

        >>> pitches = abjad.PitchSegment(r"c'' f'' g''")
        >>> auxjad.get.virtual_fundamental(pitches)
        f,

        >>> pitches = abjad.PitchSegment(r"c'' d'' ef'' fs''")
        >>> auxjad.get.virtual_fundamental(pitches)
        bf,,

    ..  note::

        Auxjad automatically adds this function as an extension function to
        |abjad.get|. It can thus be used from either |auxjad.get|_ or
        |abjad.get| namespaces. Therefore, the two lines below are equivalent:

        >>> pitches = abjad.PitchSegment(r"c'' g''")
        >>> auxjad.get.virtual_fundamental(pitches)
        c'
        >>> abjad.get.virtual_fundamental(pitches)
        c'

    Input types:
        Input types can be |abjad.PitchSegment| or |abjad.Chord|:

        >>> pitches = abjad.PitchSegment(r"c'' cs'' d'' ef'' e'' fs''")
        >>> auxjad.get.virtual_fundamental(pitches)
        d,,
        >>> chord = abjad.Chord(r"<c'' cs'' d'' ef'' e'' fs''>4")
        >>> auxjad.get.virtual_fundamental(chord)
        d,,
        >>> staff = abjad.Staff(r"r4 <c'' cs'' d'' ef'' e'' fs''>4 r4")
        >>> auxjad.get.virtual_fundamental(staff[1])
        d,,

    ``min_fundamental``:
        The partials above the 13th partial can be approximated to include all
        chromatic pitches. This means that any complex of pitches will have a
        virtual fundamental, even though they are fairly distant from it. To
        limit the search of a fundamental by a minimum value, set
        ``min_fundamental`` to a specific pitch:

        >>> pitches = abjad.PitchSegment(r"c'' cs'' d'' ef'' e'' fs''")
        >>> auxjad.get.virtual_fundamental(
        ...     pitches,
        ...     min_fundamental=abjad.NamedPitch(r"c,,,"),
        ... )
        d,,

        >>> pitches = abjad.PitchSegment(r"c'' cs'' d'' ef'' e'' fs''")
        >>> auxjad.get.virtual_fundamental(
        ...     pitches,
        ...     min_fundamental=abjad.NumberedPitch(-48),
        ... )
        d,,

    ..  error::

        If a fundamental is not found with a given ``min_fundamental``, the
        function will raise a :exc:`ValueError` exception:

        >>> pitches = abjad.PitchSegment(r"c'' cs'' d'' ef'' e'' fs''")
        >>> auxjad.get.virtual_fundamental(
        ...     pitches,
        ...     min_fundamental=abjad.NamedPitch(r"c'"),
        ... )
        ValueError: No fundamental found above c'
    """
    if not isinstance(pitches, (abjad.PitchSegment, abjad.Chord)):
        raise TypeError("argument must be 'abjad.PitchSegment' or an "
                        "'abjad.Chord'")
    if min_fundamental is not None:
        if not isinstance(min_fundamental, (abjad.Pitch)):
            raise TypeError("'min_fundamental' must be 'abjad.Pitch' or child "
                            "class")
    if isinstance(pitches, abjad.Chord):
        pitches = pitches.written_pitches
    fundamental = abjad.NumberedPitch(min(pitches))
    if min_fundamental is not None:
        min_fundamental = abjad.NumberedPitch(min_fundamental)
    while True:
        harmonics = _generate_harmonics_from_pitch(fundamental, max(pitches))
        if all(abjad.NumberedPitch(pitch) in harmonics for pitch in pitches):
            return abjad.NamedPitch(fundamental)
        fundamental = fundamental - 1
        if min_fundamental is not None and fundamental < min_fundamental:
            raise ValueError('No fundamental found above '
                             + format(min_fundamental))
