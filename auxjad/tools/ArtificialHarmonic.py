import abjad


class ArtificialHarmonic(abjad.Chord):
    r"""Creates an ``abjad.Chord`` with a tweaked top note head for notating
    artificial harmonics.

    ..  container:: example

        Usage is similar to ``abjad.Chord``:

        >>> chord = auxjad.ArtificialHarmonic("<g c'>4")
        >>> chord.style
        'harmonic'
        >>> abjad.f(chord)
        <
            g
            \tweak style #'harmonic
            c'
        >4

        And similarly to ``abjad.Chord``, pitch and duration can be input in
        many different ways:

        >>> chord1 = auxjad.ArtificialHarmonic("<g c'>4")
        >>> chord2 = auxjad.ArtificialHarmonic(["g", "c'"], 1/4)
        >>> chord3 = auxjad.ArtificialHarmonic([-5, 0], 0.25)
        >>> chord4 = auxjad.ArtificialHarmonic([-5, 0], abjad.Duration(1, 4))
        >>> abjad.f(chord1)
        <
            g
            \tweak style #'harmonic
            c'
        >4
        >>> abjad.f(chord2)
        <
            g
            \tweak style #'harmonic
            c'
        >4
        >>> abjad.f(chord3)
        <
            g
            \tweak style #'harmonic
            c'
        >4
        >>> abjad.f(chord4)
        <
            g
            \tweak style #'harmonic
            c'
        >4

    ..  container:: example

        It is important to note that this class can only be initialised with
        exactly two pitches. Any other number of pitches will raise a
        ``ValueError``:

        >>> auxjad.ArtificialHarmonic("<g c' d'>4")
        ValueError: 'ArtificialHarmonic' requires exactly two 'note_heads' for
        initialisation

    ..  container:: example

        When creating an ``ArtificialHarmonic``, use the keyword argument
        ``style`` to set a different type of chord head for the top note, such
        as ``'harmonic-mixed'``:

        >>> chord = auxjad.ArtificialHarmonic("<g c'>4",
        ...                                   style='harmonic-mixed',
        ...                                   )
        >>> chord.style
        'harmonic-mixed'
        >>> abjad.f(chord)
        <
            g
            \tweak style #'harmonic-mixed
            c'
        >4

    ..  container:: example

        To notate natural harmonics with a parenthesised pitch for the open
        string at the bottom of the interval, set the keyword
        ``is_parenthesized`` to ``True``.

        >>> chord = auxjad.ArtificialHarmonic("<g c'>4",
        ...                                   is_parenthesized=True,
        ...                                   )
        >>> chord.is_parenthesized
        True
        >>> abjad.f(chord)
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >4

    ..  container:: example

        Similarly to ``abjad.Chord``, ``ArtificialHarmonic`` can take
        multipliers:

        >>> chord = auxjad.ArtificialHarmonic("<g c'>4",
        ...                                   multiplier=(2, 3),
        ...                                   )
        >>> chord.multiplier
        abjad.Multiplier(2, 3)
        >>> abjad.f(chord)
        <
            g
            \tweak style #'harmonic
            c'
        >4 * 2/3

    ..  container:: example

        All properties of ``abjad.Chord`` are also available to be read. This
        class also includes two new properties named ``style`` and
        ``is_parenthesized``:

        >>> chord = auxjad.ArtificialHarmonic("<g c'>4")
        >>> chord.written_pitches
        "g c'"
        >>> chord.written_duration
        1/4
        >>> chord.style
        'harmonic'
        >>> chord.is_parenthesized
        False

        All these properties can be set to different values after
        initialisation:

        >>> chord.written_pitches = [-5, 2]
        >>> chord.written_duration = abjad.Duration(1, 8)
        >>> chord.style = 'harmonic-mixed'
        >>> chord.is_parenthesized = True
        >>> chord.written_pitches
        "g d'"
        >>> chord.written_duration
        1/8
        >>> chord.style
        'harmonic-mixed'
        >>> chord.is_parenthesized
        True

    ..  container:: example

        The methods ``sounding_pitch()`` and ``sounding_note()`` return the
        sounding pitch and sounding note, respectively. Their types are
        ``abjad.Pitch`` and ``abjad.Note``, respectively.

        >>> harmonics = [ArtificialHarmonic("<g b>4"),
        ...              ArtificialHarmonic("<g c'>4"),
        ...              ArtificialHarmonic("<g d'>4"),
        ...              ArtificialHarmonic("<g e'>4"),
        ...              ArtificialHarmonic("<g g'>4"),
        ...              ]
        >>> for harmonic in harmonics:
        ...     print(harmonic.sounding_pitch())
        b''
        g''
        d''
        b''
        g'
        >>> for harmonic in harmonics:
        ...     print(harmonic.sounding_note())
        b''4
        g''4
        d''4
        b''4
        g'4

    ..  container:: example

        The note created by ``sounding_note()`` inherits all indicators from
        the ``ArtificialHarmonic``.

        >>> note = auxjad.ArtificialHarmonic(r"<g c'>4-.\pp")
        >>> abjad.f(note.sounding_note())
        g''4
        \pp
        - \staccato

    ..  container:: example

        Both ``sounding_pitch()`` and ``sounding_note()`` methods raise a
        ValueError exception when it cannot calculate the sounding pitch for
        the given interval.

        >>> ArtificialHarmonic("<g ef'>4").sounding_pitch()
        ValueError: cannot calculate sounding pitch for given interval
        >>> ArtificialHarmonic("<g ef'>4").sounding_note()
        ValueError: cannot calculate sounding pitch for given interval

    """

    def __init__(self,
                 *arguments,
                 multiplier: abjad.typings.DurationTyping = None,
                 tag: abjad.Tag = None,
                 style: str = 'harmonic',
                 is_parenthesized: bool = False,
                 ):
        super().__init__(*arguments, multiplier=multiplier, tag=tag)
        if len(self.note_heads) != 2:
            raise ValueError("'ArtificialHarmonic' requires exactly two "
                             "'note_heads' for initialisation")
        self._style = style
        self.style = self._style
        self._is_parenthesized = is_parenthesized
        self.is_parenthesized = self._is_parenthesized

    def sounding_pitch(self) -> abjad.Pitch:
        interval = abs(self.note_heads[1].written_pitch \
                   - self.note_heads[0].written_pitch).semitones
        sounding_pitch_dict = {1: 48,
                               2: 36,
                               3: 31,
                               4: 28,
                               5: 24,
                               7: 19,
                               9: 28,
                               12: 12,
                               16: 28,
                               19: 19,
                               24: 24,
                               28: 28,
                               }
        try:
            sounding_pitch = self.note_heads[0].written_pitch \
                           + sounding_pitch_dict[interval]
        except:
            raise KeyError('cannot calculate sounding pitch for given '
                           'interval')
        return sounding_pitch

    def sounding_note(self) -> abjad.Note:
        note = abjad.Note(self.sounding_pitch(), self.written_duration)
        for indicator in abjad.inspect(self).indicators():
            abjad.attach(indicator, note)
        return note

    @property
    def written_pitches(self) -> abjad.pitch.PitchSegment:
        return abjad.pitch.PitchSegment(
            items=(note_head.written_pitch for note_head in self.note_heads),
            item_class=abjad.pitch.NamedPitch,
        )

    @written_pitches.setter
    def written_pitches(self,
                        pitches,
                        ):
        for i, pitch in enumerate(pitches):
            self.note_heads[i].written_pitch = pitch

    @property
    def style(self) -> str:
        return self._style

    @style.setter
    def style(self,
              style_string: str,
              ):
        if not isinstance(style_string, str):
            raise TypeError("'style_string' must be 'str'")
        self._style = style_string
        abjad.tweak(self.note_heads[1]).style = self._style

    @property
    def is_parenthesized(self) -> bool:
        return self._is_parenthesized

    @is_parenthesized.setter
    def is_parenthesized(self,
                         parenthesized_bool: bool,
                         ):
        if not isinstance(parenthesized_bool, bool):
            raise TypeError("'parenthesized_bool' must be 'bool'")
        self._is_parenthesized = parenthesized_bool
        self.note_heads[0].is_parenthesized = self._is_parenthesized
        if self._is_parenthesized:
            abjad.tweak(self.note_heads[0]).ParenthesesItem__font_size = -4
