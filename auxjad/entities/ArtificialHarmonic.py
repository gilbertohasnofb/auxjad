import abjad
from ._HarmonicParent import _HarmonicParent


class ArtificialHarmonic(abjad.Chord, _HarmonicParent):
    r"""Creates an chord with a tweaked top note head for notating artificial
    harmonics. This is a child class of ``abjad.Chord``.

    ..  container:: example

        Usage is similar to ``abjad.Chord``:

        >>> harm = auxjad.ArtificialHarmonic("<g c'>4")
        >>> harm.style
        'harmonic'
        >>> abjad.f(harm)
        <
            g
            \tweak style #'harmonic
            c'
        >4

        .. figure:: ../_images/image-ArtificialHarmonic-1.png

        And similarly to ``abjad.Chord``, pitch and duration can be input in
        many different ways:

        >>> harm1 = auxjad.ArtificialHarmonic("<g c'>4")
        >>> harm2 = auxjad.ArtificialHarmonic(["g", "c'"], 1/4)
        >>> harm3 = auxjad.ArtificialHarmonic([-5, 0], 0.25)
        >>> harm4 = auxjad.ArtificialHarmonic([-5, 0], abjad.Duration(1, 4))
        >>> staff = abjad.Staff([harm1, harm2, harm3, harm4])
        >>> abjad.f(staff)
        \new Staff
        {
            <
                g
                \tweak style #'harmonic
                c'
            >4
            <
                g
                \tweak style #'harmonic
                c'
            >4
            <
                g
                \tweak style #'harmonic
                c'
            >4
            <
                g
                \tweak style #'harmonic
                c'
            >4
        }

        .. figure:: ../_images/image-ArtificialHarmonic-2.png



    ..  container:: example

        It is important to note that this class can only be initialised with
        exactly two pitches. Any other number of pitches will raise a
        ``ValueError``:

        >>> auxjad.ArtificialHarmonic("<g c' d'>4")
        ValueError: 'ArtificialHarmonic' requires exactly two 'note_heads' for
        initialisation

    ..  container:: example

        When creating an ``ArtificialHarmonic``, use the keyword argument
        ``style`` to set a different type of note head for the top note, such
        as ``'harmonic-mixed'``:

        >>> harm = auxjad.ArtificialHarmonic("<g c'>4",
        ...                                  style='harmonic-mixed',
        ...                                  )
        >>> harm.style
        'harmonic-mixed'
        >>> abjad.f(harm)
        <
            g
            \tweak style #'harmonic-mixed
            c'
        >4

        .. figure:: ../_images/image-ArtificialHarmonic-3.png

    ..  container:: example

        To notate natural harmonics with a parenthesised pitch for the open
        string at the bottom of the interval, set the keyword
        ``is_parenthesized`` to ``True``.

        >>> harm = auxjad.ArtificialHarmonic("<g c'>4",
        ...                                  is_parenthesized=True,
        ...                                  )
        >>> harm.is_parenthesized
        True
        >>> abjad.f(harm)
        <
            \parenthesize
            \tweak ParenthesesItem.font-size #-4
            g
            \tweak style #'harmonic
            c'
        >4

        .. figure:: ../_images/image-ArtificialHarmonic-4.png

    ..  container:: example

        Similarly to ``abjad.Chord``, ``ArtificialHarmonic`` can take
        multipliers:

        >>> harm = auxjad.ArtificialHarmonic("<g c'>4",
        ...                                  multiplier=(2, 3),
        ...                                  )
        >>> harm.multiplier
        abjad.Multiplier(2, 3)
        >>> abjad.f(harm)
        <
            g
            \tweak style #'harmonic
            c'
        >4 * 2/3

        .. figure:: ../_images/image-ArtificialHarmonic-5.png

    ..  container:: example

        All properties of ``abjad.Chord`` are also available to be read. This
        class also includes two new properties named ``style`` and
        ``is_parenthesized``:

        >>> harm = auxjad.ArtificialHarmonic("<g c'>4")
        >>> harm.written_pitches
        "g c'"
        >>> harm.written_duration
        1/4
        >>> harm.style
        'harmonic'
        >>> harm.is_parenthesized
        False

        All these properties can be set to different values after
        initialisation:

        >>> harm.written_pitches = [-5, 2]
        >>> harm.written_duration = abjad.Duration(1, 8)
        >>> harm.style = 'harmonic-mixed'
        >>> harm.is_parenthesized = True
        >>> harm.written_pitches
        "g d'"
        >>> harm.written_duration
        1/8
        >>> harm.style
        'harmonic-mixed'
        >>> harm.is_parenthesized
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

        To add a markup expression to the harmonic note, use the markup:

        >>> harm1 = auxjad.ArtificialHarmonic("<a d'>1")
        >>> harm2 = auxjad.ArtificialHarmonic("<a d'>1",
        ...                                   markup='I.',
        ...                                   )
        >>> harm3 = auxjad.ArtificialHarmonic("<a d'>1",
        ...                                   markup='I.',
        ...                                   direction=abjad.Down)
        >>> staff = abjad.Staff([harm1, harm2, harm3])
        >>> abjad.f(staff)
        \new Staff
        {
            <
                a
                \tweak style #'harmonic
                d'
            >1
            <
                a
                \tweak style #'harmonic
                d'
            >1
            ^ \markup { I. }
            <
                a
                \tweak style #'harmonic
                d'
            >1
            _ \markup { I. }
        }

        .. figure:: ../_images/image-ArtificialHarmonic-6.png

        Setting ``markup`` to ``None`` will remove the markup from the note.

        >>> harm = auxjad.ArtificialHarmonic("<a d'>1",
        ...                                  markup='I.',
        ...                                  )
        >>> harm.markup = None
        >>> abjad.f(harm)
        <
            a
            \tweak style #'harmonic
            d'
        >1

        .. figure:: ../_images/image-ArtificialHarmonic-7.png

    ..  warning::

        If another markup is attached to the harmonic note, trying to set the
        ``markup`` to ``None`` will raise an Exception:

        >>> harm = auxjad.ArtificialHarmonic("<a d'>1")
        >>> abjad.attach(abjad.Markup('test'), harm)
        >>> harm.markup = 'I.'
        >>> harm.markup = None
        Exception: multiple indicators attached to client.

    ..  container:: example

        The note created by ``sounding_note()`` inherits all indicators from
        the ``ArtificialHarmonic``.

        >>> harm = auxjad.ArtificialHarmonic(r"<g c'>4-.\pp")
        >>> abjad.f(harm.sounding_note())
        g''4
        \pp
        - \staccato

        .. figure:: ../_images/image-ArtificialHarmonic-8.png

    ..  warning::

        Both ``sounding_pitch()`` and ``sounding_note()`` methods raise a
        ValueError exception when it cannot calculate the sounding pitch for
        the given interval.

        >>> ArtificialHarmonic("<g ef'>4").sounding_pitch()
        ValueError: cannot calculate sounding pitch for given interval
        >>> ArtificialHarmonic("<g ef'>4").sounding_note()
        ValueError: cannot calculate sounding pitch for given interval
    """

    ### INITIALISER ###

    def __init__(self,
                 *arguments,
                 multiplier: abjad.typings.DurationTyping = None,
                 tag: abjad.Tag = None,
                 style: str = 'harmonic',
                 is_parenthesized: bool = False,
                 markup: str = None,
                 direction: (str, abjad.enums.VerticalAlignment) = 'up',
                 ):
        super().__init__(*arguments, multiplier=multiplier, tag=tag)
        if len(self.note_heads) != 2:
            raise ValueError("'ArtificialHarmonic' requires exactly two "
                             "'note_heads' for initialisation")
        self.style = style
        self.is_parenthesized = is_parenthesized
        self._direction = direction
        self.markup = markup

    ### PUBLIC METHODS ###

    def sounding_pitch(self) -> abjad.Pitch:
        r'Returns the sounding pitch of the harmonic as an ``abjad.Pitch``.'
        interval = abs(self.note_heads[1].written_pitch
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
            sounding_pitch = (self.note_heads[0].written_pitch
                              + sounding_pitch_dict[interval])
        except KeyError as err:
            raise ValueError('cannot calculate sounding pitch for given '
                             'interval') from err
        return sounding_pitch

    def sounding_note(self) -> abjad.Note:
        r'Returns the sounding note of the harmonic as an ``abjad.Note``.'
        note = abjad.Note(self.sounding_pitch(), self.written_duration)
        for indicator in abjad.inspect(self).indicators():
            abjad.attach(indicator, note)
        return note

    ### PUBLIC PROPERTIES ###

    @property
    def written_pitches(self) -> abjad.pitch.PitchSegment:
        r'The written pitches of the two note heads.'
        return abjad.pitch.PitchSegment(
            items=(note_head.written_pitch for note_head in self.note_heads),
            item_class=abjad.pitch.NamedPitch,
        )

    @written_pitches.setter
    def written_pitches(self,
                        written_pitches,
                        ):
        written_pitches_ = abjad.PitchSegment(written_pitches)
        if len(written_pitches_) != 2:
            raise ValueError("'ArtificialHarmonic' requires exactly two "
                             "pitches")
        for i, pitch in enumerate(written_pitches_):
            self.note_heads[i].written_pitch = pitch

    @property
    def style(self) -> str:
        r'The style of the upper note head.'
        return self._style

    @style.setter
    def style(self,
              style: str,
              ):
        if not isinstance(style, str):
            raise TypeError("'style' must be 'str'")
        self._style = style
        abjad.tweak(self.note_heads[1]).style = self._style

    @property
    def is_parenthesized(self) -> bool:
        r'Whether the bottom note head is parenthesised or not.'
        return self._is_parenthesized

    @is_parenthesized.setter
    def is_parenthesized(self,
                         is_parenthesized: bool,
                         ):
        if not isinstance(is_parenthesized, bool):
            raise TypeError("'is_parenthesized' must be 'bool'")
        self._is_parenthesized = is_parenthesized
        self.note_heads[0].is_parenthesized = self._is_parenthesized
        if self._is_parenthesized:
            abjad.tweak(self.note_heads[0]).ParenthesesItem__font_size = -4
