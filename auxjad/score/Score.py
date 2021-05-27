import abjad


class Score(abjad.Score):
    r"Score."

    def add_final_barline(self) -> None:
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

            >>> score.add_final_barline()
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
            >>> score.add_final_barline()
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

            >>> staff_1 = abjad.Staff(r"c''1 d''1 e''1 f''1")
            >>> staff_2 = abjad.Staff(r"c'1 d'1 e'1 f'1")
            >>> score = abjad.Score([staff_1, staff_2])
            >>> score.add_final_barline()
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

        Multiple voices:
            Works with staves with multiple voices:

            >>> voice_1 = abjad.Voice(r"c''1 d''1 e''1 f''1")
            >>> voice_2 = abjad.Voice(r"c'2 d'2 e'2 f'2 g'2 a'2 b'2 c''2")
            >>> staff_1 = abjad.Staff([voice_1, voice_2], simultaneous=True)
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceOne'), voice_1)
            >>> abjad.attach(abjad.LilyPondLiteral(r'\voiceTwo'), voice_2)
            >>> staff_2 = abjad.Staff(r"c'1 d'1 e'1 f'1")
            >>> score = abjad.Score([staff_1, staff_2])
            >>> score.add_final_barline()
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
                    \new Staff
                    {
                        c'1
                        d'1
                        e'1
                        f'1
                        \bar "|."
                    }
                >>

            ..  figure:: ../_images/Score-RNDEWuut8j.png
        """
        for component in self._components:
            last_leaf = abjad.select(component).leaf(-1)
            abjad.attach(abjad.BarLine("|."), last_leaf, context='Staff')


### EXTENSION METHODS ###

abjad.Score.add_final_barline = Score.add_final_barline
