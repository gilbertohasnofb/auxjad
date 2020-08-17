from typing import Optional, Union

import abjad

from ._HarmonicParent import _HarmonicParent


class HarmonicNote(abjad.Note, _HarmonicParent):
    r"""Creates a note with tweaked note head for harmonics. This is a child
    class of |abjad.Note|.

    Basic usage:
        Usage is similar to |abjad.Note|:

        >>> harm = auxjad.HarmonicNote(r"c''4")
        >>> harm.style
        'harmonic'
        >>> abjad.f(harm)
        \tweak style #'harmonic
        c''4

        .. figure:: ../_images/HarmonicNote-jslykzpz7en.png

        And similarly to |abjad.Note|, pitch and duration can be input in
        many different ways:

        >>> harm1 = auxjad.HarmonicNote(r"c''4")
        >>> harm2 = auxjad.HarmonicNote(r"c''", 1 / 4)
        >>> harm3 = auxjad.HarmonicNote(12, 0.25)
        >>> harm4 = auxjad.HarmonicNote(12, abjad.Duration(1, 4))
        >>> staff = abjad.Staff([harm1, harm2, harm3, harm4])
        >>> abjad.f(staff)
        \new Staff
        {
            \tweak style #'harmonic
            c''4
            \tweak style #'harmonic
            c''4
            \tweak style #'harmonic
            c''4
            \tweak style #'harmonic
            c''4
        }

        .. figure:: ../_images/HarmonicNote-kdx8pmkdspn.png

    :attr:`style`:
        When instantiating this class, use the keyword argument :attr:`style`
        to set a different type of note head, such as ``'harmonic-mixed'``:

        >>> harm = auxjad.HarmonicNote(r"c''4",
        ...                            style='harmonic-mixed',
        ...                            )
        >>> harm.style
        'harmonic-mixed'
        >>> abjad.f(harm)
        \tweak style #'harmonic-mixed
        c''4

        .. figure:: ../_images/HarmonicNote-z48i5il6vf.png

    :attr:`~abjad.core.Note.Note.multiplier`:
        Similarly to |abjad.Note|, this class can take multipliers:

        >>> harm = auxjad.HarmonicNote(r"c''4",
        ...                            multiplier=(2, 3),
        ...                            )
        >>> harm.multiplier
        abjad.Multiplier(2, 3)
        >>> abjad.f(harm)
        \tweak style #'harmonic
        c''4 * 2/3

        .. figure:: ../_images/HarmonicNote-4qbhly2hfi.png

    Properties:
        All properties of |abjad.Note| are also available to be read. This
        class also includes a new property named :attr:`style`:

        >>> harm = auxjad.HarmonicNote(r"c''4")
        >>> harm.written_pitch
        "c''"
        >>> harm.written_duration
        1/4
        >>> harm.style
        'harmonic'

        All these properties can be set to different values after
        initialisation:

        >>> harm.written_pitch = 18
        >>> harm.written_duration = abjad.Duration(1, 8)
        >>> harm.style = 'harmonic-mixed'
        >>> harm.written_pitch
        "fs''"
        >>> harm.written_duration
        1/8
        >>> harm.style
        'harmonic-mixed'

    Setting :attr:`style` to ``'flageolet'``:
        To create a harmonic note with a regular note head and with a flageolet
        circle above it, use the style ``'flageolet'``:

        >>> harm = auxjad.HarmonicNote(r"c''1",
        ...                            style='flageolet',
        ...                            )
        >>> harm.style
        'flageolet'
        >>> abjad.f(harm)
        c''1
        \flageolet

        .. figure:: ../_images/HarmonicNote-4q2q7rz65lj.png

    :attr:`markup`:
        To add a markup expression to the harmonic note, use the :attr:`markup`
        optional keyword argument, which takes strings. By default, the markup
        position is above the harmonic note, but this can be overridden using
        the keyword :attr:`direction`, which can take strings as well as
        |abjad.Up| and |abjad.Down|:

        >>> harm1 = auxjad.HarmonicNote(r"d''1")
        >>> harm2 = auxjad.HarmonicNote(r"d''1",
        ...                             markup='III.',
        ...                             )
        >>> harm3 = auxjad.HarmonicNote(r"d''1",
        ...                             markup='III.',
        ...                             direction=abjad.Down)
        >>> staff = abjad.Staff([harm1, harm2, harm3])
        >>> abjad.f(staff)
        \new Staff
        {
            \tweak style #'harmonic
            d''1
            \tweak style #'harmonic
            d''1
            ^ \markup { III. }
            \tweak style #'harmonic
            d''1
            _ \markup { III. }
        }

        .. figure:: ../_images/HarmonicNote-v9uer4i864.png

        Setting :attr:`markup` to ``None`` will remove the markup from the
        note.

        >>> harm = auxjad.HarmonicNote(r"d''1",
        ...                            markup='III.',
        ...                            )
        >>> harm.markup = None
        >>> abjad.f(harm)
        \tweak style #'harmonic
        d''1

        .. figure:: ../_images/HarmonicNote-2gqky0o8dgt.png

    .. error::

        If another markup is attached to the harmonic note, trying to set the
        :attr:`markup` to ``None`` will raise an :exc:`Exception`:

        >>> harm = auxjad.HarmonicNote(r"d''1")
        >>> abjad.attach(abjad.Markup('test'), harm)
        >>> harm.markup = 'III.'
        >>> harm.markup = None
        Exception: multiple indicators attached to client.
    """

    ### CLASS VARIABLES ###

    __slots__ = ('_style',
                 '_direction',
                 '_markup',
                 )

    ### INITIALISER ###

    def __init__(self,
                 *arguments,
                 multiplier: Optional[abjad.typings.DurationTyping] = None,
                 tag: Optional[abjad.Tag] = None,
                 style: str = 'harmonic',
                 markup: Optional[str] = None,
                 direction: Union[str, abjad.enums.VerticalAlignment] = 'up',
                 ):
        r'Initialises self.'
        super().__init__(*arguments, multiplier=multiplier, tag=tag)
        self.style = style
        self._direction = direction
        self.markup = markup

    ### PUBLIC PROPERTIES ###

    @property
    def style(self) -> str:
        r'The style of the harmonic note head.'
        return self._style

    @style.setter
    def style(self,
              style: str,
              ):
        if not isinstance(style, str):
            raise TypeError("'style' must be 'str'")
        self._style = style
        if not self._style == 'flageolet':
            abjad.tweak(self._note_head).style = self._style
        else:
            flageolet = abjad.LilyPondLiteral(r'\flageolet',
                                              format_slot='after',
                                              )
            abjad.attach(flageolet, self)
