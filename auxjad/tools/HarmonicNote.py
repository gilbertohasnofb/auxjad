import abjad


class HarmonicNote(abjad.Note):
    r"""Creates an ``abjad.Note`` with tweaked notehead for harmonics.

    ..  container:: example

        Usage is similar to ``abjad.Note``:

        >>> note = auxjad.HarmonicNote("c''4")
        >>> note.style
        'harmonic'
        >>> abjad.f(note)
        \tweak style #'harmonic
        c''4

        And similarly to ``abjad.Note``, pitch and duration can be input in
        many different ways:

        >>> note1 = auxjad.HarmonicNote("c''4")
        >>> note2 = auxjad.HarmonicNote("c''", 1/4)
        >>> note3 = auxjad.HarmonicNote(12, 0.25)
        >>> note4 = auxjad.HarmonicNote(12, abjad.Duration(1, 4))
        >>> abjad.f(note1)
        \tweak style #'harmonic
        c''4
        >>> abjad.f(note2)
        \tweak style #'harmonic
        c''4
        >>> abjad.f(note3)
        \tweak style #'harmonic
        c''4
        >>> abjad.f(note4)
        \tweak style #'harmonic
        c''4

    ..  container:: example

        When creating an ``HarmonicNote``, use the keyword argument ``style``
        to set a different type of note head, such as ``'harmonic-mixed'``:

        >>> note = auxjad.HarmonicNote("c''4",
        ...                            style='harmonic-mixed',
        ...                            )
        >>> note.style
        'harmonic-mixed'
        >>> abjad.f(note)
        \tweak style #'harmonic-mixed
        c''4

    ..  container:: example

        Similarly to ``abjad.Note``, ``HarmonicNote`` can take multipliers:

        >>> note = auxjad.HarmonicNote("c''4",
        ...                            multiplier=(2, 3),
        ...                            )
        >>> note.multiplier
        abjad.Multiplier(2, 3)
        >>> abjad.f(note)
        \tweak style #'harmonic
        c''4 * 2/3

    ..  container:: example

        All properties of ``abjad.Note`` are also available to be read. This
        class also includes a new property named ``style``:

        >>> note = auxjad.HarmonicNote("c''4")
        >>> note.written_pitch
        "c''"
        >>> note.written_duration
        1/4
        >>> note.style
        'harmonic'

        All these properties can be set to different values after
        initialisation:

        >>> note.written_pitch = 18
        >>> note.written_duration = abjad.Duration(1, 8)
        >>> note.style = 'harmonic-mixed'
        >>> note.written_pitch
        "fs''"
        >>> note.written_duration
        1/8
        >>> note.style
        'harmonic-mixed'

    ..  container:: example

        To create a note with a regular note head and with a flageolet circle
        above it, use the style ``'flageolet'``:

        >>> note = auxjad.HarmonicNote("c''1",
        ...                            style='flageolet',
        ...                            )
        >>> note.style
        'flageolet'
        >>> abjad.f(note)
        c''1
        \flageolet
    """

    def __init__(self,
                 *arguments,
                 multiplier: abjad.typings.DurationTyping = None,
                 tag: abjad.Tag = None,
                 style: str = 'harmonic',
                 ):
        super().__init__(*arguments, multiplier=multiplier, tag=tag)
        self._style = style
        self.style = self._style

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
        if not self._style == 'flageolet':
            abjad.tweak(self.note_head).style = self._style
        else:
            flageolet = abjad.LilyPondLiteral(r'\flageolet',
                                              format_slot='after',
                                              )
            abjad.attach(flageolet, self)
