import abjad


class _HarmonicParent:
    r"""This is the parent class of the ArtificialHarmonic and HarmonicNote
    classes. It implements two common properties with @property and @setter
    decorators.
    """

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self) -> (str, abjad.enums.VerticalAlignment):
        r'The direction of the harmonic note head.'
        return self._direction

    @direction.setter
    def direction(self,
                  direction: (str, abjad.enums.VerticalAlignment),
                  ):
        if direction:
            if not isinstance(direction, (str, abjad.enums.VerticalAlignment)):
                raise TypeError("'direction' must be 'str', None, or either "
                                "'abjad.Up' or 'abjad.Down'")
        self._direction = direction
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
        if markup:
            if not isinstance(markup, str):
                raise TypeError("'markup' must be 'str'")
            self._markup = markup
            markup = abjad.Markup(self._markup,
                                  direction=self._direction,
                                  )
            abjad.attach(markup, self)
        else:
            self._markup = markup
            markup = abjad.inspect(self).indicator(abjad.Markup)
            if markup:
                abjad.detach(abjad.Markup, self)
