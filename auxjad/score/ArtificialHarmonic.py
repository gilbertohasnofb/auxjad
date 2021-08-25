from typing import Optional, Union

import abjad

from ._HarmonicParent import _HarmonicParent


class ArtificialHarmonic(abjad.Chord, _HarmonicParent):
    r"""Creates a chord with a tweaked top note head for notating artificial
    harmonics. This is a child class of |abjad.Chord|.

    Basic usage:
        Usage is similar to |abjad.Chord|:

        >>> harm = auxjad.ArtificialHarmonic("<g c'>4")
        >>> harm.style
        "#'harmonic"
        >>> abjad.show(harm)

        ..  docs::

            <
                g
                \tweak style #'harmonic
                c'
            >4

        ..  figure:: ../_images/ArtificialHarmonic-16am9cj6p9u.png

        And similarly to |abjad.Chord|, pitch and duration can be input in
        many different ways:

        >>> harm1 = auxjad.ArtificialHarmonic(r"<g c'>4")
        >>> harm2 = auxjad.ArtificialHarmonic(["g", "c'"], 1 / 4)
        >>> harm3 = auxjad.ArtificialHarmonic([-5, 0], 0.25)
        >>> harm4 = auxjad.ArtificialHarmonic([-5, 0], abjad.Duration(1, 4))
        >>> staff = abjad.Staff([harm1, harm2, harm3, harm4])
        >>> abjad.show(staff)

        ..  docs::

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

        ..  figure:: ../_images/ArtificialHarmonic-je277bmakgs.png

    ..  error::
        It is important to note that this class can only be initialised with
        exactly two pitches. Any other number of pitches will raise a
        :exc:`ValueError`:

        >>> auxjad.ArtificialHarmonic(r"<g c' d'>4")
        ValueError: 'ArtificialHarmonic' requires exactly two
        'written_pitches' for initialisation

    :attr:`style`:
        When instantiating this class, use the keyword argument :attr:`style`
        to set a different type of note head for the top note, such as
        ``"#'harmonic-mixed"``:

        >>> harm = auxjad.ArtificialHarmonic(r"<g c'>4",
        ...                                  style="#'harmonic-mixed",
        ...                                  )
        >>> harm.style
        "#'harmonic-mixed"
        >>> abjad.show(harm)

        ..  docs::

            <
                g
                \tweak style #'harmonic-mixed
                c'
            >4

        ..  figure:: ../_images/ArtificialHarmonic-ohqb65228iq.png

    :attr:`is_parenthesized`:
        To notate natural harmonics with a parenthesised pitch for the open
        string at the bottom of the interval, set the keyword
        :attr:`is_parenthesized` to ``True``.

        >>> harm = auxjad.ArtificialHarmonic(r"<g c'>4",
        ...                                  is_parenthesized=True,
        ...                                  )
        >>> harm.is_parenthesized
        True
        >>> abjad.show(harm)

        ..  docs::

            <
                \parenthesize
                \tweak ParenthesesItem.font-size -4
                g
                \tweak style #'harmonic
                c'
            >4

        ..  figure:: ../_images/ArtificialHarmonic-2q3jkx33yvl.png

    :attr:`~abjad.core.Chord.Chord.multiplier`:
        Similarly to |abjad.Chord|, this class can take multipliers:

        >>> harm = auxjad.ArtificialHarmonic(r"<g c'>4",
        ...                                  multiplier=(2, 3),
        ...                                  )
        >>> harm.multiplier
        abjad.Multiplier(2, 3)
        >>> abjad.show(harm)

        ..  docs::

            <
                g
                \tweak style #'harmonic
                c'
            >4 * 2/3

        ..  figure:: ../_images/ArtificialHarmonic-ouhdk3ugkcs.png

    Properties:
        All properties of |abjad.Chord| are also available to be read. This
        class also includes two new properties named :attr:`style` and
        :attr:`is_parenthesized`:

        >>> harm = auxjad.ArtificialHarmonic(r"<g c'>4")
        >>> harm.written_pitches
        "g c'"
        >>> harm.written_duration
        1/4
        >>> harm.style
        "#'harmonic"
        >>> harm.is_parenthesized
        False

        All these properties can be set to different values after
        initialisation:

        >>> harm.written_pitches = [-5, 2]
        >>> harm.written_duration = abjad.Duration(1, 8)
        >>> harm.style = "#'harmonic-mixed"
        >>> harm.is_parenthesized = True
        >>> harm.written_pitches
        "g d'"
        >>> harm.written_duration
        1/8
        >>> harm.style
        "#'harmonic-mixed"
        >>> harm.is_parenthesized
        True

    :meth:`sounding_pitch` and :meth:`sounding_note`:
        The methods :meth:`sounding_pitch` and :meth:`sounding_note` return the
        sounding pitch and sounding note, respectively. Their types are
        |abjad.Pitch| and |abjad.Note|, respectively.

        >>> harmonics = [ArtificialHarmonic(r"<g b>4"),
        ...              ArtificialHarmonic(r"<g c'>4"),
        ...              ArtificialHarmonic(r"<g d'>4"),
        ...              ArtificialHarmonic(r"<g e'>4"),
        ...              ArtificialHarmonic(r"<g g'>4"),
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

    :meth:`sounding_note` and indicators:
        The note created by :meth:`sounding_note` inherits all indicators of
        the artificial harmonic.

        >>> harm = auxjad.ArtificialHarmonic(r"<g c'>4-.\pp")
        >>> abjad.show(harm.sounding_note())

        ..  docs::

            g''4
            \pp
            - \staccato

        ..  figure:: ../_images/ArtificialHarmonic-dfabdv155mu.png

    ..  error::

        Both :meth:`sounding_pitch` and :meth:`sounding_note` methods raise a
        :exc:`ValueError` exception when it cannot calculate the sounding pitch
        for the given interval.

        >>> harm = auxjad.ArtificialHarmonic(r"<g ef'>4")
        >>> harm.sounding_pitch()
        ValueError: cannot calculate sounding pitch for given interval
        >>> harm.sounding_note()
        ValueError: cannot calculate sounding pitch for given interval

    :attr:`markup`:
        To add a markup expression to the artificial harmonic, use the
        :attr:`markup` optional keyword argument, which takes strings. By
        default, the markup position is above the harmonic note, but this can
        be overridden using the keyword :attr:`direction`, which can take
        strings as well as ``abjad.Up`` and ``abjad.Down``:

        >>> harm1 = auxjad.ArtificialHarmonic(r"<a d'>1")
        >>> harm2 = auxjad.ArtificialHarmonic(r"<a d'>1",
        ...                                   markup='I.',
        ...                                   )
        >>> harm3 = auxjad.ArtificialHarmonic(r"<a d'>1",
        ...                                   markup='I.',
        ...                                   direction=abjad.Down)
        >>> staff = abjad.Staff([harm1, harm2, harm3])
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                <
                    a
                    \tweak style #'harmonic
                    d'
                >1
                \once \override TextScript.parent-alignment-X = 0
                \once \override TextScript.self-alignment-X = 0
                <
                    a
                    \tweak style #'harmonic
                    d'
                >1
                ^ \markup { I. }
                \once \override TextScript.parent-alignment-X = 0
                \once \override TextScript.self-alignment-X = 0
                <
                    a
                    \tweak style #'harmonic
                    d'
                >1
                _ \markup { I. }
            }

        ..  figure:: ../_images/ArtificialHarmonic-teysjphrrpn.png

        Setting :attr:`markup` to ``None`` will remove the markup from the
        note.

        >>> harm = auxjad.ArtificialHarmonic(r"<a d'>1",
        ...                                  markup='I.',
        ...                                  )
        >>> harm.markup = None
        >>> abjad.show(harm)

        ..  docs::

            <
                a
                \tweak style #'harmonic
                d'
            >1

        ..  figure:: ../_images/ArtificialHarmonic-nov336z64r.png

    :attr:`centre_markup`:
        When a markup expression is added to the harmonic note by using the
        :attr:`markup` optional keyword argument, it will be automatically
        centred above the note (as the main purpose of this markup is to show
        string numbers). To disable this behaviour, set :attr:`centre_markup`
        to ``False``. Compare:

        >>> harm1 = auxjad.ArtificialHarmonic(r"<a d'>1",
        ...                                   markup='III.',
        ...                                   )
        >>> abjad.show(harm1)

        ..  docs::

            \once \override TextScript.parent-alignment-X = 0
            \once \override TextScript.self-alignment-X = 0
            <
                bf'
                \tweak style #'harmonic
                ef''
            >1
            ^ \markup { III. }

        ..  figure:: ../_images/ArtificialHarmonic-cFjQuNmS3p.png

        >>> harm2 = auxjad.ArtificialHarmonic(r"<a d'>1",
        ...                                   markup='III.',
        ...                                   centre_markup=False,
        ...                                   )
        >>> abjad.show(harm2)

        ..  docs::

            <
                bf'
                \tweak style #'harmonic
                ef''
            >1
            ^ \markup { III. }

        ..  figure:: ../_images/ArtificialHarmonic-gfhbSlQPlK.png

    ..  error::

        If another markup is attached to the harmonic note, trying to set the
        :attr:`markup` property to ``None`` will raise an :exc:`Exception`:

        >>> harm = auxjad.ArtificialHarmonic(r"<a d'>1")
        >>> abjad.attach(abjad.Markup('test'), harm)
        >>> harm.markup = 'I.'
        >>> harm.markup = None
        Exception: multiple indicators attached to client.
    """

    ### CLASS VARIABLES ###

    __slots__ = ('_style',
                 '_is_parenthesized',
                 '_direction',
                 '_centre_markup',
                 '_markup',
                 )

    ### INITIALISER ###

    def __init__(self,
                 *arguments,
                 multiplier: Optional[abjad.typings.DurationTyping] = None,
                 tag: Optional[abjad.Tag] = None,
                 style: str = "#'harmonic",
                 is_parenthesized: bool = False,
                 markup: Optional[str] = None,
                 centre_markup: bool = True,
                 direction: Union[str, abjad.enums.VerticalAlignment] = 'up',
                 ) -> None:
        r'Initialises self.'
        super().__init__(*arguments, multiplier=multiplier, tag=tag)
        if len(self.written_pitches) != 2:
            raise ValueError("'ArtificialHarmonic' requires exactly two "
                             "'written_pitches' for initialisation")
        self.style = style
        self.is_parenthesized = is_parenthesized
        self._direction = direction
        self.centre_markup = centre_markup
        self.markup = markup

    ### PUBLIC METHODS ###

    def sounding_pitch(self) -> abjad.Pitch:
        r'Returns the sounding pitch of the harmonic as an |abjad.Pitch|.'
        interval = abs(self.written_pitches[1]
                       - self.written_pitches[0]).semitones
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
            sounding_pitch = (self.written_pitches[0]
                              + sounding_pitch_dict[interval])
        except KeyError as err:
            raise ValueError('cannot calculate sounding pitch for given '
                             'interval') from err
        return sounding_pitch

    def sounding_note(self) -> abjad.Note:
        r'Returns the sounding note of the harmonic as an |abjad.Note|.'
        note = abjad.Note(self.sounding_pitch(), self._written_duration)
        for indicator in abjad.get.indicators(self):
            abjad.attach(indicator, note)
        return note

    ### PRIVATE METHODS ###

    def _attach_centre_markup(self) -> None:
        r'Attaches the centre markup tweaks.'
        literal1 = abjad.LilyPondLiteral(
            r'\once \override TextScript.parent-alignment-X = 0'
        )
        literal2 = abjad.LilyPondLiteral(
            r'\once \override TextScript.self-alignment-X = 0'
        )
        abjad.attach(literal1, self)
        abjad.attach(literal2, self)

    def _detach_centre_markup(self) -> None:
        r'Detaches the centre markup tweaks.'
        literal1 = abjad.LilyPondLiteral(
            r'\once \override TextScript.parent-alignment-X = 0'
        )
        literal2 = abjad.LilyPondLiteral(
            r'\once \override TextScript.self-alignment-X = 0'
        )
        if abjad.get.indicator(self, literal1):
            abjad.detach(literal1, self)
        if abjad.get.indicator(self, literal2):
            abjad.detach(literal2, self)

    ### PUBLIC PROPERTIES ###

    @property
    def written_pitches(self) -> abjad.pitch.segments.PitchSegment:
        r'The written pitches of the two note heads.'
        return abjad.pitch.segments.PitchSegment(
            items=(note_head.written_pitch for note_head in self._note_heads),
            item_class=abjad.pitch.pitches.NamedPitch,
        )

    @written_pitches.setter
    def written_pitches(self,
                        written_pitches,
                        ) -> None:
        written_pitches_ = abjad.PitchSegment(written_pitches)
        if len(written_pitches_) != 2:
            raise ValueError("'ArtificialHarmonic' requires exactly two "
                             "pitches")
        for index, pitch in enumerate(written_pitches_):
            self._note_heads[index].written_pitch = pitch

    @property
    def style(self) -> str:
        r'The style of the upper note head.'
        return self._style

    @style.setter
    def style(self,
              style: str,
              ) -> None:
        if not isinstance(style, str):
            raise TypeError("'style' must be 'str'")
        self._style = style
        abjad.tweak(self._note_heads[1]).style = self._style

    @property
    def centre_markup(self) -> bool:
        r"""Tweaks the markup of the harmonic note head to be centred or not
        as LilyPond doesn't centralises markups above note heads by default.
        """
        return self._centre_markup

    @centre_markup.setter
    def centre_markup(self,
                      centre_markup: bool,
                      ) -> None:
        if not isinstance(centre_markup, bool):
            raise TypeError("'style' must be 'bool'")
        self._centre_markup = centre_markup

    @property
    def is_parenthesized(self) -> bool:
        r'Whether the bottom note head is parenthesised or not.'
        return self._is_parenthesized

    @is_parenthesized.setter
    def is_parenthesized(self,
                         is_parenthesized: bool,
                         ) -> None:
        if not isinstance(is_parenthesized, bool):
            raise TypeError("'is_parenthesized' must be 'bool'")
        self._is_parenthesized = is_parenthesized
        self._note_heads[0].is_parenthesized = self._is_parenthesized
        if self._is_parenthesized:
            abjad.tweak(self._note_heads[0]).ParenthesesItem__font_size = -4

    @property
    def markup(self) -> str:
        r'The markup of the harmonic note head.'
        return self._markup

    @markup.setter
    def markup(self,
               markup: str,
               ) -> None:
        if markup is not None:
            if not isinstance(markup, str):
                raise TypeError("'markup' must be 'str'")
            self._markup = markup
            markup = abjad.Markup(self._markup,
                                  direction=self._direction,
                                  )
            abjad.attach(markup, self)
            if self._centre_markup:
                self._attach_centre_markup()
            else:
                self._detach_centre_markup()
        else:
            self._markup = markup
            if abjad.get.indicator(self, abjad.Markup):
                abjad.detach(abjad.Markup, self)
            self._detach_centre_markup()
