from typing import Union

import abjad


class Score(abjad.Score):
    r"Score."

    def add_final_bar_line(self,
                           bar_line: Union[str, abjad.BarLine] = "|.",
                           *,
                           to_each_voice: bool = False,
                           ) -> None:
        r"""Adds a final bar line to all components of |abjad.Score|. Note that
        Auxjad adds this function as an extension method to |abjad.Score| (see
        usage below).

        Basic usage:
            >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
            >>> score = abjad.Score([staff])
            >>> abjad.show(score)

            ..  docs::

                \new Score
                <<
                    \new Staff
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                >>

            ..  figure:: ../_images/Score-fdO5TP6ff9.png

            >>> score.add_final_bar_line()
            >>> abjad.show(score)

            ..  docs::

                \new Score
                <<
                    \new Staff
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                        \bar "|."
                    }
                >>

            ..  figure:: ../_images/Score-SHok9MqNVh.png

        Multiple staves:
            Works with multiple staves:

            >>> staff_1 = abjad.Staff(r"c''1 d''1 e''1 f''1")
            >>> staff_2 = abjad.Staff(r"c'1 d'1 e'1 f'1")
            >>> score = abjad.Score([staff_1, staff_2])
            >>> score.add_final_bar_line()
            >>> abjad.show(score)

            ..  docs::

                \new Score
                <<
                    \new Staff
                    {
                        c''1
                        d''1
                        e''1
                        f''1
                        \bar "|."
                    }
                    \new Staff
                    {
                        c'1
                        d'1
                        e'1
                        f'1
                        \bar "|."
                    }
                >>

            ..  figure:: ../_images/Score-oCR5QGUz6W.png

            Each stave will receive their own final bar line, which can be
            useful when part extracting:

            >>> abjad.show(staff_1)

            ..  docs::

                \new Staff
                {
                    c''1
                    d''1
                    e''1
                    f''1
                    \bar "|."
                }

            ..  figure:: ../_images/Score-tTXh7GOAop.png

            >>> abjad.show(staff_2)

            ..  docs::

                \new Staff
                {
                    c'1
                    d'1
                    e'1
                    f'1
                    \bar "|."
                }

            ..  figure:: ../_images/Score-MRWgOyiqt3.png

        ``to_each_voice``
            When multiple voices are present in a staff, the final bar line is
            added to the last voice only:

            >>> voice_1 = abjad.Voice(r"c''1 d''1 e''1 f''1")
            >>> voice_2 = abjad.Voice(r"c'2 d'2 e'2 f'2 g'2 a'2 b'2 c''2")
            >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
            >>> score = auxjad.Score([staff])
            >>> score.add_final_bar_line()
            >>> abjad.show(score)

            ..  docs::

                \new Score
                <<
                    \new Staff
                    <<
                        \new Voice
                        {
                            \voiceOne
                            c''1
                            d''1
                            e''1
                            f''1
                        }
                        \new Voice
                        {
                            \voiceTwo
                            c'2
                            d'2
                            e'2
                            f'2
                            g'2
                            a'2
                            b'2
                            c''2
                            \bar "|."
                        }
                    >>
                >>

            ..  figure:: ../_images/Score-8mnllVCEoL.png

            >>> abjad.show(voice_1)

            ..  docs::

                \new Voice
                {
                    \voiceOne
                    c''1
                    d''1
                    e''1
                    f''1
                }

            ..  figure:: ../_images/Score-DPW54DDeyM.png

            >>> abjad.show(voice_2)

            ..  docs::

                \new Voice
                {
                    \voiceTwo
                    c'2
                    d'2
                    e'2
                    f'2
                    g'2
                    a'2
                    b'2
                    c''2
                    \bar "|."
                }

            ..  figure:: ../_images/Score-ua8cZAITB5.png

            Setting ``to_each_voice`` to ``True`` will add a bar line to each
            voice in a staff:

            >>> voice_1 = abjad.Voice(r"c''1 d''1 e''1 f''1")
            >>> voice_2 = abjad.Voice(r"c'2 d'2 e'2 f'2 g'2 a'2 b'2 c''2")
            >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
            >>> score = auxjad.Score([staff])
            >>> score.add_final_bar_line(to_each_voice=True)
            >>> abjad.show(voice_1)

            ..  docs::

                \new Voice
                {
                    \voiceOne
                    c''1
                    d''1
                    e''1
                    f''1
                    \bar "|."
                }

            ..  figure:: ../_images/Score-adtLRR3v1W.png

            >>> abjad.show(voice_2)

            ..  docs::

                \new Voice
                {
                    \voiceTwo
                    c'2
                    d'2
                    e'2
                    f'2
                    g'2
                    a'2
                    b'2
                    c''2
                    \bar "|."
                }

            ..  figure:: ../_images/Score-DqhspXgvIJ.png

        ..  warning::

            If voices do not end together then manually adding bar lines will
            be required:

            >>> voice_1 = abjad.Voice(r"c''1 d''1 e''1 f''1")
            >>> voice_2 = abjad.Voice(r"c'1 d'1 e'1")
            >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
            >>> score = auxjad.Score([staff])
            >>> score.add_final_bar_line(to_each_voice=True)
            >>> abjad.show(score)

            ..  docs::

                \new Score
                <<
                    \new Staff
                    <<
                        \new Voice
                        {
                            \voiceOne
                            c''1
                            d''1
                            e''1
                            f''1
                            \bar "|."
                        }
                        \new Voice
                        {
                            \voiceTwo
                            c'1
                            d'1
                            e'1
                            \bar "|."
                        }
                    >>
                >>

            ..  figure:: ../_images/Score-duPkS4pJGc.png

    argument:
        The default bar line is of type ``'|.'``. To change this behaviour,
        call this method with an argument of type :obj:`str` or |abjad.BarLine|
        with the desired bar line type:

        >>> staff_1 = abjad.Staff(r"c''1 d''1 e''1 f''1")
        >>> staff_2 = abjad.Staff(r"c'1 d'1 e'1 f'1")
        >>> score = auxjad.Score([staff_1, staff_2])
        >>> score.add_final_bar_line(abjad.BarLine(":|."))
        >>> abjad.show(score)

        ..  docs::

            \new Score
            <<
                \new Staff
                {
                    c''1
                    d''1
                    e''1
                    f''1
                    \bar ":|."
                }
                \new Staff
                {
                    c'1
                    d'1
                    e'1
                    f'1
                    \bar ":|."
                }
            >>

        ..  figure:: ../_images/Score-3JvhD9DKvE.png
        """
        if not isinstance(bar_line, (str, abjad.BarLine)):
            raise TypeError("argument must be 'str' or 'abjad.BarLine'")
        if not isinstance(to_each_voice, bool):
            raise TypeError("'to_each_voice' must be 'bool'")
        if isinstance(bar_line, str):
            bar_line = abjad.BarLine(bar_line)
        if not to_each_voice:
            for staff in abjad.Iteration(self).components(abjad.Staff):
                last_leaf = abjad._iterate._get_leaf(staff, -1)
                abjad.attach(bar_line, last_leaf, context='Staff')
        else:
            for staff in abjad.Iteration(self).components(abjad.Staff):
                voices = [voice for voice
                          in abjad.Iteration(staff).components(abjad.Voice)]
                if len(voices) == 0:
                    last_leaf = abjad._iterate._get_leaf(staff, -1)
                    abjad.attach(bar_line, last_leaf, context='Staff')
                else:
                    for voice in abjad.Iteration(self).components(abjad.Voice):
                        last_leaf = abjad._iterate._get_leaf(voice, -1)
                        abjad.attach(bar_line, last_leaf, context='Voice')

    def add_double_bar_lines_before_time_signatures(
        self,
        *,
        to_each_voice: bool = False,
    ) -> None:
        r"""Adds double bar lines to all components of |abjad.Score| before
        every time signature changes. Note that Auxjad adds this function as an
        extension method to |abjad.Score| (see usage below).

        Basic usage:
            >>> staff = abjad.Staff(
            ...     r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
            ... )
            >>> score = abjad.Score([staff])
            >>> abjad.show(score)

            ..  docs::

                \new Score
                <<
                    \new Staff
                    {
                        \time 3/4
                        c'2.
                        \time 4/4
                        d'1
                        e'1
                        \time 6/4
                        f'2.
                        g'2.
                    }
                >>

            ..  figure:: ../_images/Score-65l45tLipK.png

            >>> score.add_double_bar_lines_before_time_signatures()
            >>> abjad.show(score)

            ..  docs::

                \new Score
                <<
                    \new Staff
                    {
                        \time 3/4
                        c'2.
                        \bar "||"
                        \time 4/4
                        d'1
                        e'1
                        \bar "||"
                        \time 6/4
                        f'2.
                        g'2.
                    }
                >>

            ..  figure:: ../_images/Score-cjmOgHxSJH.png

        Multiple staves:
            Works with multiple staves:

            >>> staff_1 = abjad.Staff(
            ...     r"\time 3/4 c''2. \time 4/4 d''1 e''1 "
            ...     "\time 6/4 f''2. g''2."
            ... )
            >>> staff_2 = abjad.Staff(
            ...     r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
            ... )
            >>> score = abjad.Score([staff_1, staff_2])
            >>> score.add_double_bar_lines_before_time_signatures()
            >>> abjad.show(score)

            ..  docs::

                \new Score
                <<
                    \new Staff
                    {
                        \time 3/4
                        c''2.
                        \bar "||"
                        \time 4/4
                        d''1
                        e''1
                        \bar "||"
                        \time 6/4
                        f''2.
                        g''2.
                    }
                    \new Staff
                    {
                        \time 3/4
                        c'2.
                        \bar "||"
                        \time 4/4
                        d'1
                        e'1
                        \bar "||"
                        \time 6/4
                        f'2.
                        g'2.
                    }
                >>

            ..  figure:: ../_images/Score-cnkUgFuYmI.png

            Each stave will receive their own double bar lines, which can be
            useful when part extracting:

            >>> abjad.show(staff_1)

            ..  docs::

                \new Staff
                {
                    \time 3/4
                    c''2.
                    \bar "||"
                    \time 4/4
                    d''1
                    e''1
                    \bar "||"
                    \time 6/4
                    f''2.
                    g''2.
                }

            ..  figure:: ../_images/Score-TZaC5C12yA.png

            >>> abjad.show(staff_2)

            ..  docs::

                \new Staff
                {
                    \time 3/4
                    c'2.
                    \bar "||"
                    \time 4/4
                    d'1
                    e'1
                    \bar "||"
                    \time 6/4
                    f'2.
                    g'2.
                }

            ..  figure:: ../_images/Score-wZgCbZi8JD.png

        ``to_each_voice``
            When multiple voices are present in a staff, double bar lines will
            be added to the last voice only:

            >>> voice_1 = abjad.Voice(
            ...     r"\time 3/4 c''2. \time 4/4 d''1 e''1 "
            ...     "\time 6/4 f''2. g''2."
            ... )
            >>> voice_2 = abjad.Voice(
            ...     r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
            ... )
            >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
            >>> score = auxjad.Score([staff])
            >>> score.add_double_bar_lines_before_time_signatures()
            >>> abjad.show(score)

            ..  docs::

                \new Score
                <<
                    \new Staff
                    <<
                        \new Voice
                        {
                            \voiceOne
                            \time 3/4
                            c''2.
                            \time 4/4
                            d''1
                            e''1
                            \time 6/4
                            f''2.
                            g''2.
                        }
                        \new Voice
                        {
                            \voiceTwo
                            \time 3/4
                            c'2.
                            \bar "||"
                            \time 4/4
                            d'1
                            e'1
                            \bar "||"
                            \time 6/4
                            f'2.
                            g'2.
                        }
                    >>
                >>

            ..  figure:: ../_images/Score-F6f5a6z3ly.png

            >>> abjad.show(voice_1)

            ..  docs::

                \new Voice
                {
                    \voiceOne
                    \time 3/4
                    c''2.
                    \time 4/4
                    d''1
                    e''1
                    \time 6/4
                    f''2.
                    g''2.
                }

            ..  figure:: ../_images/Score-FEAvA2mn1t.png

            >>> abjad.show(voice_2)

            ..  docs::

                \new Voice
                {
                    \voiceTwo
                    \time 3/4
                    c'2.
                    \bar "||"
                    \time 4/4
                    d'1
                    e'1
                    \bar "||"
                    \time 6/4
                    f'2.
                    g'2.
                }

            ..  figure:: ../_images/Score-QKhtZj82cG.png

            Setting ``to_each_voice`` to ``True`` will add a bar line to each
            voice in a staff:

            >>> voice_1 = abjad.Voice(
            ...     r"\time 3/4 c''2. \time 4/4 d''1 e''1 "
            ...     "\time 6/4 f''2. g''2."
            ... )
            >>> voice_2 = abjad.Voice(
            ...     r"\time 3/4 c'2. \time 4/4 d'1 e'1 \time 6/4 f'2. g'2."
            ... )
            >>> staff = abjad.Staff([voice_1, voice_2], simultaneous=True)
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
            >>> score = auxjad.Score([staff])
            >>> score.add_double_bar_lines_before_time_signatures(
            ...     to_each_voice=True,
            ... )
            >>> abjad.show(voice_1)

            ..  docs::

                \new Voice
                {
                    \voiceOne
                    \time 3/4
                    c''2.
                    \bar "||"
                    \time 4/4
                    d''1
                    e''1
                    \bar "||"
                    \time 6/4
                    f''2.
                    g''2.
                }

            ..  figure:: ../_images/Score-n5x7JhOHy6.png

            >>> abjad.show(voice_2)

            ..  docs::

                \new Voice
                {
                    \voiceTwo
                    \time 3/4
                    c'2.
                    \bar "||"
                    \time 4/4
                    d'1
                    e'1
                    \bar "||"
                    \time 6/4
                    f'2.
                    g'2.
                }

            ..  figure:: ../_images/Score-tAXRWLGxMp.png

        Multi-measure rests:
            This method can handle multi-measure rests.

            >>> staff = abjad.Staff(
            ...     r"\time 3/4 R1 * 3/4 "
            ...     r"\time 4/4 R1 * 2 "
            ...     r"\time 6/4 R1 * 6/4 "
            ...     r"\time 4/4 R1"
            ... )
            >>> score = abjad.Score([staff])
            >>> score.add_double_bar_lines_before_time_signatures()
            >>> abjad.show(score)

            ..  docs::

                \new Score
                <<
                    \new Staff
                    {
                        \time 3/4
                        R1 * 3/4
                        \bar "||"
                        \time 4/4
                        R1 * 2
                        \bar "||"
                        \time 6/4
                        R1 * 3/2
                        \bar "||"
                        \time 4/4
                        R1
                    }
                >>

            ..  figure:: ../_images/Score-nwYMM8JAYR.png

        Input with bar lines:
            If the score already contains non-standard bar lines at points
            where a time signature changes, only those of types ``"|"`` and
            ``""`` will be replaced, keeping all others as they were.

            >>> staff = abjad.Staff(
            ...     r"R1 "
            ...     r"\time 3/4 c'2. "
            ...     r"\time 4/4 d'1 "
            ...     r"e'1 "
            ...     r"\time 6/4 f'2. g'2. "
            ...     r"\time 2/4 a'2"
            ... )
            >>> abjad.attach(abjad.BarLine('.|:'), staff[0])
            >>> abjad.attach(abjad.BarLine(':|.'), staff[1])
            >>> abjad.attach(abjad.BarLine('|'), staff[3])
            >>> abjad.attach(abjad.BarLine('!'), staff[5])
            >>> score = abjad.Score([staff])
            >>> score.add_double_bar_lines_before_time_signatures()
            >>> abjad.show(score)

            ..  docs::

                \new Score
                <<
                    \new Staff
                    {
                        R1
                        \bar ".|:"
                        \time 3/4
                        c'2.
                        \bar ":|."
                        \time 4/4
                        d'1
                        e'1
                        \bar "||"
                        \time 6/4
                        f'2.
                        g'2.
                        \bar "!"
                        \time 2/4
                        a'2
                    }
                >>

            ..  figure:: ../_images/Score-XVe9oSR8Gi.png
        """
        if not isinstance(to_each_voice, bool):
            raise TypeError("'to_each_voice' must be 'bool'")
        for staff in abjad.Iteration(self).components(abjad.Staff):
            voices = [voice for voice
                      in abjad.Iteration(staff).components(abjad.Voice)]
            if len(voices) == 0:
                self._double_bar_line_adder(staff)
            elif not to_each_voice:
                self._double_bar_line_adder(voices[-1])
            else:
                for voice in voices:
                    self._double_bar_line_adder(voice)

    @staticmethod
    def _double_bar_line_adder(container: abjad.Container) -> None:
        r"""Goes through a container and adds double bar lines before each and
        every time signature change."""
        leaves = abjad.select(container).leaves()
        for i, leaf in enumerate(leaves[1:], 1):
            time_signature = abjad.get.indicator(leaf, abjad.TimeSignature)
            if time_signature is not None:
                bar_line = abjad.get.indicator(leaves[i - 1], abjad.BarLine)
                if bar_line is not None and bar_line.abbreviation in ('|', ''):
                    abjad.detach(abjad.BarLine, leaves[i - 1])
                    bar_line = None
                if bar_line is None:
                    abjad.attach(abjad.BarLine("||"),
                                 leaves[i - 1],
                                 context='Voice',
                                 )


### EXTENSION METHODS ###

abjad.Score.add_final_bar_line = Score.add_final_bar_line
abjad.Score.add_double_bar_lines_before_time_signatures = (
    Score.add_double_bar_lines_before_time_signatures
)
