import abjad


class NumericOttava(abjad.Ottava):
    r"""LilyPond's ``\ottava`` command tweaked to output numeric ottavation
    (e.g. ``"8"`` instead of ``"8va"`` or ``"8vb"``, ``"15"`` instead of
    ``"15va"`` or ``"15vb"``, etc).

    Basic usage:
        Usage is similar to |abjad.Ottava|:

        >>> staff = abjad.Staff(
        ...     r"c'''4 d'''4 e'''4 f'''4 g'''4 a'''4 b'''4 c''''4"
        ... )
        >>> ottava = auxjad.NumericOttava(1)
        >>> abjad.attach(ottava, staff[0])
        >>> ottava = auxjad.NumericOttava(2)
        >>> abjad.attach(ottava, staff[4])
        >>> ottava = auxjad.NumericOttava(0, format_slot='after')
        >>> abjad.attach(ottava, staff[-1])
        >>> abjad.f(staff)
        \new Staff
        {
            \ottava 1 \set Staff.ottavation = "8"
            c'''4
            d'''4
            e'''4
            f'''4
            \ottava 2 \set Staff.ottavation = "15"
            g'''4
            a'''4
            b'''4
            c''''4
            \ottava 0
        }

        .. figure:: ../_images/NumericOttava-bB64Wtgtgz.png

        Numeric ottavation is also used for ottava bassa:

        >>> staff = abjad.Staff(
        ...     r"\clef bass c,4 b,,4 a,,4 g,,4 f,,4 e,,4 d,,4 c,,4"
        ... )
        >>> ottava = auxjad.NumericOttava(-1)
        >>> abjad.attach(ottava, staff[0])
        >>> ottava = auxjad.NumericOttava(-2)
        >>> abjad.attach(ottava, staff[4])
        >>> ottava = auxjad.NumericOttava(0, format_slot='after')
        >>> abjad.attach(ottava, staff[-1])
        >>> abjad.f(staff)
        \new Staff
        {
            \ottava -1 \set Staff.ottavation = "8"
            \clef "bass"
            c,4
            b,,4
            a,,4
            g,,4
            \ottava -2 \set Staff.ottavation = "15"
            f,,4
            e,,4
            d,,4
            c,,4
            \ottava 0
        }

        .. figure:: ../_images/NumericOttava-nJrbuohDvN.png
    """

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self) -> abjad.LilyPondFormatBundle:
        bundle = abjad.LilyPondFormatBundle()
        n = self.n or 0
        string = rf'\ottava {n}'
        if n != 0:
            ottavation_number = abs(n) * 7 + 1
            string += rf' \set Staff.ottavation = "{ottavation_number}"'
        if self.format_slot in ('before', None):
            bundle.before.commands.append(string)
        else:
            assert self.format_slot == 'after'
            bundle.after.commands.append(string)
        return bundle
