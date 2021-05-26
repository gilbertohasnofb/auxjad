from textwrap import dedent
from typing import Union

import abjad


def half_piano_pedal(argument: Union[abjad.Component, abjad.Selection],
                     *,
                     until_the_end: bool = False,
                     omit_raise_pedal_glyph: bool = False,
                     selector: abjad.Expression = abjad.select().leaves(),
                     start_piano_pedal: abjad.StartPianoPedal = None,
                     stop_piano_pedal: abjad.StopPianoPedal = None,
                     tag: abjad.Tag = None,
                     ) -> None:
    r"""Attaches half piano pedal indicators. Derived from Abjad's built-in
    |abjad.piano_pedal()|.

    Basic usage:
        Usage is very similar to |abjad.piano_pedal()|:

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> auxjad.half_piano_pedal(staff[:])
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \once \override Staff.SustainPedal.stencil =
                    #(lambda (grob) (grob-interpret-markup grob
                        #{
                            \markup {
                                \larger "½"
                                \concat {
                                    \musicglyph "pedal.Ped"
                                    \musicglyph "pedal.."
                                }
                            }
                        #}))
                c'4
                \sustainOn
                d'4
                e'4
                f'4
                \sustainOff
            }

        ..  figure:: ../_images/half_piano_pedal-KaleXflNvL.png

    ..  note::

        Auxjad automatically adds this function to the :mod:`abjad` namespace.
        Therefore it can be used either as :func:`auxjad.half_piano_pedal()` or
        |abjad.half_piano_pedal()|, as shown below:

        >>> staff1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> staff2 = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> auxjad.half_piano_pedal(staff1[:])
        >>> abjad.half_piano_pedal(staff2[:])
        >>> selections = [staff1[:], staff2[:]]
        >>> auxjad.get.selections_are_identical(selections)
        True

    ``until_the_end``:
        Call the function with ``until_the_end`` set to ``True`` to add an
        arrow to the initial pedal glyph:

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> auxjad.half_piano_pedal(staff[:],
        ...                         until_the_end=True,
        ...                         )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \once \override Staff.SustainPedal.stencil =
                    #(lambda (grob) (grob-interpret-markup grob
                        #{
                            \markup {
                                \larger "½"
                                \concat {
                                    \musicglyph "pedal.Ped"
                                    \musicglyph "pedal.."
                                }
                                \raise #-0.3 "→"
                            }
                        #}))
                c'4
                \sustainOn
                d'4
                e'4
                f'4
                \sustainOff
            }

        ..  figure:: ../_images/half_piano_pedal-rA7ZHeMrjf.png

    ``omit_raise_pedal_glyph``:
        Call the function with ``omit_raise_pedal_glyph`` set to ``False`` to
        remove the raise pedal glyph:

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> auxjad.half_piano_pedal(staff[:],
        ...                         omit_raise_pedal_glyph=True,
        ...                         )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \once \override Staff.SustainPedal.stencil =
                    #(lambda (grob) (grob-interpret-markup grob
                        #{
                            \markup {
                                \larger "½"
                                \concat {
                                    \musicglyph "pedal.Ped"
                                    \musicglyph "pedal.."
                                }
                            }
                        #}))
                c'4
                \sustainOn
                d'4
                e'4
                \once \override Staff.SustainPedal.stencil = ##f
                f'4
                \sustainOff
            }

        ..  figure:: ../_images/half_piano_pedal-p8S1KwHLIx.png

        Combined with ``until_the_end=True``:

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> auxjad.half_piano_pedal(staff[:],
        ...                         until_the_end=True,
        ...                         omit_raise_pedal_glyph=True,
        ...                         )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \once \override Staff.SustainPedal.stencil =
                    #(lambda (grob) (grob-interpret-markup grob
                        #{
                            \markup {
                                \larger "½"
                                \concat {
                                    \musicglyph "pedal.Ped"
                                    \musicglyph "pedal.."
                                }
                                \raise #-0.3 "→"
                            }
                        #}))
                c'4
                \sustainOn
                d'4
                e'4
                \once \override Staff.SustainPedal.stencil = ##f
                f'4
                \sustainOff
            }

        ..  figure:: ../_images/half_piano_pedal-Fb5rE6QB1f.png

    Pedal style:
        The style of the sustain pedal can be tweaked using |abjad.setting()|
        as shown below:

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> auxjad.half_piano_pedal(staff[:])
        >>> abjad.setting(staff).pedal_sustain_style = "#'mixed"
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            \with
            {
                pedalSustainStyle = #'mixed
            }
            {
                \once \override Staff.SustainPedal.stencil =
                    #(lambda (grob) (grob-interpret-markup grob
                        #{
                            \markup {
                                \larger "½"
                                \concat {
                                    \musicglyph "pedal.Ped"
                                    \musicglyph "pedal.."
                                }
                            }
                        #}))
                c'4
                \sustainOn
                d'4
                e'4
                f'4
                \sustainOff
            }

        ..  figure:: ../_images/half_piano_pedal-6q9Swb2elq.png

        This tweak also works with ``until_the_end=True`` if desired:

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> auxjad.half_piano_pedal(staff[:],
        ...                         until_the_end=True,
        ...                         )
        >>> abjad.setting(staff).pedal_sustain_style = "#'mixed"
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            \with
            {
                pedalSustainStyle = #'mixed
            }
            {
                \new Staff
                {
                    \once \override Staff.SustainPedal.stencil =
                        #(lambda (grob) (grob-interpret-markup grob
                            #{
                                \markup {
                                    \larger "½"
                                    \concat {
                                        \musicglyph "pedal.Ped"
                                        \musicglyph "pedal.."
                                    }
                                    \raise #-0.3 "→"
                                }
                            #}))
                c'4
                \sustainOn
                d'4
                e'4
                f'4
                \sustainOff
            }

        ..  figure:: ../_images/half_piano_pedal-cYyRwFvnFH.png
    """
    assert isinstance(selector, abjad.Expression)
    argument = selector(argument)
    leaves = abjad.Selection(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    if not until_the_end:
        string = r"""
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    #{
                        \markup {
                            \larger "½"
                            \concat {
                                \musicglyph "pedal.Ped"
                                \musicglyph "pedal.."
                            }
                        }
                    #}))
            """
    else:
        string = r"""
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    #{
                        \markup {
                            \larger "½"
                            \concat {
                                \musicglyph "pedal.Ped"
                                \musicglyph "pedal.."
                            }
                            \raise #-0.3 "→"
                        }
                    #}))
            """
    string = dedent(string).strip()
    half_pedal_tweak = abjad.LilyPondLiteral(string)
    abjad.attach(half_pedal_tweak, start_leaf)
    if omit_raise_pedal_glyph:
        omit_raise_pedal_glyph_tweak = abjad.LilyPondLiteral(
            r"\once \override Staff.SustainPedal.stencil = ##f"
        )
        abjad.attach(omit_raise_pedal_glyph_tweak, stop_leaf)
    abjad.piano_pedal(argument=argument,
                      selector=selector,
                      start_piano_pedal=start_piano_pedal,
                      stop_piano_pedal=stop_piano_pedal,
                      tag=tag,
                      )


abjad.spanners.half_piano_pedal = half_piano_pedal
abjad.half_piano_pedal = half_piano_pedal
