from typing import Union

import abjad


class _HarmonicParent:
    r"""This is the parent class of :class:`auxjad.ArtificialHarmonic` and
    :class:`auxjad.HarmonicNote`. It implements two common properties with
    ``@property`` and ``@setter`` decorators.
    """

    ### CLASS VARIABLES ###

    # due to subclasses using multiple inheritance, '_markup' and '_direction'
    # are added to their __slots__ since you cannot inherit from multiple
    # classes with non-empty __slots__
    __slots__ = ()

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self) -> Union[str, abjad.enums.VerticalAlignment]:
        r'The direction of the harmonic note head.'
        return self._direction

    @direction.setter
    def direction(self,
                  direction: Union[str, abjad.enums.VerticalAlignment],
                  ):
        if direction is not None:
            if not isinstance(direction, (str, abjad.enums.VerticalAlignment)):
                raise TypeError("'direction' must be 'str', None, or either "
                                "'abjad.Up' or 'abjad.Down'")
        self._direction = direction
        # detaching and reattaching markup to apply new direction
        markup = self._markup
        self.markup = None
        self.markup = markup

    @property
    def markup(self) -> str:
        r'The markup of the harmonic note head.'
        return self._markup

    @markup.setter
    def markup(self,
               markup: str,
               ):
        if markup is not None:
            if not isinstance(markup, str):
                raise TypeError("'markup' must be 'str'")
            self._markup = markup
            markup = abjad.Markup(self._markup,
                                  direction=self._direction,
                                  )
            abjad.attach(markup, self)
        else:
            self._markup = markup
            if abjad.inspect(self).indicator(abjad.Markup):
                abjad.detach(abjad.Markup, self)
