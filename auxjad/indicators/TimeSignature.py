import abjad


class TimeSignature(abjad.TimeSignature):
    r"Time signature."

    def simplify_ratio(self,
                       *,
                       min_denominator: int = 4,
                       ) -> None:
        r"""Simplifies the ratio of an |abjad.TimeSignature| according to a
        minimum denominator value. Mutates the ratio in place and has no return
        value. Note that Auxjad adds this function as an extension method to
        |abjad.TimeSignature| (see usage below).

        Basic usage:
            By default, this method simplifies the ratio of
            ``numerator / denominator`` using a minimum denominator value of
            ``4`` (that is, the denominator will not get smaller than ``4``).
            In the case below, ``(2, 4)`` is the simplest representation of the
            ratio ``(4, 8)`` with a denominator equal to or larger than ``4``.

            >>> time_signature = abjad.TimeSignature((4, 8))
            >>> time_signature.simplify_ratio()
            >>> time_signature
            abjad.TimeSignature((2, 4))
            >>> time_signature = abjad.TimeSignature((1, 1))
            >>> time_signature.simplify_ratio()
            >>> time_signature
            abjad.TimeSignature((4, 4))

            If a ratio cannot be simplified at all, the function returns a time
            signature with the original ratio.

            >>> time_signature = abjad.TimeSignature((7, 8))
            >>> time_signature.simplify_ratio()
            >>> time_signature
            abjad.TimeSignature((7, 8))

            It also simplifies ratios even if the minimum denominator cannot be
            reached.

            >>> time_signature = abjad.TimeSignature((10, 16))
            >>> time_signature.simplify_ratio()
            >>> time_signature
            abjad.TimeSignature((5, 8))

        ``min_denominator``:
            The ``min_denominator`` can be set to values other than ``4``. If
            set to ``2``, the simplest representaion of the ratio ``(4, 8)``
            becomes ``(1, 2)``.

            >>> time_signature = abjad.TimeSignature((4, 8))
            >>> time_signature.simplify_ratio(min_denominator=2)
            >>> time_signature
            abjad.TimeSignature((1, 2))
            >>> time_signature = abjad.TimeSignature((1, 1))
            >>> time_signature.simplify_ratio(min_denominator=1)
            >>> time_signature
            abjad.TimeSignature((1, 1))
        """
        if not isinstance(min_denominator, int):
            raise TypeError("'min_denominator' must be 'int'")

        while self._denominator < min_denominator:
            self._numerator *= 2
            self._denominator *= 2
        while True:
            if (self._numerator % 2 == 0 and self._denominator % 2 == 0
                    and self._denominator >= 2 * min_denominator):
                self._numerator //= 2
                self._denominator //= 2
            else:
                return


### EXTENSION METHODS ###

abjad.TimeSignature.simplify_ratio = TimeSignature.simplify_ratio
